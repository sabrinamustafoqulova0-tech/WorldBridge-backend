"""
scholarship_tracker.py — aggregates scholarships from public RSS feeds.

Strategy: fetch feed bytes with httpx (async), parse with feedparser (sync).
This keeps the service non-blocking without needing run_in_executor.
"""

import re
import time
from datetime import datetime, timezone
from typing import Optional

import feedparser
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.external_scholarship import ExternalScholarship, ScholarshipCategory

# ── Feed sources ──────────────────────────────────────────────────────────────

SOURCES = [
    {
        "name": "Opportunity Desk",
        "url":  "https://opportunitydesk.org/feed/",
    },
    {
        "name": "Scholarships365",
        "url":  "https://scholarships365.info/feed/",
    },
    {
        "name": "UN Jobs",
        "url":  "https://careers.un.org/lcruitment/shared/library/common/rss/feed.xml",
    },
]

# ── Classification helpers ────────────────────────────────────────────────────

_CATEGORY_KEYWORDS: dict[ScholarshipCategory, list[str]] = {
    ScholarshipCategory.FELLOWSHIP:  ["fellowship", "fellow"],
    ScholarshipCategory.INTERNSHIP:  ["internship", "intern", "trainee"],
    ScholarshipCategory.EXCHANGE:    ["exchange", "erasmus", "study abroad"],
    ScholarshipCategory.CONFERENCE:  ["conference", "summit", "workshop", "seminar"],
}

_COUNTRY_KEYWORDS: dict[str, list[str]] = {
    "Germany":     ["germany", "german", "deutschland", "daad"],
    "USA":         ["usa", "united states", " america", "american"],
    "UK":          ["uk", "united kingdom", "britain", "england", "british"],
    "Canada":      ["canada", "canadian"],
    "Australia":   ["australia", "australian"],
    "China":       ["china", "chinese"],
    "Japan":       ["japan", "japanese"],
    "France":      ["france", "french"],
    "Sweden":      ["sweden", "swedish"],
    "Norway":      ["norway", "norwegian"],
    "Turkey":      ["turkey", "turkish"],
    "Netherlands": ["netherlands", "dutch", "holland"],
    "Switzerland": ["switzerland", "swiss"],
    "Austria":     ["austria", "austrian"],
    "South Korea": ["south korea", "korean"],
    "Singapore":   ["singapore"],
    "Finland":     ["finland", "finnish"],
}

# Matches dates like: "31 December 2026", "Dec 31, 2026", "2026-12-31"
_DEADLINE_RE = re.compile(
    r"\b(\d{1,2}[\s\-/]\w+[\s\-/]\d{4}|\w+\s+\d{1,2},?\s*\d{4}|\d{4}-\d{2}-\d{2})\b",
    re.IGNORECASE,
)

_HTML_TAG_RE = re.compile(r"<[^>]+>")


def _strip_html(text: str) -> str:
    return _HTML_TAG_RE.sub("", text or "").strip()


def _detect_category(text: str) -> ScholarshipCategory:
    t = text.lower()
    for cat, keywords in _CATEGORY_KEYWORDS.items():
        if any(k in t for k in keywords):
            return cat
    return ScholarshipCategory.SCHOLARSHIP


def _detect_country(text: str) -> Optional[str]:
    t = text.lower()
    for country, keywords in _COUNTRY_KEYWORDS.items():
        if any(k in t for k in keywords):
            return country
    return None


def _extract_deadline(text: str) -> Optional[str]:
    m = _DEADLINE_RE.search(text)
    return m.group(0) if m else None


def _parse_published(entry) -> Optional[datetime]:
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        try:
            return datetime.fromtimestamp(time.mktime(entry.published_parsed), tz=timezone.utc)
        except (OSError, OverflowError):
            pass
    return None


# ── Sync logic ────────────────────────────────────────────────────────────────

async def sync_source(source: dict, db: AsyncSession) -> tuple[int, int]:
    """Fetch and upsert scholarships from one RSS source. Returns (inserted, updated)."""
    inserted = updated = 0
    try:
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            resp = await client.get(
                source["url"],
                headers={"User-Agent": "WorldBridge/1.0 (+https://worldbridge-frontend.netlify.app)"},
            )
            resp.raise_for_status()

        feed = feedparser.parse(resp.content)

        for entry in feed.entries:
            url = entry.get("link", "").strip()
            if not url:
                continue

            title    = (entry.get("title", "") or "")[:500].strip()
            desc     = _strip_html(entry.get("summary", "") or "")[:2000]
            combined = title + " " + desc

            existing = (
                await db.execute(
                    select(ExternalScholarship).where(ExternalScholarship.url == url)
                )
            ).scalar_one_or_none()

            if existing:
                existing.title        = title
                existing.description  = desc
                existing.deadline     = _extract_deadline(combined)
                existing.country      = _detect_country(combined)
                existing.category     = _detect_category(combined)
                existing.published_at = _parse_published(entry)
                updated += 1
            else:
                db.add(ExternalScholarship(
                    title=title,
                    description=desc,
                    url=url,
                    source=source["name"],
                    deadline=_extract_deadline(combined),
                    country=_detect_country(combined),
                    category=_detect_category(combined),
                    published_at=_parse_published(entry),
                    is_active=True,
                ))
                inserted += 1

        await db.flush()

    except Exception as exc:
        print(f"[scholarship_tracker] {source['name']} failed: {exc}")

    return inserted, updated


async def sync_all_sources(db: AsyncSession) -> dict:
    """Sync all RSS sources. Commits after all sources run. Returns summary."""
    results = {}
    for source in SOURCES:
        ins, upd = await sync_source(source, db)
        results[source["name"]] = {"inserted": ins, "updated": upd}
    await db.commit()
    return results
