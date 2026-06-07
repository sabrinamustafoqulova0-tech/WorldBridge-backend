import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class ScholarshipCategory(str, enum.Enum):
    SCHOLARSHIP = "SCHOLARSHIP"
    INTERNSHIP  = "INTERNSHIP"
    EXCHANGE    = "EXCHANGE"
    FELLOWSHIP  = "FELLOWSHIP"
    CONFERENCE  = "CONFERENCE"


class ExternalScholarship(Base):
    __tablename__ = "external_scholarships"

    id:           Mapped[int]                  = mapped_column(Integer, primary_key=True, index=True)
    title:        Mapped[str]                  = mapped_column(String(500), nullable=False)
    description:  Mapped[str | None]           = mapped_column(Text, nullable=True)
    deadline:     Mapped[str | None]           = mapped_column(String(100), nullable=True)
    url:          Mapped[str]                  = mapped_column(String(1000), unique=True, nullable=False, index=True)
    source:       Mapped[str]                  = mapped_column(String(100), nullable=False)
    country:      Mapped[str | None]           = mapped_column(String(100), nullable=True)
    category:     Mapped[ScholarshipCategory]  = mapped_column(
                      Enum(ScholarshipCategory, name="scholarshipcategory"),
                      default=ScholarshipCategory.SCHOLARSHIP, nullable=False)
    is_active:    Mapped[bool]                 = mapped_column(Boolean, default=True, nullable=False)
    published_at: Mapped[datetime | None]      = mapped_column(DateTime(timezone=True), nullable=True)
    created_at:   Mapped[datetime]             = mapped_column(DateTime(timezone=True), server_default=func.now())
    synced_at:    Mapped[datetime]             = mapped_column(
                      DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
