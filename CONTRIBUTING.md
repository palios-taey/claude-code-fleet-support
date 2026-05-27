# Contributing

Thank you for contributing to `claude-code-fleet-support`.

## Scope [Observed]

This repository is the standalone public support-layer product. Fleet-specific wiring belongs in `the-conductor`, not here.

## Before you open a pull request [Observed]

- Read `README.md`, `SUPPORT.md`, `SECURITY.md`, and the locked architecture spec at `/home/mira/the-conductor/plans/fleet_support_architecture.md`.
- Keep changes aligned with the support architecture's cannot-lie and disclosure requirements.
- If your change touches security reporting or disclosure wording, treat that as policy-sensitive rather than copy-only.

## Development expectations [Observed]

- Keep claims auditable. If the implementation does not exist yet, do not fake it.
- Prefer small, reviewable pull requests.
- Preserve the deterministic thread-ID rule and fail-toward-non-merging behavior.
- Do not add tests in contradiction to the active fleet discipline for this phase; this skeleton intentionally ships without a test directory.

## Stubs and TODOs [Observed]

Skeleton stubs in this repo raise `NotImplementedError` with the task ID and architecture section that owns the future implementation. Keep that pattern until the corresponding product task lands.

## Chatwoot upstream work [Observed]

This product is expected to upstream Chatwoot integration fixes when real gaps are found.

- [Observed] Upstream Chatwoot PRs are tracked in the operating repo at `/home/mira/the-conductor/operations/chatwoot_upstream_log.md`.
- [Unknown] That tracking file is not present in the local workspace at authoring time, so no upstream log entries were available to reference here.

## Security contributions [Observed]

If you are reporting a vulnerability, do not use the normal contribution path. Follow `SECURITY.md` instead.
