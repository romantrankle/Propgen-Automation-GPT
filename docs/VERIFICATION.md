# Verification report — 2026-11-16

- Official YAML retrieved successfully via HTTPS and parsed: 223 paths, 401 operations.
- Automated suite: 31 passed, all HTTP tests mocked. Representative mutation tests only;
  not all 401 operations have endpoint-specific fixtures.
- Ruff lint and formatting checks passed.
- Authenticated read check attempted but stopped locally: PROPGEN_API_KEY not configured.
  No authenticated request was sent. No production writes, deletions, workflow runs or messages.
- Secret review found no private-key markers; credentials in tests are synthetic. No real key was
  present in the environment or written to files. This is not a third-party secret scanner audit.
- Initial /workspace had no usable Git repository and no remote. Created an isolated local project
  repository in /workspace/propgen-ai. Subsequently connected the user-specified remote
  https://github.com/romantrankle/Propgen-Automation-GPT.git and pushed main successfully.
  Local tests, lint and formatting checks passed again before publishing. GitHub Actions
  results have not yet been verified.
- All API operations remain documented but not live-tested. Permissions and actual server response
  compatibility remain unverified. Do not call the integration production-verified yet.

Implemented resource families: projects; contacts; companies; search profiles; leases;
properties, images, media, links and associations; pipelines and columns; deals; tasks and subtasks;
tags, statuses and sources; notes and labels; booking slots and bookings; calendar events;
activities; phone calls; emails; legal proofs; datenraums; document activities; templates and
merge capabilities; document generation; documents and attachments; folders; account profile,
assets and signatures; cost centers; invoice service types, payment terms and text templates;
user assignments and agent numbers; lookups; search; form definitions and customizations;
webhooks and deliveries; automation capabilities, references, recipes, plans, drafts, revisions,
deployments, rollback, activation, manual runs, cancellation, metrics and execution steps.
Exact complete method/path list with schemas and scope descriptions: API_CAPABILITIES.md.

Unsupported or undocumented: standalone leads resource, contract signing, arbitrary server logs,
and booking-page creation. These are not invented. Lead classification must use tenant metadata.
Data rooms have documented reads only. The client deliberately rejects redirects and external
schema references; binary downloads requiring a redirect would need a safe reviewed enhancement.
