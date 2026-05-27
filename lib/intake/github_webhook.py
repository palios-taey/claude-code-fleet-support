"""GitHub webhook intake skeleton."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(slots=True)
class GitHubWebhookEvent:
    event_name: str
    delivery_id: str
    payload: Dict[str, Any]


def verify_signature(signature_header: str, raw_body: bytes, secret: str) -> bool:
    raise NotImplementedError(
        "product-github-webhook not implemented yet (spec §1, §2, §6)"
    )


def build_intake_event(event: GitHubWebhookEvent) -> Dict[str, Any]:
    raise NotImplementedError(
        "product-github-webhook not implemented yet (spec §2, §6)"
    )
