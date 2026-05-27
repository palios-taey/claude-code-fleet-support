"""Support event router."""

from __future__ import annotations

from dataclasses import dataclass
import subprocess

from lib import config


@dataclass(slots=True)
class RoutedEvent:
    event_id: str
    assigned_owner: str
    notification_body: str


def _owner_for(product: str) -> str:
    return config.owner_map().get(product, "conductor")


def _build_notification(event: dict[str, str], owner: str) -> str:
    excerpt = (event.get("body") or "").strip().replace("\r", "")
    if len(excerpt) > 500:
        excerpt = excerpt[:500] + "..."
    disclosure = "prepend STANDARD_DISCLOSURE on first external response" if event.get("is_first_contact") == "true" else "thread already exists"
    return (
        f"SUPPORT EVENT {event['event_id']} for {owner}\n"
        f"product: {event.get('product', '')}\n"
        f"thread: {event.get('thread_id', '')}\n"
        f"channel_ref: {event.get('channel_ref', '')}\n"
        f"triage: {event.get('triage_state', '')} ({event.get('triage_confidence', '')})\n"
        f"reasoning: {event.get('triage_reasoning', '')}\n"
        f"disclosure: {disclosure}\n"
        f"user: {event.get('user_handle', '')}\n"
        f"subject: {event.get('subject', '')}\n"
        f"body:\n{excerpt}"
    )


def route_event(event: dict[str, str]) -> RoutedEvent:
    owner = _owner_for(event.get("product", ""))
    body = _build_notification(event, owner)
    result = subprocess.run(
        [
            config.notify_bin(),
            owner,
            body,
            "--type",
            "directive",
            "--priority",
            "high",
            "--from",
            "cf-support",
        ],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"taey-notify failed for {owner}: {result.stderr.strip() or result.stdout.strip()}"
        )
    return RoutedEvent(
        event_id=event["event_id"],
        assigned_owner=owner,
        notification_body=body,
    )
