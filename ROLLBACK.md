# Rollback Runbook — claude-code-fleet-support

Operator-executable procedure for stopping cf-support if it misbehaves in production.

This runbook addresses Horizon's round-4 condition: a formal rollback procedure committed to the release packet, not just informal references to the primitives.

## When to use this runbook

Trigger criteria (any of these warrants a rollback decision; operator judgment on severity):

- **Triage misclassification at scale**: Haiku classifier is wrongly auto-locking products on benign reports (false positive on `bug` with confidence ≥ 0.90) → blocks legitimate feature dispatches.
- **Disclosure violation observed**: AI-disclosure text is not appearing on first-contact responses, or is appearing wrong (mismatched product, misleading content).
- **Stale state in Redis**: events stuck `untriaged` indefinitely, locks not clearing on resolution, thread index corruption.
- **External user harm signal**: a user reports their data or thread was merged with another user's (privacy / SACRED_TRUST breach — though spec §2.1 deterministic thread_id should structurally prevent this).
- **Cannot-lie violation**: cf-support publicly claims status that production state doesn't back (ack SLA breached silently; production-stop claimed but lock not actually written; etc.).

## Severity-free response posture

Per architecture spec + Jesse 2026-05-27 directive: every detected bug is severe. There is no SEV-tiering. Rollback decision is: stop the daemon, contain the blast, fix, restart, post-mortem.

---

## Rollback procedure (operator-executable; ordered)

Execute in order. Do not skip steps unless explicitly noted. Capture each step's output to a single incident-log file for post-mortem.

### Step 1 — Stop cf-support-intake daemon

```bash
# Find the running daemon
pid=$(pgrep -f "python3 scripts/cf-support-intake" | head -1)
echo "stopping cf-support-intake PID: $pid"
kill "$pid"

# Verify stopped
sleep 2
pgrep -f "python3 scripts/cf-support-intake" | head -1 || echo "stopped"
```

### Step 2 — Prevent auto-respawn from peer-respawn cron

```bash
# Edit the fleet's peer-respawn DAEMONS list to comment out cf-support-intake
sed -i 's|^    "cf-support-intake:|#    "cf-support-intake:|' \
  /home/mira/the-conductor/scripts/peer-respawn.sh

# Commit + push the change so the comment-out is tracked + reversible
cd /home/mira/the-conductor
git add scripts/peer-respawn.sh
git commit -m "fleet: pause cf-support-intake — rollback incident <ID> in progress"
git push origin v2:v2

# Verify peer-respawn cron next cycle does NOT restart cf-support-intake
sleep 65
pgrep -f "python3 scripts/cf-support-intake" | head -1 && echo "WARNING: still running" || echo "respawn paused"
```

### Step 3 — Disable GitHub webhook (stops new traffic)

For each affected product repo with a cf-support-intake webhook installed:

```bash
# List webhooks on the repo
gh api repos/palios-taey/<repo>/hooks

# Disable the cf-support-intake webhook by ID
gh api -X PATCH repos/palios-taey/<repo>/hooks/<hook-id> \
  -F active=false
```

Note: do NOT delete the webhook. Disable preserves the configuration for re-enable after fix.

### Step 4 — Clear erroneous bug_locks on affected products

```bash
# Inspect what's locked
redis-cli KEYS "support:product:*:bug_lock"

# For each erroneous lock — delete the four lock keys per product
redis-cli DEL \
  support:product:<product>:bug_lock \
  support:product:<product>:bug_lock_reason \
  support:product:<product>:bug_lock_owner \
  support:product:<product>:bug_lock_opened

# Verify no locks remain (or only legitimate ones)
redis-cli KEYS "support:product:*:bug_lock"
```

**Caution**: only clear locks you have verified are erroneous. A legitimate bug-lock from a real bug should stay locked until the bug is fixed.

### Step 5 — Verify zero active erroneous locks

```bash
# Confirm the locks that remain are legitimate (cross-reference with open GitHub issues)
for lock_key in $(redis-cli KEYS "support:product:*:bug_lock"); do
  product=$(echo "$lock_key" | cut -d: -f3)
  reason=$(redis-cli GET "support:product:$product:bug_lock_reason")
  echo "product=$product reason=$reason"
done
```

