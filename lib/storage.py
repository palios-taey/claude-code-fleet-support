"""Redis-backed Phase 0 storage."""

from __future__ import annotations

import json
from datetime import datetime, timezone
import uuid

import redis

from lib import config


SUPPORT_INBOX_KEY = "taey:support:inbox"


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def redis_client() -> redis.Redis:
    return redis.Redis(
        host=config.redis_host(),
        port=config.redis_port(),
        decode_responses=True,
    )


def event_key(event_id: str) -> str:
    return f"taey:support:event:{event_id}"


def thread_key(thread_id: str) -> str:
    return f"taey:support:thread:{thread_id}"


def thread_events_key(thread_id: str) -> str:
    return f"taey:support:thread:{thread_id}:events"


def new_event_id() -> str:
    return f"evt_{uuid.uuid4().hex}"


def _redis_value(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.6f}".rstrip("0").rstrip(".")
    return str(value)


def write_event(event: dict[str, object], client: redis.Redis | None = None) -> dict[str, object]:
    r = client or redis_client()
    stored = dict(event)
    thread_id = str(stored["thread_id"])
    thread_hash_key = thread_key(thread_id)
    stored["is_first_contact"] = not r.exists(thread_hash_key)
    event_hash = {key: _redis_value(value) for key, value in stored.items()}
    now = utcnow_iso()

    pipe = r.pipeline()
    pipe.hset(event_key(str(stored["event_id"])), mapping=event_hash)
    pipe.hset(
        thread_hash_key,
        mapping={
            "thread_id": thread_id,
            "channel": _redis_value(stored["channel"]),
            "product": _redis_value(stored["product"]),
            "channel_ref": _redis_value(stored["channel_ref"]),
            "user_handle": _redis_value(stored["user_handle"]),
            "last_event_id": _redis_value(stored["event_id"]),
            "updated_at": now,
        },
    )
    pipe.rpush(thread_events_key(thread_id), str(stored["event_id"]))
    pipe.lpush(SUPPORT_INBOX_KEY, str(stored["event_id"]))
    pipe.execute()
    return stored


def read_event(event_id: str, client: redis.Redis | None = None) -> dict[str, str]:
    r = client or redis_client()
    event = r.hgetall(event_key(event_id))
    if not event:
        raise KeyError(f"support event missing: {event_id}")
    return event


def update_event_fields(
    event_id: str,
    fields: dict[str, object],
    client: redis.Redis | None = None,
) -> None:
    r = client or redis_client()
    mapping = {key: _redis_value(value) for key, value in fields.items()}
    r.hset(event_key(event_id), mapping=mapping)


def queue_snapshot(client: redis.Redis | None = None) -> list[str]:
    r = client or redis_client()
    return list(r.lrange(SUPPORT_INBOX_KEY, 0, -1))


def event_snapshot(event_id: str, client: redis.Redis | None = None) -> str:
    return json.dumps(read_event(event_id, client=client), indent=2, sort_keys=True)
