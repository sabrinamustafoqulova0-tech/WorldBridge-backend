from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from models.external_scholarship import ScholarshipCategory


class ScholarshipResponse(BaseModel):
    id:           int
    title:        str
    description:  Optional[str] = None
    deadline:     Optional[str] = None
    url:          str
    source:       str
    country:      Optional[str] = None
    category:     ScholarshipCategory
    published_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ScholarshipListResponse(BaseModel):
    items: list[ScholarshipResponse]
    total: int
    page:  int
    size:  int
