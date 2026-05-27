"""X bridge intake skeleton."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(slots=True)
class XBridgeEvent:
    source_url: str
    payload: Dict[str, Any]


class XBridgeAdapter:
    def poll(self) -> list[XBridgeEvent]:
        raise NotImplementedError(
            "foundation-cf-support-skeleton placeholder only; X bridge implementation follows spec §1, §2.1, §12 Q6"
        )


def build_intake_event(event: XBridgeEvent) -> Dict[str, Any]:
    raise NotImplementedError(
        "foundation-cf-support-skeleton placeholder only; X bridge implementation follows spec §1, §2.1, §12 Q6"
    )
