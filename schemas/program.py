from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from models.program import ProgramCategory, ProgramLevel


# ── Base ──────────────────────────────────────────────────────────────────────

class ProgramBase(BaseModel):
    title: str
    category: ProgramCategory
    level: ProgramLevel = ProgramLevel.BEGINNER
    country_slug: Optional[str] = None
    short_description: str
    description: str
    full_description: Optional[str] = None
    duration_months: Optional[int] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    language_requirement: Optional[str] = None
    salary_range: Optional[str] = None
    cost: Optional[str] = None
    documents: Optional[str] = None
    deadline: Optional[str] = None
    official_url: Optional[str] = None
    residence_permit: bool = False
    pros: Optional[str] = None
    cons: Optional[str] = None
    career_opportunities: Optional[str] = None
    cover_image_url: Optional[str] = None


# ── Create / Update ───────────────────────────────────────────────────────────

class ProgramCreate(ProgramBase):
    slug: str
    is_published: bool = False
    # Optional translations
    title_en: Optional[str] = None
    title_tg: Optional[str] = None
    short_description_en: Optional[str] = None
    short_description_tg: Optional[str] = None
    description_en: Optional[str] = None
    description_tg: Optional[str] = None
    full_description_en: Optional[str] = None
    full_description_tg: Optional[str] = None


class ProgramUpdate(BaseModel):
    title: Optional[str] = None
    title_en: Optional[str] = None
    title_tg: Optional[str] = None
    category: Optional[ProgramCategory] = None
    level: Optional[ProgramLevel] = None
    country_slug: Optional[str] = None
    short_description: Optional[str] = None
    short_description_en: Optional[str] = None
    short_description_tg: Optional[str] = None
    description: Optional[str] = None
    description_en: Optional[str] = None
    description_tg: Optional[str] = None
    full_description: Optional[str] = None
    full_description_en: Optional[str] = None
    full_description_tg: Optional[str] = None
    duration_months: Optional[int] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    language_requirement: Optional[str] = None
    salary_range: Optional[str] = None
    cost: Optional[str] = None
    documents: Optional[str] = None
    deadline: Optional[str] = None
    official_url: Optional[str] = None
    residence_permit: Optional[bool] = None
    pros: Optional[str] = None
    cons: Optional[str] = None
    career_opportunities: Optional[str] = None
    cover_image_url: Optional[str] = None
    is_published: Optional[bool] = None


# ── Public response (visible without auth) ────────────────────────────────────

class ProgramPublicResponse(BaseModel):
    """Program info shown on the public listing page."""
    id: int
    slug: str
    country_slug: Optional[str] = None
    title: str
    category: ProgramCategory
    level: ProgramLevel
    short_description: str
    duration_months: Optional[int] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    language_requirement: Optional[str] = None
    salary_range: Optional[str] = None
    deadline: Optional[str] = None
    residence_permit: bool = False
    pros: Optional[str] = None
    cost: Optional[str] = None
    cover_image_url: Optional[str] = None
    is_published: bool
    views_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Full response (visible after auth) ────────────────────────────────────────

class ProgramResponse(ProgramBase):
    """Full program info shown to authenticated users."""
    id: int
    slug: str
    is_published: bool
    views_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProgramListResponse(BaseModel):
    items: list[ProgramPublicResponse]
    total: int
    page: int
    size: int
