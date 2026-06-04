"""
routers/suggestions.py — User program suggestions + admin moderation.

Public:
  POST /suggestions          — submit a suggestion (no auth required)

Admin:
  GET  /suggestions/admin/all            — list all with filters + pagination
  GET  /suggestions/admin/pending-count  — badge count
  GET  /suggestions/admin/{id}           — detail view
  PATCH /suggestions/admin/{id}/review   — approve / reject
"""

import re
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.program import Program, ProgramCategory, ProgramLevel
from models.program_suggestion import ProgramSuggestion, SuggestionStatus
from models.user import User
from schemas.suggestion import (
    SuggestionCreate,
    SuggestionListResponse,
    SuggestionResponse,
    SuggestionReview,
)
from utils.dependencies import get_current_admin

router = APIRouter(prefix="/suggestions", tags=["Suggestions"])

# Simple in-memory rate-limit: {email: last_submit_time}
_rate_cache: dict[str, datetime] = {}
RATE_LIMIT_MINUTES = 10

# Map Russian country names (from the suggest form) → country_slug
_COUNTRY_NAME_TO_SLUG: dict[str, str] = {
    "германия": "de",
    "франция": "fr",
    "бельгия": "be",
    "швейцария": "ch",
    "австрия": "at",
    "польша": "pl",
    "чехия": "cz",
    "швеция": "se",
    "норвегия": "no",
    "финляндия": "fi",
    "китай": "cn",
    "канада": "ca",
    "сша": "us",
    "турция": "tr",
}


def _transliterate(text: str) -> str:
    table = {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e",
        "ё": "yo", "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k",
        "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r",
        "с": "s", "т": "t", "у": "u", "ф": "f", "х": "kh", "ц": "ts",
        "ч": "ch", "ш": "sh", "щ": "shch", "ъ": "", "ы": "y", "ь": "",
        "э": "e", "ю": "yu", "я": "ya", " ": "-",
    }
    result = text.lower()
    for ru, lat in table.items():
        result = result.replace(ru, lat)
    result = re.sub(r"[^a-z0-9-]", "", result)
    result = re.sub(r"-+", "-", result).strip("-")
    return result or "suggestion"


async def _make_unique_slug(base: str, db: AsyncSession) -> str:
    slug = base[:60]
    suffix = 1
    while True:
        existing = (await db.execute(select(Program).where(Program.slug == slug))).scalar_one_or_none()
        if not existing:
            return slug
        slug = f"{base[:55]}-{suffix}"
        suffix += 1


# ── Public endpoint ───────────────────────────────────────────────────────────

@router.post("", response_model=SuggestionResponse, status_code=status.HTTP_201_CREATED)
async def submit_suggestion(
    payload: SuggestionCreate,
    db: AsyncSession = Depends(get_db),
):
    """Submit a new program suggestion. No authentication required."""
    email_key = payload.submitter_email.lower()
    now = datetime.now(tz=timezone.utc)

    # Rate-limit: one submission per email per 10 minutes
    last = _rate_cache.get(email_key)
    if last and (now - last) < timedelta(minutes=RATE_LIMIT_MINUTES):
        wait = RATE_LIMIT_MINUTES - int((now - last).total_seconds() / 60)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Вы уже отправили предложение. Повторите через {wait} мин.",
        )

    suggestion = ProgramSuggestion(
        submitter_name=payload.submitter_name,
        submitter_email=email_key,
        submitter_phone=payload.submitter_phone,
        program_title=payload.program_title,
        country=payload.country,
        description=payload.description,
        official_url=payload.official_url,
        extra_info=payload.extra_info,
        status=SuggestionStatus.PENDING,
    )
    db.add(suggestion)
    await db.flush()
    await db.refresh(suggestion)

    _rate_cache[email_key] = now
    return suggestion


# ── Admin endpoints ───────────────────────────────────────────────────────────

@router.get("/admin/pending-count")
async def get_pending_count(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """[Admin] Count of pending suggestions (for badge)."""
    count = (
        await db.execute(
            select(func.count()).where(ProgramSuggestion.status == SuggestionStatus.PENDING)
        )
    ).scalar_one()
    return {"pending_count": count}


@router.get("/admin/all", response_model=SuggestionListResponse)
async def list_suggestions(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status_filter: SuggestionStatus | None = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """[Admin] List all suggestions with optional status filter."""
    base = select(ProgramSuggestion)
    if status_filter:
        base = base.where(ProgramSuggestion.status == status_filter)

    total = (await db.execute(select(func.count()).select_from(base.subquery()))).scalar_one()
    pending_count = (
        await db.execute(
            select(func.count()).where(ProgramSuggestion.status == SuggestionStatus.PENDING)
        )
    ).scalar_one()

    result = await db.execute(
        base.order_by(ProgramSuggestion.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
    )
    items = list(result.scalars().all())
    return SuggestionListResponse(
        items=items, total=total, page=page, size=size, pending_count=pending_count
    )


@router.get("/admin/{suggestion_id}", response_model=SuggestionResponse)
async def get_suggestion(
    suggestion_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """[Admin] Get a single suggestion by ID."""
    suggestion = (
        await db.execute(select(ProgramSuggestion).where(ProgramSuggestion.id == suggestion_id))
    ).scalar_one_or_none()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Предложение не найдено")
    return suggestion


@router.patch("/admin/{suggestion_id}/review", response_model=SuggestionResponse)
async def review_suggestion(
    suggestion_id: int,
    payload: SuggestionReview,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """[Admin] Approve or reject a suggestion.

    On approval a draft Program is automatically created from the suggestion data.
    """
    suggestion = (
        await db.execute(select(ProgramSuggestion).where(ProgramSuggestion.id == suggestion_id))
    ).scalar_one_or_none()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Предложение не найдено")

    if suggestion.status != SuggestionStatus.PENDING:
        raise HTTPException(status_code=400, detail="Предложение уже было рассмотрено")

    suggestion.status = payload.status
    suggestion.admin_comment = payload.admin_comment
    suggestion.reviewed_at = datetime.now(tz=timezone.utc)
    suggestion.reviewed_by_id = admin.id

    if payload.status == SuggestionStatus.APPROVED:
        base_slug = _transliterate(suggestion.program_title)
        slug = await _make_unique_slug(f"{base_slug}-s{suggestion.id}", db)
        short_desc = suggestion.description[:497] + "..." if len(suggestion.description) > 500 else suggestion.description
        country_slug = _COUNTRY_NAME_TO_SLUG.get(suggestion.country.lower().strip())

        program = Program(
            slug=slug,
            title=suggestion.program_title,
            category=ProgramCategory.STUDIUM,
            level=ProgramLevel.BEGINNER,
            short_description=short_desc,
            description=suggestion.description,
            official_url=suggestion.official_url,
            country_slug=country_slug,
            is_published=True,
        )
        db.add(program)

    await db.flush()
    await db.refresh(suggestion)
    return suggestion