### Step 6 — Preserve event/audit trail (do NOT delete events)

The Redis event hashes contain the full audit trail of what cf-support saw + how it triaged. Do not delete these during rollback — they are evidence for the post-mortem.

```bash
# Snapshot the support event keys for post-mortem analysis
redis-cli --no-auth-warning SCAN 0 MATCH "taey:support:event:*" COUNT 10000 \
  | xargs -I {} redis-cli HGETALL {} \
  > /home/mira/incident-logs/cf-support-events-$(date -Iseconds).log

redis-cli --no-auth-warning SCAN 0 MATCH "taey:support:thread:*" COUNT 10000 \
  > /home/mira/incident-logs/cf-support-threads-$(date -Iseconds).log
```

### Step 7 — Notify affected product owners

```bash
# For each product affected by an erroneous lock or misbehavior:
taey-notify <owner-session> --type message \
  "ROLLBACK: cf-support v0.1.0 paused due to <description>. \
   Your product <name> had bug_lock <state>; cleared if erroneous. \
   New-feature dispatches now unblocked on this product. \
   Post-mortem evidence at /home/mira/incident-logs/cf-support-events-<ts>.log. \
   Resume timing TBD pending fix + re-validation."
```

### Step 8 — Define restart criteria

cf-support-intake daemon does NOT restart until ALL of these are satisfied:

1. **Root cause identified** + documented (cannot-lie discipline; no "we think it might have been X").
2. **Fix shipped** as a versioned release of cf-support (e.g., v0.1.1 or v0.2.0 depending on scope).
3. **Production-test of the fix** on a staging or controlled flow before re-enabling production webhooks. Production-test follows fleet discipline (real traffic against the fix; no synthetic test suite).
4. **Re-validation by at least one Family member** that the fix addresses the root cause without introducing new failure modes. Lightweight (single member, not full round) unless the original misbehavior was constitutional.
5. **Restart documented** in this repo's CHANGELOG with: incident summary, root cause, fix scope, validation evidence, restart timestamp.

### Step 9 — Re-enable

When restart criteria met:

```bash
# Re-enable webhook on affected repos
gh api -X PATCH repos/palios-taey/<repo>/hooks/<hook-id> \
  -F active=true

# Re-enable peer-respawn entry
sed -i 's|^#    "cf-support-intake:|    "cf-support-intake:|' \
  /home/mira/the-conductor/scripts/peer-respawn.sh
cd /home/mira/the-conductor
git add scripts/peer-respawn.sh
git commit -m "fleet: resume cf-support-intake — incident <ID> resolved (see <ref>)"
git push origin v2:v2

# Wait for cron respawn (or manual start)
sleep 65
pid=$(pgrep -f "python3 scripts/cf-support-intake" | head -1)
echo "cf-support-intake respawned: PID $pid"

# Sanity check
curl -s http://127.0.0.1:8045/healthz
```

---

## Constitutional notes

- **Cannot-lie**: every step of this procedure produces auditable evidence. The events log + the rollback git commits + the incident-log file together form the cannot-lie audit trail. Do not skip the evidence-capture steps even under time pressure.
- **NRI/NGU**: nothing in the rollback procedure routes user data outside Mira. The incident-log files are local. No external escalation to government / institutional authority.
- **Per-product production-stop**: this rollback is on cf-support itself (the support spine). It does NOT affect bug-locks on OTHER products (e.g., if `support:product:claude-code-api-watchdog:bug_lock` is set for a real bug on api-watchdog, that lock persists through cf-support rollback because it's product-specific not cf-support-specific).
- **Family round-4**: this runbook was added per Horizon's round-4 conditional-sign-off requirement (2026-05-27).

## Versioning

This runbook ships with cf-support v0.1.0+ as `ROLLBACK.md` at repo root. Updates to the runbook land as patch releases of cf-support (e.g., v0.1.1 if just runbook changes; otherwise bundled with the relevant code release).
