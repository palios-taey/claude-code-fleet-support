# claude-code-fleet-support

We run a public, AI-assisted support intake that discloses itself on first contact, unifies reports across channels, routes confirmed bugs to the owning product, stops conflicting feature work while a bug lock is active, and keeps the issue pulled forward until closure without promising a fixed resolution clock.

`claude-code-fleet-support` is the standalone public support-layer product in the locked PALIOS-TAEY support architecture. [Observed] This repository currently ships a valid Python skeleton at `v0.0.2`, not a finished support daemon.

## Status

- [Observed] The repository contains installable package structure, daemon entrypoint scaffolding, and documentation aligned to the locked architecture.
- [Observed] Core runtime logic is still stubbed and raises `NotImplementedError` with the corresponding product task ID and architecture section.
- [Inferred] A standalone, disclosed, AI-native support layer is critical for adoption of the broader fleet product set.
- [Unknown] Whether support is the primary adoption bottleneck versus docs, discoverability, or product maturity. We have not measured that yet.

## Design Depth

- [Observed] The locked architecture spec used for this skeleton lives at `/home/mira/the-conductor/plans/fleet_support_architecture.md`.
- [Observed] The implementation plan lives at `/home/mira/the-conductor/plans/fleet_support_product.md`.

## What This Repo Is For

- [Observed] Chatwoot-backed support intake normalization
- [Observed] Unified cross-channel support thread records
- [Observed] One-tier bug-or-not-bug triage
- [Observed] Per-product routing via `taey-notify`
- [Observed] Product-level bug locks in Redis
- [Observed] First-contact AI disclosure with explicit limits on authority and memory

## What Ships In `v0.0.2`

- [Observed] `lib/intake/` adapter stubs for Chatwoot, GitHub webhooks, Gmail, and X bridge ingestion
- [Observed] `lib/triage.py`, `lib/router.py`, `lib/buglock.py`, `lib/disclosure.py`, and `lib/thread_id.py`
- [Observed] `scripts/cf-support-intake` daemon entrypoint stub
- [Observed] Repository support and security docs customized for this product

## Non-Goals In This Skeleton

- [Observed] No live production support logic yet
- [Observed] No tests in this phase, per fleet discipline
- [Observed] No severity tiering; the architecture is severity-free once a bug is confirmed
- [Observed] No automatic similarity-based thread merging; uncertain links must fail toward non-merging and owner review

## Repository Layout

```text
lib/
  intake/
    chatwoot.py
    github_webhook.py
    gmail.py
    x_bridge.py
  buglock.py
  disclosure.py
  router.py
  thread_id.py
  triage.py
scripts/
  cf-support-intake
docs/
  CHATWOOT_INSTALL.md
  DISCLOSURE.md
  TRIAGE.md
```

## Install

- [Observed] `make install` installs the `cf-support-intake` daemon binary and copies the Python package payload under `/usr/local/lib/claude-code-fleet-support`.
- [Observed] Packaging metadata is in `pyproject.toml`; dependency pinning is in `requirements.txt`.

## Transparency

- [Observed] This product is designed to be adoptable without `the-conductor`; fleet-specific wiring belongs in that integration repo, not here.
- [Observed] Upstream Chatwoot improvement tracking is intended to live in the operating repo at `/home/mira/the-conductor/operations/chatwoot_upstream_log.md`.
- [Unknown] That upstream tracking file is not present in the local workspace at authoring time.
