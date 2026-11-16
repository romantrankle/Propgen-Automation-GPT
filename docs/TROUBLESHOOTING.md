# Troubleshooting

401: configure a valid key; do not repeatedly probe missing credentials. Twenty invalid requests
per minute can block the IP for ten minutes. 403: check independent scopes, user-bound record
permissions and source IP allowlists. RestrictedEntity intentionally omits private fields.
412: re-read the target and reconcile changes; never overwrite blindly. 422: consult published
schema and effective form metadata. 429: respect Retry-After and per-key settings.
Transport failure during a mutation: outcome is unknown; inspect state before retrying.
Schema mismatch: stop and compare the pinned specification with current upstream; do not disable
validation blindly. Errors suppress server bodies deliberately; inspect safely in a secure debugger
if needed. Do not enable httpx/httpcore debug logging in environments containing real credentials.
No live write access has been verified. There is no guessed leads endpoint or signing endpoint.
