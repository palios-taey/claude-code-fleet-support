"""One-tier bug-or-not-bug triage."""

from __future__ import annotations

from dataclasses import dataclass
import json
import subprocess
from typing import Any, Literal

from lib import config


TriageState = Literal["untriaged", "bug", "not_bug", "spam"]


@dataclass(slots=True)
class TriageDecision:
    state: TriageState
    confidence: float
    reasoning: str
    owner_confirmed_bug: bool | None = None


def _prompt_for(event: dict[str, Any]) -> str:
    return f"""You are triaging a real support event for an AI support router.
Classify this support event as exactly one of: bug, not_bug, spam.

Rules:
- bug = reproducible product-behavior defect against the product's documented contract
- not_bug = question, feature request, docs feedback, philosophical/design discussion, unreproducible report
- spam = off-topic, promotional, or abusive
- Return JSON only with keys: state, confidence, reasoning
- confidence must be a float between 0 and 1
- reasoning must be brief and concrete
- Do not ask follow-up questions
- Do not restate the event
- This is a triage decision, not a code fix

Event:
product: {event.get("product", "")}
channel: {event.get("channel", "")}
subject: {event.get("subject", "")}
user: {event.get("user_handle", "")}
body:
{event.get("body", "")}
"""


def _extract_json(text: str) -> dict[str, Any]:
    stripped = text.strip()
    with_context: dict[str, Any] | None = None
    if stripped.startswith("{"):
        with_context = json.loads(stripped)
        if isinstance(with_context, dict) and "state" in with_context:
            return with_context
        nested = with_context.get("result") if isinstance(with_context, dict) else None
        if isinstance(nested, str):
            return _extract_json(nested)

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise RuntimeError(f"triage response did not contain JSON: {text!r}")
    return json.loads(text[start : end + 1])


def classify_event(event: dict[str, Any]) -> TriageDecision:
    command = [
        config.claude_bin(),
        "-p",
        "--model",
        config.claude_model(),
        "--output-format",
        "json",
        "--permission-mode",
        "bypassPermissions",
        _prompt_for(event),
    ]
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=90,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"triage command failed: {result.stderr.strip() or result.stdout.strip()}")

    payload = _extract_json(result.stdout.strip())
    state = payload.get("state")
    if state not in {"bug", "not_bug", "spam"}:
        raise RuntimeError(f"triage returned invalid state: {state!r}")

    confidence = float(payload.get("confidence"))
    reasoning = str(payload.get("reasoning") or "").strip()
    if not reasoning:
        raise RuntimeError("triage returned empty reasoning")

    return TriageDecision(
        state=state,
        confidence=max(0.0, min(1.0, confidence)),
        reasoning=reasoning,
        owner_confirmed_bug=None,
    )
