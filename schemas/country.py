from pydantic import BaseModel


class CountryResponse(BaseModel):
    slug: str
    name_ru: str
    name_en: str
    flag_emoji: str
    description_ru: str
    description_en: str
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
