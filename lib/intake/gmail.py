"""Gmail MCP intake skeleton."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(slots=True)
class GmailMessage:
    message_id: str
    thread_id: str
    payload: Dict[str, Any]


class GmailIntakeAdapter:
    def poll(self) -> list[GmailMessage]:
        raise NotImplementedError(
            "product-gmail-intake not implemented yet (spec §1, §2, §6)"
        )


def build_intake_event(message: GmailMessage) -> Dict[str, Any]:
    raise NotImplementedError(
        "product-gmail-intake not implemented yet (spec §2, §6)"
    )
