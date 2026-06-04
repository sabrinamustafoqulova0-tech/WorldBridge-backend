from typing import Optional

from pydantic import BaseModel


class CountryResponse(BaseModel):
    slug: str
    # Raw multilingual fields (always returned for backward compat)
    name_ru: str
    name_en: str
    name_tg: Optional[str] = None
    flag_emoji: str
    description_ru: str
    description_en: str
    description_tg: Optional[str] = None
    # Localised flat fields — filled by the router via localize()
    name: Optional[str] = None
    description: Optional[str] = None
    capital: str
    population: str
    languages: str
    currency: str
    region: str
    map_x: float
    map_y: float

    model_config = {"from_attributes": True}


class CountryListResponse(BaseModel):
    items: list[CountryResponse]
    total: int
