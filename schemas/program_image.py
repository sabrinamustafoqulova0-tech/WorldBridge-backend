from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from models.program_image import ImageType


class ProgramImageCreate(BaseModel):
    url: str
    caption_ru: Optional[str] = None
    caption_en: Optional[str] = None
    image_type: Optional[ImageType] = None
    display_order: int = 0


class ProgramImageResponse(BaseModel):
    id: int
    program_id: int
    url: str
    caption_ru: Optional[str] = None
    caption_en: Optional[str] = None
    image_type: Optional[ImageType] = None
    display_order: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ProgramImageListResponse(BaseModel):
    items: list[ProgramImageResponse]
    total: int
