"""Chatwoot intake adapter skeleton."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(slots=True)
class ChatwootConfig:
    base_url: str
    api_token: str
    account_id: str


class ChatwootClient:
    """Chatwoot API client skeleton."""

    def __init__(self, config: ChatwootConfig) -> None:
        self.config = config

    def list_new_conversations(self) -> list[Dict[str, Any]]:
        raise NotImplementedError(
            "product-chatwoot-intake not implemented yet (spec §1, §2, §9)"
        )

    def post_reply(self, conversation_id: str, body: str) -> Dict[str, Any]:
        raise NotImplementedError(
            "product-chatwoot-intake not implemented yet (spec §1, §5, §6, §9)"
        )


def build_intake_event(conversation: Dict[str, Any]) -> Dict[str, Any]:
    raise NotImplementedError(
        "product-chatwoot-intake not implemented yet (spec §2, §5, §6)"
    )
