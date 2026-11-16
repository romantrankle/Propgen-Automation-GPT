import httpx
import pytest
from typer.testing import CliRunner

from propgen.cli import app
from propgen.client import METHODS, Client, PropGenError, Settings, specification


@pytest.fixture
def factory():
    clients = []

    def make(handler, **kw):
        client = Client("test-secret", transport=httpx.MockTransport(handler), **kw)
        clients.append(client)
        return client

    yield make
    for client in clients:
        client.close()


def test_auth(factory):
    def handler(req):
        assert req.headers["X-API-Key"] == "test-secret"
        assert str(req.url) == "https://crm.propgen.ai/public_api/v1/contacts?limit=1"
        return httpx.Response(200, json={"data": [], "meta": {"has_more": False}})

    factory(handler).request("get", "/contacts", query={"limit": 1})
    assert "test-secret" not in repr(Settings(api_key="test-secret"))


def test_no_key(monkeypatch):
    monkeypatch.delenv("PROPGEN_API_KEY", raising=False)
    with pytest.raises(PropGenError, match="not configured"):
        Client()


@pytest.mark.parametrize(
    "kwargs",
    [
        {"path": "https://evil.invalid"},
        {"path": "/contacts", "query": {"limit": 201}},
        {"path": "/contacts", "query": {"unknown": 1}},
        {"path": "/contacts", "headers": {"X-API-Key": "override"}},
        {"path": "/contacts/{id}", "path_params": {"id": "../account"}},
        {"path": "/contacts/{id}", "path_params": {}},
    ],
)
def test_invalid_no_request(factory, kwargs):
    def fail(req):
        pytest.fail("Invalid input sent")

    with pytest.raises(PropGenError):
        factory(fail).request("get", **kwargs)


@pytest.mark.parametrize(
    "method,path",
    [
        ("delete", "/contacts/{id}"),
        ("post", "/contacts/batch"),
        ("post", "/automations/{id}/runs"),
        ("patch", "/deals/{id}"),
    ],
)
def test_mutation_gates(factory, method, path):
    c = factory(lambda r: pytest.fail("Unexpected production mutation"))
    for flags in [{}, {"authorize_write": True}, {"confirm": True}]:
        with pytest.raises(PropGenError):
            c.request(method, path, **flags)


def test_mocked_create(factory):
    def handler(req):
        assert req.method == "POST"
        assert b"contact" in req.content
        return httpx.Response(201, json={"data": {}})

    factory(handler).request(
        "post", "/contacts", body={"contact": {}}, authorize_write=True, confirm=True
    )


def test_missing_body(factory):
    with pytest.raises(PropGenError, match="body required"):
        factory(lambda r: pytest.fail()).request(
            "post", "/contacts", authorize_write=True, confirm=True
        )


def test_pagination(factory):
    seen = []

    def handler(req):
        seen.append(req.url.params.get("cursor"))
        return httpx.Response(
            200, json={"data": [], "meta": {"has_more": len(seen) == 1, "next_cursor": "next"}}
        )

    assert list(factory(handler).paginate("/contacts")) == []
    assert seen == [None, "next"]


def test_cursor_loop(factory):
    c = factory(
        lambda r: httpx.Response(
            200, json={"data": [], "meta": {"has_more": True, "next_cursor": "same"}}
        )
    )
    with pytest.raises(PropGenError, match="repeated"):
        list(c.paginate("/contacts"))


@pytest.mark.parametrize("status", [401, 403, 412, 422, 429, 500])
def test_sanitized_errors(factory, status):
    c = factory(lambda r: httpx.Response(status, json={"secret": "test-secret"}), retries=0)
    with pytest.raises(PropGenError) as exc:
        c.request("get", "/contacts")
    assert "test-secret" not in str(exc.value)
    assert str(status) in str(exc.value)


def test_retry(factory, monkeypatch):
    waits, calls = [], []
    monkeypatch.setattr("propgen.client.time.sleep", waits.append)

    def handler(req):
        calls.append(req)
        if len(calls) == 1:
            return httpx.Response(429, headers={"Retry-After": "3"})
        return httpx.Response(200, json={"data": []})

    factory(handler).request("get", "/contacts")
    assert waits == [3]
    assert len(calls) == 2


def test_no_write_retry(factory):
    calls = []

    def handler(req):
        calls.append(req)
        return httpx.Response(503)

    with pytest.raises(PropGenError):
        factory(handler).request(
            "post", "/contacts", body={"contact": {}}, authorize_write=True, confirm=True
        )
    assert len(calls) == 1


def test_all_operations_registered(factory):
    c = factory(lambda r: pytest.fail())
    for path, ops in specification()["paths"].items():
        for method in ops.keys() & METHODS:
            assert c.operation(method, path) == ops[method]


def test_cli(monkeypatch):
    runner = CliRunner()
    result = runner.invoke(app, ["capabilities"])
    assert result.exit_code == 0
    assert "GET /automations/{id}" in result.stdout
    monkeypatch.delenv("PROPGEN_API_KEY", raising=False)
    assert runner.invoke(app, ["check-connection"]).exit_code == 1


def test_nullable_and_refs(factory):
    c = factory(lambda r: pytest.fail())
    c.validate(None, {"type": "string", "nullable": True})
    with pytest.raises(PropGenError):
        c.validate("bad", {"type": "integer"})


def test_multipart(factory):
    def handler(req):
        assert "multipart/form-data" in req.headers["content-type"]
        assert b"report.txt" in req.content
        return httpx.Response(201, json={"data": []})

    factory(handler).request(
        "post",
        "/documents",
        body={"entity_type": "contact", "entity_id": 1},
        uploads={"files": [("report.txt", b"example", "text/plain")]},
        authorize_write=True,
        confirm=True,
    )


def test_response_validation(factory):
    c = factory(lambda r: httpx.Response(200, json={"data": "wrong type"}))
    with pytest.raises(PropGenError, match="schema"):
        c.request("get", "/contacts")


def test_long_retry_after(factory, monkeypatch):
    monkeypatch.setattr("propgen.client.time.sleep", lambda _: pytest.fail("Must not retry early"))
    c = factory(lambda r: httpx.Response(429, headers={"Retry-After": "120"}))
    with pytest.raises(PropGenError, match="429"):
        c.request("get", "/contacts")


def test_download_does_not_follow_redirect(factory):
    c = factory(lambda r: httpx.Response(302, headers={"Location": "https://example.com/"}))
    with pytest.raises(PropGenError, match="302"):
        c.request(
            "get",
            "/documents/{id}/download",
            path_params={"id": 1},
            query={"entity_type": "contact", "entity_id": 1},
        )
