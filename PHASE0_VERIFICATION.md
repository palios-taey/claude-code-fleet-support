# Phase 0 Verification

Date: 2026-05-27

## Scope

- [Observed] This verification covered the required Phase 0 path: real GitHub issue webhook delivery into `cf-support-intake`, normalization into `taey:support:*`, triage, and owner notification.
- [Observed] Verification target repo: `palios-taey/claude-code-fleet-support`
- [Observed] Webhook endpoint used during verification: a temporary Cloudflare quick tunnel pointed at local `cf-support-intake` on `127.0.0.1:8045`

## Production Evidence

- [Observed] Repository webhook `631870904` was created on `palios-taey/claude-code-fleet-support` with URL `https://whether-relevance-pregnant-arbitration.trycloudflare.com/github/webhook`.
- [Observed] GitHub recorded delivery `3822301495848615936` with GUID `a8e40996-59e5-11f1-9309-438b94af4e7d` at `2026-05-27T16:03:55.034Z`, `event="issues"`, `action="opened"`, `status="OK"`, `status_code=200`.
- [Observed] The real verification issue was created at `https://github.com/palios-taey/claude-code-fleet-support/issues/1`.
- [Observed] That delivery produced Redis event `taey:support:event:evt_7390640fa54b4df2a47327b2a4f4f48a` with:
  - `thread_id=github:palios-taey/claude-code-fleet-support#1`
  - `channel_ref=palios-taey/claude-code-fleet-support#1`
  - `triage_state=not_bug`
  - `triage_confidence=0.78`
  - `assigned_owner=conductor-codex`
  - `owner_notified_at=2026-05-27T16:04:09Z`
- [Observed] Thread index `taey:support:thread:github:palios-taey/claude-code-fleet-support#1:events` contained the event id `evt_7390640fa54b4df2a47327b2a4f4f48a`.
- [Observed] Owner notification was delivered to `taey:conductor-codex:inbox` with a `directive` from `cf-support` containing the triage decision and thread reference.

## Local Shakeout Evidence

- [Observed] Before the real GitHub delivery, a signed local webhook POST hit `POST /github/webhook` successfully and produced Redis event `evt_7c4eee53dba145ab81b5bf983f661d06`.
- [Observed] That local event classified as `bug` with confidence `0.87` and routed successfully to `conductor-codex`.
- [Observed] The bug-lock write threshold did not fire during either observed verification event because neither run met the architecture gate `bug && confidence >= 0.90`, and no owner-confirmation path was exercised.

## Configuration Notes

- [Observed] Verification used `CF_SUPPORT_OWNER_MAP_JSON='{"claude-code-fleet-support":"conductor-codex"}'` so the notification could be observed directly in the peer session inbox.
- [Inferred] Without that override, the default owner map would have routed this product to `conductor`.

## Unknowns

- [Unknown] This verification did not exercise the owner-confirmed bug-lock path.
- [Unknown] This verification did not exercise the non-GitHub intake adapters, which remain outside Phase 0.
