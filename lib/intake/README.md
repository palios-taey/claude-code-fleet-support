# `lib/intake/` — channel adapters

## Phase 0 (v0.1.0, current)

| Adapter | Status | Notes |
|---|---|---|
| `github_webhook.py` | **Implemented + production-verified** | Real GitHub webhook delivery exercised in `PHASE0_VERIFICATION.md`. |
| `gmail.py` | Deferred — raises `NotImplementedError` | Activate per spec §15.5 demand-trigger when first Gmail-channel demand is observed. |
| `x_bridge.py` | Deferred — raises `NotImplementedError` | X channel intake. Activate when x-claude's X distribution lane warrants direct intake (currently informal monitoring is sufficient). |

## Dropped (NOT in this product)

- **Chatwoot intake** — adoption was rejected per architecture spec §15 (Family A/B/C consultation 2026-05-27 reconciled 5/5 on Option B: native Python spine, no Chatwoot). The Chatwoot stub file was removed at the same time.

## Adding a new adapter

Phase 0 design (per spec §15.1): one channel to start, add incrementally per real demand. When adding a new adapter:

1. Implement it in this directory.
2. Normalize incoming events to the canonical event hash schema (spec §6).
3. Compute `thread_id` via `lib.thread_id.thread_id_from_event(channel, channel_unique_id)` — deterministic composite key per spec §2.1.
4. Cross-channel linking ONLY via explicit reference extraction (URL parsing, issue-ID format detection). Never via content-similarity merge (per spec §2.1 security argument).
5. Add a test cycle in `PHASE0_VERIFICATION.md` (or `PHASE1_VERIFICATION.md` if you're past v0.1.x) using real traffic, not synthetic.
