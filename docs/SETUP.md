# Setup and configuration

Install Python 3.12+, then `python -m pip install -e '.[dev]'`. Inject `PROPGEN_API_KEY` through
your execution environment's secret manager. Do not paste keys into chat, scripts or commands.
The placeholder in .env.example is not a credential; the project never automatically loads .env.
Authentication is X-API-Key, an explicitly documented alternative to Bearer authentication.
The origin and /public_api/v1 base path are pinned; redirects are disabled.

This execution workspace had no configured PROPGEN_API_KEY and no Git repository or remote.
Supply a repository checkout or remote before pushing. Select the necessary API scopes in
PropGen Settings → Integrationen → API-Schlüssel; list and read are independent permissions.
Allow the runner's egress IP if an allowlist is configured.

HTTP-secret substitution: no documented substitution mechanism was provided or discovered for
this runtime. Do not invent a placeholder syntax. If Python cannot access the secret, configure
a runner that injects PROPGEN_API_KEY into its process environment, or provide the runtime's
official HTTP-secret documentation and adapt the transport. Do not claim authentication works
until `propgen check-connection` succeeds. No production mutations are needed for setup.
