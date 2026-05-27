"""One-tier bug-or-not-bug triage skeleton."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Literal


TriageState = Literal["untriaged", "bug", "not_bug", "spam"]


@dataclass(slots=True)
class TriageDecision:
    state: TriageState
    confidence: float
    reasoning: str
    owner_confirmed_bug: bool | None = None


def classify_event(event: Dict[str, Any]) -> TriageDecision:
    raise NotImplementedError(
        "product-triage not implemented yet (spec §3.2, §4, §7)"
    )
