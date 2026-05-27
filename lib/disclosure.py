"""First-contact AI disclosure text."""

from __future__ import annotations


STANDARD_DISCLOSURE = """You're talking to an AI agent (not a person reading in real time).

Here's what this means in practice:

— I read your message immediately and can ask clarifying questions, collect logs, classify whether this is a bug, route it to the product owner, and open or update a public GitHub issue on your behalf.

— I do not have authority to make irreversible decisions for you (deploy fixes you didn't ask for, change pricing, share your data, commit to legal obligations). For anything in those categories I'll surface the question to a human facilitator and tell you that's happening.

— My memory of our conversation is what's in this thread plus the public issue record. I don't have access to your account history elsewhere.

— Acknowledgment is fast (target ~15 min when our systems are healthy; we publish a status indicator). Resolution proceeds continuously until the issue is closed — we don't promise a fix-by clock because that depends on the bug.

— Don't paste secrets, tokens, private keys, or confidential logs here. For security vulnerability reports, see SECURITY.md for the private reporting path."""


def prepend_disclosure(body: str, is_first_contact: bool) -> str:
    if not is_first_contact:
        return body
    if body.startswith(STANDARD_DISCLOSURE):
        return body
    return f"{STANDARD_DISCLOSURE}\n\n{body}"


def get_disclosure_for_first_contact() -> str:
    return STANDARD_DISCLOSURE
