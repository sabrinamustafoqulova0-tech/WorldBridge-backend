import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class ImageType(str, enum.Enum):
    HERO = "hero"
    CAMPUS = "campus"
    CITY = "city"
    STUDENTS = "students"
    WORKPLACE = "workplace"
    PARTNER = "partner"


class ProgramImage(Base):
    __tablename__ = "program_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    program_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("programs.id", ondelete="CASCADE"), nullable=False, index=True
    )

    url: Mapped[str] = mapped_column(String(500), nullable=False)
    caption_ru: Mapped[str | None] = mapped_column(String(300), nullable=True)
    caption_en: Mapped[str | None] = mapped_column(String(300), nullable=True)
    image_type: Mapped[ImageType | None] = mapped_column(
        Enum(ImageType, name="image_type"), nullable=True
    )
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    program = relationship("Program", back_populates="images")

    def __repr__(self) -> str:
        return f"<ProgramImage id={self.id} program_id={self.program_id} type={self.image_type}>"
