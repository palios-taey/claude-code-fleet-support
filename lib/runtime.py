"""Phase 0 runtime: FastAPI webhook intake plus queue consumer."""

from __future__ import annotations

import json
import threading
import traceback
from typing import Any

from fastapi import FastAPI, HTTPException, Request

from lib import config
from lib.buglock import open_bug_lock, should_open_bug_lock
from lib.intake.github_webhook import GitHubWebhookEvent, build_intake_event, verify_signature
from lib.router import route_event
from lib.storage import SUPPORT_INBOX_KEY, read_event, redis_client, update_event_fields, utcnow_iso, write_event
from lib.triage import classify_event


class SupportRuntime:
    def __init__(self) -> None:
        self.redis = redis_client()
        self.last_error = ""

    def ingest_github_event(
        self,
        *,
        event_name: str,
        delivery_id: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        intake = build_intake_event(
            GitHubWebhookEvent(
                event_name=event_name,
                delivery_id=delivery_id,
                payload=payload,
            )
        )
        return write_event(intake, client=self.redis)

    def process_next_event(self, timeout: int = 1) -> bool:
        item = self.redis.brpop(SUPPORT_INBOX_KEY, timeout=timeout)
        if not item:
            return False
        _, event_id = item
        event = read_event(event_id, client=self.redis)
        decision = classify_event(event)
        update_event_fields(
            event_id,
            {
                "triage_state": decision.state,
                "triage_confidence": decision.confidence,
                "triage_reasoning": decision.reasoning,
                "owner_confirmed_bug": decision.owner_confirmed_bug,
            },
            client=self.redis,
        )
        event.update(
            {
                "triage_state": decision.state,
                "triage_confidence": str(decision.confidence),
                "triage_reasoning": decision.reasoning,
                "owner_confirmed_bug": "null" if decision.owner_confirmed_bug is None else str(decision.owner_confirmed_bug).lower(),
            }
        )

        if should_open_bug_lock(
            triage_state=decision.state,
            triage_confidence=decision.confidence,
            owner_confirmed_bug=decision.owner_confirmed_bug,
        ):
            open_bug_lock(
                str(event["product"]),
                f"{event_id} - {decision.reasoning}",
                "cf-support",
            )

        if decision.state == "spam":
            return True

        routed = route_event(event)
        update_event_fields(
            event_id,
            {
                "assigned_owner": routed.assigned_owner,
                "owner_notified_at": utcnow_iso(),
            },
            client=self.redis,
        )
        return True


def create_app(runtime: SupportRuntime | None = None) -> FastAPI:
    app = FastAPI(title="claude-code-fleet-support", version="0.1.0")
    service = runtime or SupportRuntime()

    @app.get("/healthz")
    def healthz() -> dict[str, object]:
        return {"ok": not bool(service.last_error), "last_error": service.last_error}

    @app.post("/github/webhook")
    async def github_webhook(request: Request) -> dict[str, Any]:
        event_name = request.headers.get("X-GitHub-Event", "")
        delivery_id = request.headers.get("X-GitHub-Delivery", "")
        signature = request.headers.get("X-Hub-Signature-256", "")
        raw_body = await request.body()
        if not verify_signature(signature, raw_body, config.github_webhook_secret()):
            raise HTTPException(status_code=401, detail="invalid signature")
        if event_name == "ping":
            payload = json.loads(raw_body.decode("utf-8"))
            return {"ok": True, "ping": payload.get("zen", "")}
        try:
            payload = json.loads(raw_body.decode("utf-8"))
            stored = service.ingest_github_event(
                event_name=event_name,
                delivery_id=delivery_id,
                payload=payload,
            )
            return {"ok": True, "event_id": stored["event_id"], "thread_id": stored["thread_id"]}
        except ValueError as exc:
            raise HTTPException(status_code=202, detail=str(exc)) from exc

    return app


def run_consumer(stop_event: threading.Event, runtime: SupportRuntime | None = None) -> None:
    service = runtime or SupportRuntime()
    while not stop_event.is_set():
        try:
            service.process_next_event(timeout=1)
        except Exception as exc:
            service.last_error = str(exc)
            traceback.print_exc()
            stop_event.set()
            raise
