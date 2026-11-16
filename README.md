# PropGen AI integration

Python 3.12+ integration driven by the complete official OpenAPI snapshot. Every documented
method/path is accessible through one validated client, including automation drafts, execution,
deployments, rollback and logs. No undocumented resource aliases are invented.

```bash
python -m pip install -e '.[dev]'
# Set PROPGEN_API_KEY securely in the calling environment; .env is not automatically loaded.
propgen capabilities
propgen check-connection
propgen call GET /contacts --query '{"limit":10}'
propgen call GET '/automations/{id}' --path-params '{"id":1200}'
```

`AGENTS.md` teaches Codex to interpret natural-language instructions using this client.
There is no standalone natural-language model or hosted MCP server.

```python
from propgen import Client

with Client() as client:
    for contact in client.paginate("/contacts", query={"limit": 100}):
        pass  # Process privately; do not log personal information.
```

Writes require both authorization flags and validated schema inputs. Obtain user confirmation
as described in AGENTS.md, read targets first, and verify effects afterward. All non-GET
operations are conservatively gated. Multipart uploads are available through Python's
`uploads={field: (filename, bytes, content_type)}` or a list of those tuples for array fields;
use the exact documented field name. CLI supports JSON bodies and binary response output.

See docs/API_CAPABILITIES.md for every operation, permissions, request and response schemas,
and the distinction between documented, mocked and live verification. See docs/SETUP.md,
docs/OPERATIONS.md and docs/TROUBLESHOOTING.md for operational guidance.
