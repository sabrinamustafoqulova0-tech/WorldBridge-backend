from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UniversityBase(BaseModel):
    slug: str
    name_ru: str
    name_en: Optional[str] = None
    name_tg: Optional[str] = None
    country_slug: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    website_url: Optional[str] = None
    logo_url: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    description_tg: Optional[str] = None


class UniversityCreate(UniversityBase):
    pass


class UniversityUpdate(BaseModel):
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    name_tg: Optional[str] = None
    country_slug: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    website_url: Optional[str] = None
    logo_url: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    description_tg: Optional[str] = None


class UniversityResponse(UniversityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UniversityListResponse(BaseModel):
    items: list[UniversityResponse]
    total: int
    page: int
    size: int
