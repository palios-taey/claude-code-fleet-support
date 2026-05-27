"""Bug-lock skeleton."""

from __future__ import annotations

from dataclasses import dataclass


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
    raise NotImplementedError(
        "product-buglock not implemented yet (spec §3, §3.2)"
    )


def clear_bug_lock(product_id: str) -> None:
    raise NotImplementedError(
        "product-buglock not implemented yet (spec §3)"
    )
