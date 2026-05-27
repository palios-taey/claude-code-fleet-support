"""Support event router skeleton."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(slots=True)
class RoutedEvent:
    event_id: str
    assigned_owner: str
    notification_body: str


def route_event(event: Dict[str, Any]) -> RoutedEvent:
    raise NotImplementedError(
        "product-router not implemented yet (spec §1, §6)"
    )
