"""Runtime configuration for Phase 0 support spine."""

from __future__ import annotations

import json
import os
import shutil


DEFAULT_OWNER_MAP = {
    "claude-code-api-watchdog": "conductor",
    "mcp-reconnect": "conductor",
    "claude-code-fleet-notify": "conductor",
    "claude-code-fleet-orchestrator": "conductor",
    "claude-code-fleet-cockpit-template": "conductor",
    "claude-code-fleet-support": "conductor",
}


def redis_host() -> str:
    return os.environ.get("REDIS_HOST", "127.0.0.1")


def redis_port() -> int:
    return int(os.environ.get("REDIS_PORT", "6379"))


def github_webhook_secret() -> str:
    return os.environ.get("CF_SUPPORT_GITHUB_WEBHOOK_SECRET", "")


def notify_bin() -> str:
    return os.environ.get("CF_SUPPORT_NOTIFY_BIN", "/usr/local/bin/taey-notify")


def claude_bin() -> str:
    explicit = os.environ.get("CF_SUPPORT_CLAUDE_BIN", "").strip()
    if explicit:
        return explicit
    resolved = shutil.which("claude")
    if resolved:
        return resolved
    return "/home/mira/.npm-global/bin/claude"


def claude_model() -> str:
    return os.environ.get("CF_SUPPORT_CLAUDE_MODEL", "haiku")


def owner_map() -> dict[str, str]:
    raw = os.environ.get("CF_SUPPORT_OWNER_MAP_JSON", "").strip()
    if not raw:
        return dict(DEFAULT_OWNER_MAP)
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("CF_SUPPORT_OWNER_MAP_JSON must decode to an object")
    return {str(key): str(value) for key, value in parsed.items()}
