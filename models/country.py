from datetime import datetime
from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(10), unique=True, index=True, nullable=False)
    name_ru: Mapped[str] = mapped_column(String(100), nullable=False)
    name_en: Mapped[str] = mapped_column(String(100), nullable=False)
    flag_emoji: Mapped[str] = mapped_column(String(10), nullable=False, default="🌍")
    description_ru: Mapped[str] = mapped_column(Text, nullable=False, default="")
    description_en: Mapped[str] = mapped_column(Text, nullable=False, default="")
    capital: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    population: Mapped[str] = mapped_column(String(50), nullable=False, default="")
    languages: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    currency: Mapped[str] = mapped_column(String(50), nullable=False, default="")
    region: Mapped[str] = mapped_column(String(50), nullable=False, default="Europe")
    map_x: Mapped[float] = mapped_column(nullable=False, default=50.0)
    map_y: Mapped[float] = mapped_column(nullable=False, default=40.0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<Country slug={self.slug!r} name={self.name_en!r}>"
