"""GitHub webhook intake for the Phase 0 support spine."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
from typing import Any

from lib.storage import new_event_id, utcnow_iso
from lib.thread_id import extract_explicit_references, thread_id_from_github


@dataclass(slots=True)
class GitHubWebhookEvent:
    event_name: str
    delivery_id: str
    payload: dict[str, Any]


def verify_signature(signature_header: str, raw_body: bytes, secret: str) -> bool:
    if not secret:
        return True
    if not signature_header.startswith("sha256="):
        return False
    expected = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    actual = signature_header.split("=", 1)[1]
    return hmac.compare_digest(expected, actual)


def _base_event(
    *,
    event: GitHubWebhookEvent,
    repo_full_name: str,
    issue_number: int,
    subject: str,
    body: str,
    user_handle: str,
    received_at: str,
    channel_ref: str,
) -> dict[str, Any]:
    references = extract_explicit_references(body, "github", repo_full_name=repo_full_name)
    thread_id = thread_id_from_github(repo_full_name, issue_number)
    suggested_link = next((ref for ref in references if ref != thread_id), None)
    return {
        "event_id": new_event_id(),
        "delivery_id": event.delivery_id,
        "thread_id": thread_id,
        "channel": "github",
        "channel_ref": channel_ref,
        "product": repo_full_name.split("/", 1)[1],
        "user_handle": user_handle,
        "user_id": f"github:{user_handle}",
        "subject": subject,
        "body": body,
        "received_at": received_at,
        "is_first_contact": False,
        "triage_state": "untriaged",
        "triage_confidence": 0.0,
        "triage_reasoning": "",
        "owner_confirmed_bug": None,
        "suggested_link_thread_id": suggested_link,
        "suggestion_confidence": 1.0 if suggested_link else 0.0,
        "needs_owner_review": bool(suggested_link),
        "assigned_owner": "",
        "owner_notified_at": "",
        "blocked_on_facilitator": False,
        "blocked_on_facilitator_reason": None,
        "blocked_on_facilitator_since": None,
        "resolved_at": "",
    }


def build_intake_event(event: GitHubWebhookEvent) -> dict[str, Any]:
    payload = event.payload
    repository = payload.get("repository") or {}
    repo_full_name = repository.get("full_name")
    if not repo_full_name:
        raise ValueError("GitHub payload missing repository.full_name")

    if event.event_name == "issues":
        issue = payload.get("issue") or {}
        action = payload.get("action")
        if action not in {"opened", "edited", "reopened"}:
            raise ValueError(f"unsupported issues action: {action}")
        return _base_event(
            event=event,
            repo_full_name=repo_full_name,
            issue_number=int(issue["number"]),
            subject=f"Issue #{issue['number']}: {issue.get('title') or '(no title)'}",
            body=issue.get("body") or "",
            user_handle=(issue.get("user") or {}).get("login", "unknown"),
            received_at=issue.get("created_at") or utcnow_iso(),
            channel_ref=f"{repo_full_name}#{issue['number']}",
        )

    if event.event_name == "issue_comment":
        issue = payload.get("issue") or {}
        comment = payload.get("comment") or {}
        action = payload.get("action")
        if action not in {"created", "edited"}:
            raise ValueError(f"unsupported issue_comment action: {action}")
        return _base_event(
            event=event,
            repo_full_name=repo_full_name,
            issue_number=int(issue["number"]),
            subject=f"Comment on issue #{issue['number']}: {issue.get('title') or '(no title)'}",
            body=comment.get("body") or "",
            user_handle=(comment.get("user") or {}).get("login", "unknown"),
            received_at=comment.get("created_at") or utcnow_iso(),
            channel_ref=f"{repo_full_name}#{issue['number']}",
        )

    raise ValueError(f"unsupported GitHub event: {event.event_name}")
