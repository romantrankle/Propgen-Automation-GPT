"""Pinned OpenAPI operation executor. No arbitrary URLs or hidden writes."""

import logging
import os
import re
import time
from functools import lru_cache
from importlib.resources import files
from urllib.parse import quote

import httpx
import yaml
from jsonschema import Draft4Validator, FormatChecker
from pydantic import BaseModel, ConfigDict, Field, SecretStr

BASE_URL = "https://crm.propgen.ai/public_api/v1"
METHODS = {"get", "post", "put", "patch", "delete"}
log = logging.getLogger("propgen")


class PropGenError(Exception):
    """Sanitized error; deliberately excludes CRM bodies, URLs and credentials."""


class Settings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    api_key: SecretStr
    timeout: float = Field(default=30, gt=0, le=120)
    retries: int = Field(default=2, ge=0, le=5)


@lru_cache(maxsize=1)
def specification():
    return yaml.safe_load(files("propgen").joinpath("openapi.yaml").read_text())


def normalize(value):
    """Translate OpenAPI 3 nullable to JSON Schema draft 4, retaining local refs."""
    if isinstance(value, list):
        return [normalize(x) for x in value]
    if not isinstance(value, dict):
        return value
    result = {k: normalize(v) for k, v in value.items() if k != "nullable"}
    if value.get("nullable"):
        return {"anyOf": [result, {"type": "null"}]}
    return result


