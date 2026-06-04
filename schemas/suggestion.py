import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator

from models.program_suggestion import SuggestionStatus


class SuggestionCreate(BaseModel):
    submitter_name: str
    submitter_email: EmailStr
    submitter_phone: str
    program_title: str
    country: str
    description: str
    official_url: Optional[str] = None
    extra_info: Optional[str] = None

    @field_validator("submitter_name")
    @classmethod
    def name_valid(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Имя должно содержать минимум 2 символа")
        if len(v) > 100:
            raise ValueError("Имя не должно превышать 100 символов")
        return v

    @field_validator("submitter_phone")
    @classmethod
    def phone_valid(cls, v: str) -> str:
        v = v.strip()
        if not re.match(r"^\+?[0-9\s\-\(\)]{7,30}$", v):
            raise ValueError("Неверный формат телефона")
        return v

    @field_validator("program_title")
    @classmethod
    def title_valid(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Название программы должно содержать минимум 3 символа")
        if len(v) > 255:
            raise ValueError("Название не должно превышать 255 символов")
        return v

    @field_validator("country")
    @classmethod
    def country_valid(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Укажите страну")
        if len(v) > 100:
            raise ValueError("Название страны не должно превышать 100 символов")
        return v

    @field_validator("description")
    @classmethod
    def description_valid(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 50:
            raise ValueError("Описание должно содержать минимум 50 символов")
        if len(v) > 5000:
            raise ValueError("Описание не должно превышать 5000 символов")
        return v

    @field_validator("official_url")
    @classmethod
    def url_valid(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return None
        v = v.strip()
        if not re.match(r"https?://", v):
            raise ValueError("URL должен начинаться с http:// или https://")
        if len(v) > 500:
            raise ValueError("URL не должен превышать 500 символов")
        return v

    @field_validator("extra_info")
    @classmethod
    def extra_info_valid(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return None
        v = v.strip()
        if len(v) > 2000:
            raise ValueError("Дополнительная информация не должна превышать 2000 символов")
        return v or None


class SuggestionReview(BaseModel):
    status: SuggestionStatus
    admin_comment: Optional[str] = None

    @field_validator("status")
    @classmethod
    def status_not_pending(cls, v: SuggestionStatus) -> SuggestionStatus:
        if v == SuggestionStatus.PENDING:
            raise ValueError("Нельзя установить статус 'pending' при модерации")
        return v


class SuggestionResponse(BaseModel):
    id: int
    submitter_name: str
    submitter_email: str
    submitter_phone: str
    program_title: str
    country: str
    description: str
    official_url: Optional[str] = None
    extra_info: Optional[str] = None
    status: SuggestionStatus
    admin_comment: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SuggestionListResponse(BaseModel):
    items: list[SuggestionResponse]
    total: int
    page: int
    size: int
    pending_count: int
