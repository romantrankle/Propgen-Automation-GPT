# Operations

Use `propgen capabilities` to inspect operation templates, then consult the matching entry in
API_CAPABILITIES.md and pinned OpenAPI for typed inputs. `propgen call METHOD TEMPLATE`
accepts JSON --path-params, --query and --headers; --body-file contains a JSON request body.
Downloads can be saved using --output. Output may contain personal information.

Before updates, fetch the target and retain its response ETag. Pass it as If-Match to protect
against lost updates. Required automation revision and idempotency headers are schema validated.
Do not automatically replay uncertain writes. Client retries only GET transport failures and
429/502/503/504, at most two retries by default. Retry-After over 60 seconds returns the error
instead of retrying early. Cursor iteration detects loops and has a page budget.

Example Codex instructions (documented, pending live verification):
- List contacts tagged as leads using the configured contact statuses.
- Find properties with missing descriptions and show a proposed correction.
- Show open deals in the acquisition pipeline after resolving its ID and stages.
- Inspect automation 1200 and its recent run failures without triggering it.
- List available data rooms and document metadata without downloading files.

For new leads created today, determine the user's lead classification first, paginate contacts,
and filter created_at for the correct local-day interval; updated_since is not creation time.
For new records use exact documented wrappers (e.g. contact) and effective /schema or form
metadata. Client validation enforces published schemas; dynamic fields and business rules still
require server validation. Pydantic validates client configuration; JSON Schema validates API data.
