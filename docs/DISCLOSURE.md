# Disclosure

## Standard Disclosure Text [Observed]

This repository's first-contact disclosure text is stored in `lib/disclosure.py:STANDARD_DISCLOSURE` and is reproduced verbatim below:

> You're talking to an AI agent (not a person reading in real time).
>
> Here's what this means in practice:
>
> — I read your message immediately and can ask clarifying questions, collect logs, classify whether this is a bug, route it to the product owner, and open or update a public GitHub issue on your behalf.
>
> — I do not have authority to make irreversible decisions for you (deploy fixes you didn't ask for, change pricing, share your data, commit to legal obligations). For anything in those categories I'll surface the question to a human facilitator and tell you that's happening.
>
> — My memory of our conversation is what's in this thread plus the public issue record. I don't have access to your account history elsewhere.
>
> — Acknowledgment is fast (target ~15 min when our systems are healthy; we publish a status indicator). Resolution proceeds continuously until the issue is closed — we don't promise a fix-by clock because that depends on the bug.
>
> — Don't paste secrets, tokens, private keys, or confidential logs here. For security vulnerability reports, see SECURITY.md for the private reporting path.

## Rationale By Clause

- [Observed] "AI agent (not a person reading in real time)" prevents false implication of live human review.
- [Observed] The action list limits the system to triage, routing, collection, and issue-record work.
- [Observed] The irreversible-decision clause bounds authority and says human facilitation will be surfaced explicitly.
- [Observed] The memory clause avoids implying broader account memory than the architecture implements.
- [Observed] The acknowledgment clause is target-shaped, not guarantee-shaped.
- [Observed] The no-fix-by-clock clause preserves cannot-lie discipline around resolution timing.
- [Observed] The secrets warning pushes vulnerability and private material away from normal support channels.

## Current Skeleton Status [Observed]

- [Observed] The text is implemented as a constant.
- [Observed] Automatic first-contact insertion logic is limited to a simple prefix helper in this skeleton.
- [Observed] Full product behavior is deferred to task `product-disclosure`.
