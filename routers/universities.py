from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.program import Program
from models.university import University
from models.user import User
from schemas.program import ProgramListResponse, ProgramPublicResponse
from schemas.university import (
    UniversityCreate,
    UniversityListResponse,
    UniversityResponse,
    UniversityUpdate,
)
from utils.dependencies import get_current_admin

router = APIRouter(prefix="/universities", tags=["Universities"])

_UNIVERSITY_I18N = ["name", "description"]


def _localize_university(u: University, lang: str) -> University:
    """Apply lang-specific fields to name/description."""
    if lang in ("en", "tg"):
        suffix = lang
        for field in _UNIVERSITY_I18N:
            localized = getattr(u, f"{field}_{suffix}", None)
            if localized:
                setattr(u, field + "_ru", localized)  # not mutating, just display shim
    return u


# ── Public endpoints ──────────────────────────────────────────────────────────

@router.get("", response_model=UniversityListResponse)
async def list_universities(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    country_slug: Optional[str] = None,
    lang: str = Query(default="ru"),
    db: AsyncSession = Depends(get_db),
):
    """List all universities with optional country filter."""
    base = select(University)
    if country_slug:
        base = base.where(University.country_slug == country_slug)
    total = (await db.execute(select(func.count()).select_from(base.subquery()))).scalar_one()
    result = await db.execute(
        base.order_by(University.name_ru).offset((page - 1) * size).limit(size)
    )
    universities = list(result.scalars().all())
    return UniversityListResponse(items=universities, total=total, page=page, size=size)


@router.get("/{slug}", response_model=UniversityResponse)
async def get_university(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """Get a single university by slug."""
    result = await db.execute(select(University).where(University.slug == slug))
    university = result.scalar_one_or_none()
    if not university:
        raise HTTPException(status_code=404, detail="University not found")
    return university


@router.get("/{slug}/programs", response_model=ProgramListResponse)
async def get_university_programs(
    slug: str,
    page: int = Query(1, ge=1),
    size: int = Query(12, ge=1, le=100),
    lang: str = Query(default="ru"),
    db: AsyncSession = Depends(get_db),
):
    """List published programs belonging to a university."""
    uni = (await db.execute(select(University).where(University.slug == slug))).scalar_one_or_none()
    if not uni:
        raise HTTPException(status_code=404, detail="University not found")
    base = select(Program).where(
        Program.university_id == uni.id,
        Program.is_published.is_(True),
    )
    total = (await db.execute(select(func.count()).select_from(base.subquery()))).scalar_one()
    result = await db.execute(
        base.order_by(Program.created_at.desc()).offset((page - 1) * size).limit(size)
    )
    programs = list(result.scalars().all())
    return ProgramListResponse(items=programs, total=total, page=page, size=size)


# ── Admin endpoints ───────────────────────────────────────────────────────────

@router.post("", response_model=UniversityResponse, status_code=status.HTTP_201_CREATED)
async def create_university(
    payload: UniversityCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """[Admin] Create a new university."""
    existing = (
        await db.execute(select(University).where(University.slug == payload.slug))
    ).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Slug already exists")
    university = University(**payload.model_dump())
    db.add(university)
    await db.flush()
    await db.refresh(university)
    return university


@router.patch("/{slug}", response_model=UniversityResponse)
async def update_university(
    slug: str,
    payload: UniversityUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """[Admin] Partially update a university."""
    result = await db.execute(select(University).where(University.slug == slug))
    university = result.scalar_one_or_none()
    if not university:
        raise HTTPException(status_code=404, detail="University not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(university, field, value)
    await db.flush()
    await db.refresh(university)
    return university


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_university(
    slug: str,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """[Admin] Delete a university (does not delete linked programs)."""
    result = await db.execute(select(University).where(University.slug == slug))
    university = result.scalar_one_or_none()
    if not university:
        raise HTTPException(status_code=404, detail="University not found")
    await db.delete(university)
