# claude-code-fleet-support

`claude-code-fleet-support` is the standalone public support-layer product in the PALIOS-TAEY support architecture. `v0.1.0` ships the Phase 0 MVP spine: GitHub webhook intake, Redis-backed support event storage, deterministic `thread_id` generation, Claude-driven triage, owner routing via `taey-notify`, and product bug-lock helpers.

## Status

- [Observed] `v0.1.0` is a working Phase 0 MVP with one live intake channel: GitHub issue webhooks.
- [Observed] Storage is Redis-only in this release: `taey:support:inbox`, `taey:support:event:*`, `taey:support:thread:*`, and `taey:support:thread:*:events`.
- [Observed] The daemon entrypoint is `scripts/cf-support-intake`; it exposes `POST /github/webhook` and `GET /healthz`.
- [Observed] Triage runs through the local Claude CLI in non-interactive print mode, default model alias `haiku`.
- [Unknown] Whether a direct Anthropic API integration should replace the local CLI surface in a later release. This MVP does not ship that swap.

## What Ships In `v0.1.0`

- [Observed] Deterministic GitHub thread IDs like `github:palios-taey/claude-code-fleet-support#42`
- [Observed] Explicit-reference extraction for cross-thread suggestions without automatic merges
- [Observed] GitHub webhook signature verification (`X-Hub-Signature-256`)
- [Observed] One-tier triage: `bug | not_bug | spam`
- [Observed] Owner routing via `taey-notify`
- [Observed] Bug-lock helpers for `support:product:<id>:bug_lock*`
- [Observed] First-contact disclosure text per the locked architecture

## Install

```bash
pip install -r requirements.txt
make install
```

## Run

Required runtime dependencies:

- [Observed] Redis reachable at `REDIS_HOST` / `REDIS_PORT` or default `127.0.0.1:6379`
- [Observed] A working local `claude` CLI auth surface, or `CF_SUPPORT_CLAUDE_BIN` pointing at one

Optional environment variables:

```bash
export CF_SUPPORT_GITHUB_WEBHOOK_SECRET="change-me"
export CF_SUPPORT_OWNER_MAP_JSON='{"claude-code-fleet-support":"conductor"}'
export CF_SUPPORT_CLAUDE_MODEL="haiku"
export CF_SUPPORT_NOTIFY_BIN="/usr/local/bin/taey-notify"
```

Start the daemon:

```bash
cf-support-intake --host 127.0.0.1 --port 8045
```

Health:

```bash
curl http://127.0.0.1:8045/healthz
```

## Phase Boundaries

- [Observed] No UI ships in `v0.1.0`.
- [Observed] No Postgres ships in `v0.1.0`.
- [Observed] GitHub is the only implemented intake channel in this release.
- [Observed] `chatwoot.py`, `gmail.py`, and `x_bridge.py` remain future work and are intentionally out of the Phase 0 MVP path.

## Verification

- [Observed] A real GitHub webhook delivery was production-verified on May 27, 2026 against `palios-taey/claude-code-fleet-support`.
- [Observed] Verification evidence is recorded in `PHASE0_VERIFICATION.md`.
