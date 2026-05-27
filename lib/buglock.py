"""Bug-lock helpers."""

from __future__ import annotations

from dataclasses import dataclass

from lib.storage import redis_client, utcnow_iso


@dataclass(slots=True)
class BugLockKeys:
    active: str
    reason: str
    owner: str
    opened: str


def bug_lock_keys(product_id: str) -> BugLockKeys:
    prefix = f"support:product:{product_id}:bug_lock"
    return BugLockKeys(
        active=prefix,
        reason=f"{prefix}_reason",
        owner=f"{prefix}_owner",
        opened=f"{prefix}_opened",
    )


def open_bug_lock(product_id: str, reason: str, owner: str) -> None:
    keys = bug_lock_keys(product_id)
    client = redis_client()
    client.mset(
        {
            keys.active: "true",
            keys.reason: reason,
            keys.owner: owner,
            keys.opened: utcnow_iso(),
        }
    )


def clear_bug_lock(product_id: str) -> None:
    keys = bug_lock_keys(product_id)
    client = redis_client()
    client.delete(keys.active, keys.reason, keys.owner, keys.opened)


def should_open_bug_lock(*, triage_state: str, triage_confidence: float, owner_confirmed_bug: bool | None) -> bool:
    return triage_state == "bug" and (triage_confidence >= 0.90 or owner_confirmed_bug is True)
