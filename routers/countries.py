from typing import Optional, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.country import Country
from models.faq import FAQ
from models.program import Program
from schemas.country import CountryListResponse, CountryResponse
from schemas.faq import FAQPublicResponse, FAQResponse
from schemas.program import ProgramListResponse, ProgramPublicResponse
from utils.dependencies import get_current_active_user_optional

router = APIRouter(prefix="/countries", tags=["Countries"])


@router.get("", response_model=CountryListResponse)
async def list_countries(db: AsyncSession = Depends(get_db)):
    """List all available countries."""
    result = await db.execute(select(Country).order_by(Country.name_en))
    countries = list(result.scalars().all())
    return CountryListResponse(items=countries, total=len(countries))


@router.get("/{slug}", response_model=CountryResponse)
async def get_country(slug: str, db: AsyncSession = Depends(get_db)):
    """Get country detail by slug."""
    result = await db.execute(select(Country).where(Country.slug == slug))
    country = result.scalar_one_or_none()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


@router.get("/{slug}/programs", response_model=ProgramListResponse)
async def get_country_programs(
    slug: str,
    page: int = 1,
    size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """Get published programs for a country. Returns public info for all users."""
    base = select(Program).where(
        Program.country_slug == slug,
        Program.is_published.is_(True),
    )
    from sqlalchemy import func, select as sel
    total = (await db.execute(sel(func.count()).select_from(base.subquery()))).scalar_one()
    result = await db.execute(
        base.order_by(Program.created_at.desc()).offset((page - 1) * size).limit(size)
    )
    programs = list(result.scalars().all())
    return ProgramListResponse(items=programs, total=total, page=page, size=size)


@router.get("/{slug}/faq")
async def get_country_faq(
    slug: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user_optional),
):
    """
    Get FAQ for a country.
    - Authenticated users: full question + answer
    - Unauthenticated users: question only (answer hidden)
    """
    result = await db.execute(
        select(FAQ)
        .where(FAQ.country_slug == slug)
        .order_by(FAQ.order)
    )
    faqs = list(result.scalars().all())

    if current_user:
        return [FAQResponse.model_validate(f) for f in faqs]
    return [FAQPublicResponse.model_validate(f) for f in faqs]
