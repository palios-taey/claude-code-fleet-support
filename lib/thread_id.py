"""Deterministic thread identity helpers."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


_GITHUB_ISSUE_RE = re.compile(
    r"github\\.com/(?P<org>[^/]+)/(?P<repo>[^/]+)/issues/(?P<number>\\d+)"
)
_CHATWOOT_CONV_RE = re.compile(r"chatwoot[^\\s]*/(?:app/)?accounts/\\d+/conversations/(?P<id>\\d+)")


def build_thread_id(platform: str, platform_unique_id: str) -> str:
    platform_key = platform.strip().lower()
    unique_key = platform_unique_id.strip()
    if not platform_key or not unique_key:
        raise ValueError("platform and platform_unique_id are required")
    return f"{platform_key}:{unique_key}"


def extract_explicit_links(text: str) -> list[str]:
    links: list[str] = []
    for match in _GITHUB_ISSUE_RE.finditer(text):
        links.append(
            build_thread_id(
                "github",
                f"{match.group('org')}/{match.group('repo')}#{match.group('number')}",
            )
        )
    for match in _CHATWOOT_CONV_RE.finditer(text):
        links.append(build_thread_id("chatwoot", f"conv:{match.group('id')}"))
    return links


@dataclass(slots=True)
class ThreadLinkSuggestion:
    thread_id: str
    suggested_link_thread_id: str
    suggestion_confidence: float
    needs_owner_review: bool = True


def dedupe_links(links: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for link in links:
        if link in seen:
            continue
        seen.add(link)
        ordered.append(link)
    return ordered
