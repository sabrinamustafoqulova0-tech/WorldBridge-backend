from pydantic import BaseModel


class FAQResponse(BaseModel):
    id: int
    country_slug: str
    question: str
    answer: str
    order: int

    model_config = {"from_attributes": True}


class FAQPublicResponse(BaseModel):
    """Only question visible to unauthenticated users — answer is hidden."""
    id: int
    country_slug: str
    question: str
    order: int

    model_config = {"from_attributes": True}
