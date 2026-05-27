# Chatwoot Install

## Purpose [Observed]

This document is the adopter-facing install playbook for running Chatwoot as the conversation record layer for `claude-code-fleet-support`.

## Separation [Observed]

- [Observed] This document is for adopters of the standalone product.
- [Observed] The PALIOS-TAEY fleet's own Chatwoot operational instance lives in `the-conductor`, not in this repository.

## Required Stack [Observed]

- Postgres
- Redis
- Chatwoot Rails app
- Sidekiq
- Reverse proxy / TLS termination

This matches architecture spec §9.

## Expected Integration Shape [Observed]

1. Deploy Chatwoot self-hosted
2. Generate API credentials for the intake adapter
3. Point `lib/intake/chatwoot.py` at the Chatwoot REST API
4. Route first-contact replies through the disclosure layer
5. Keep product routing and bug-lock logic outside Chatwoot itself

## Not In This Skeleton [Observed]

- [Observed] No turnkey installer script ships in `v0.0.2`.
- [Observed] No Docker Compose bundle ships in `v0.0.2`.
- [Observed] The adapter implementation itself is deferred to task `product-chatwoot-intake`.

## Adopter TODOs [Observed]

- Publish your support mailbox
- Decide which channels to enable at launch
- Publish your security reporting path
- Configure your owner map and status-indicator URL

## Operational Unknowns [Unknown]

- Long-term maintenance overhead for adopters relative to simpler inbox tools
- Whether an adopter needs the web widget at launch or only email plus GitHub