class Client:
    def __init__(self, api_key=None, *, transport=None, timeout=30, retries=2):
        key = api_key or os.environ.get("PROPGEN_API_KEY")
        if not key:
            raise PropGenError("PROPGEN_API_KEY is not configured")
        self.settings = Settings(api_key=key, timeout=timeout, retries=retries)
        self.spec = specification()
        self.http = httpx.Client(
            base_url=BASE_URL + "/",
            headers={"X-API-Key": self.settings.api_key.get_secret_value()},
            timeout=timeout,
            follow_redirects=False,
            transport=transport,
        )

    def close(self):
        self.http.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def resolve(self, obj):
        while "$ref" in obj:
            ref = obj["$ref"]
            if not ref.startswith("#/"):
                raise PropGenError("External schema references are disabled")
            obj = self.spec
            for part in ref[2:].split("/"):
                obj = obj[part.replace("~1", "/").replace("~0", "~")]
        return obj

    def validate(self, value, schema):
        root = normalize(schema)
        root["components"] = normalize(self.spec["components"])
        if not Draft4Validator(root, format_checker=FormatChecker()).is_valid(value):
            raise PropGenError("Input or response does not match the documented schema")

    def operation(self, method, path):
        method = method.lower()
        if method not in METHODS or method not in self.spec["paths"].get(path, {}):
            raise PropGenError("Undocumented operation rejected")
        return self.spec["paths"][path][method]

    def request(
        self,
        method,
        path,
        *,
        path_params=None,
        query=None,
        body=None,
        headers=None,
        uploads=None,
        authorize_write=False,
        confirm=False,
    ):
        op = self.operation(method, path)
        method = method.lower()
        if method != "get" and not authorize_write:
            raise PropGenError("Writes require explicit authorization")
        # Conservative: every mutation requires confirmation, including final-state changes.
        if method != "get" and not confirm:
            raise PropGenError("Mutation requires confirmation of the exact action and target")
        pp, query, headers = dict(path_params or {}), dict(query or {}), dict(headers or {})
        params = [self.resolve(p) for p in self.spec["paths"][path].get("parameters", [])]
        params += [self.resolve(p) for p in op.get("parameters", [])]
        buckets = {"path": pp, "query": query, "header": headers}
        for location, supplied in buckets.items():
            allowed = {p["name"] for p in params if p["in"] == location}
            if location == "header":
                allowed |= {"If-Match", "Idempotency-Key"}
            if supplied.keys() - allowed:
                raise PropGenError("Undocumented parameter rejected")
        for p in params:
            supplied = buckets.get(p["in"], {})
            if p.get("required") and p["name"] not in supplied:
                raise PropGenError("Required documented parameter missing")
            if p["name"] in supplied:
                self.validate(supplied[p["name"]], p.get("schema", {}))
        if set(pp) != set(re.findall(r"{([^}]+)}", path)):
            raise PropGenError("Path parameters do not match template")
        for name, value in pp.items():
            if str(value) in {".", ".."} or any(c in str(value) for c in "/\\%?#"):
                raise PropGenError("Unsafe path parameter")
            path = path.replace("{" + name + "}", quote(str(value), safe=""))
        kwargs = {"params": query, "headers": headers}
        rb = self.resolve(op["requestBody"]) if "requestBody" in op else None
        if not rb and (body is not None or uploads):
            raise PropGenError("Operation has no documented body")
        if rb:
            if rb.get("required") and body is None and not uploads:
                raise PropGenError("Request body required")
            content = rb["content"]
            if "application/json" in content:
                if uploads:
                    raise PropGenError("Operation does not accept uploads")
                if body is not None:
                    self.validate(body, content["application/json"].get("schema", {}))
                    kwargs["json"] = body
            elif "multipart/form-data" in content:
                sample = dict(body or {})
                for name, items in (uploads or {}).items():
                    sample[name] = [v[0] for v in items] if isinstance(items, list) else items[0]
                self.validate(sample, content["multipart/form-data"].get("schema", {}))
                kwargs["data"] = {k: str(v) for k, v in (body or {}).items()}
                kwargs["files"] = [
                    (k, item)
                    for k, items in (uploads or {}).items()
                    for item in (items if isinstance(items, list) else [items])
                ]
            else:
                raise PropGenError("Unsupported documented content type")
        for attempt in range(self.settings.retries + 1):
            try:
                response = self.http.request(method.upper(), path.lstrip("/"), **kwargs)
            except httpx.TransportError:
                if method == "get" and attempt < self.settings.retries:
                    time.sleep(2**attempt)
                    continue
                raise PropGenError("Transport failure; write outcome may be unknown") from None
            log.info("propgen_response", extra={"method": method, "status": response.status_code})
            if (
                method == "get"
                and response.status_code in {429, 502, 503, 504}
                and attempt < self.settings.retries
            ):
                try:
                    delay = max(0, float(response.headers.get("Retry-After", 2**attempt)))
                except ValueError:
                    delay = 2**attempt
                if delay <= 60:
                    time.sleep(delay)
                    continue
            if response.status_code >= 300:
                raise PropGenError(f"PropGen HTTP {response.status_code}; response body suppressed")
            result = self.resolve(op.get("responses", {}).get(str(response.status_code), {}))
            schema = result.get("content", {}).get("application/json", {}).get("schema")
            if schema is not None:
                try:
                    self.validate(response.json(), schema)
                except ValueError:
                    raise PropGenError("Invalid JSON response") from None
            return response
        raise PropGenError("Retry budget exhausted")

    def paginate(self, path, *, query=None, path_params=None, max_pages=100):
        op = self.operation("get", path)
        names = {self.resolve(p)["name"] for p in op.get("parameters", [])}
        if "cursor" not in names:
            raise PropGenError("Endpoint does not document cursor pagination")
        query = dict(query or {})
        seen = set()
        for _ in range(max_pages):
            payload = self.request("get", path, query=query, path_params=path_params).json()
            if not isinstance(payload.get("data"), list):
                raise PropGenError("Expected paginated data array")
            yield from payload["data"]
            meta = payload.get("meta", {})
            if not meta.get("has_more"):
                return
            cursor = meta.get("next_cursor")
            if not cursor or cursor in seen:
                raise PropGenError("Missing or repeated pagination cursor")
            seen.add(cursor)
            query["cursor"] = cursor
        raise PropGenError("Pagination page budget exhausted")
