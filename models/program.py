import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class ProgramCategory(str, enum.Enum):
    AUSBILDUNG = "ausbildung"
    FSJ = "fsj"
    AU_PAIR = "au_pair"
    SCHULE = "schule"
    ARBEIT = "arbeit"
    STUDIUM = "studium"
    VOLUNTEERING = "volunteering"
    INTERNSHIP = "internship"
    LANGUAGE = "language"
    IMMIGRATION = "immigration"


class ProgramLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Program(Base):
    __tablename__ = "programs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    country_slug: Mapped[str | None] = mapped_column(String(10), index=True, nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    title_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title_tg: Mapped[str | None] = mapped_column(String(255), nullable=True)

    category: Mapped[ProgramCategory] = mapped_column(
        Enum(ProgramCategory, name="program_category"), nullable=False, index=True
    )
    level: Mapped[ProgramLevel] = mapped_column(
        Enum(ProgramLevel, name="program_level"),
        nullable=False,
        default=ProgramLevel.BEGINNER,
    )
    short_description: Mapped[str] = mapped_column(String(500), nullable=False)
    short_description_en: Mapped[str | None] = mapped_column(String(500), nullable=True)
    short_description_tg: Mapped[str | None] = mapped_column(String(500), nullable=True)

    description: Mapped[str] = mapped_column(Text, nullable=False)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_tg: Mapped[str | None] = mapped_column(Text, nullable=True)

    full_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    full_description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    full_description_tg: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_months: Mapped[int | None] = mapped_column(Integer, nullable=True)
    min_age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    language_requirement: Mapped[str | None] = mapped_column(String(100), nullable=True)
    salary_range: Mapped[str | None] = mapped_column(String(200), nullable=True)
    cost: Mapped[str | None] = mapped_column(String(300), nullable=True)
    documents: Mapped[str | None] = mapped_column(Text, nullable=True)
    deadline: Mapped[str | None] = mapped_column(String(200), nullable=True)
    official_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    residence_permit: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    pros: Mapped[str | None] = mapped_column(Text, nullable=True)
    cons: Mapped[str | None] = mapped_column(Text, nullable=True)
    career_opportunities: Mapped[str | None] = mapped_column(Text, nullable=True)




    cover_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cover_image_url_2: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cover_image_url_3: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    views_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # ── New enrichment fields (added via ALTER TABLE on startup) ──────────────
    # University linkage
    university_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("universities.id", ondelete="SET NULL"), nullable=True, index=True
    )
    university_name: Mapped[str | None] = mapped_column(String(300), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Cost details — store as formatted strings (e.g. "€500/semester", "free")
    # Never invent values; leave null if not verified from official source
    tuition_fee: Mapped[str | None] = mapped_column(String(200), nullable=True)
    tuition_currency: Mapped[str | None] = mapped_column(String(10), nullable=True)
    accommodation_cost: Mapped[str | None] = mapped_column(String(200), nullable=True)
    language_course_cost: Mapped[str | None] = mapped_column(String(200), nullable=True)

    # Scholarship info
    scholarship_available: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    scholarship_amount: Mapped[str | None] = mapped_column(String(200), nullable=True)

    # Contact info — only from verified official contact pages
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    university_address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    program_page_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Structured content
    application_steps: Mapped[str | None] = mapped_column(Text, nullable=True)  # newline-separated
    program_faq: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON: [{q,a}, …]

    # Sync metadata
    data_source: Mapped[str | None] = mapped_column(String(50), nullable=True, default="manual")
    last_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    favorites = relationship("Favorite", back_populates="program", cascade="all, delete-orphan")
    checklist_items = relationship("ChecklistItem", back_populates="program", cascade="all, delete-orphan")
    images = relationship(
        "ProgramImage", back_populates="program",
        cascade="all, delete-orphan",
        order_by="ProgramImage.display_order",
        lazy="noload",
    )
    university = relationship(
        "University", back_populates="programs",
        foreign_keys=[university_id],
        lazy="noload",
    )

    def __repr__(self) -> str:
        return f"<Program id={self.id} slug={self.slug!r} country={self.country_slug}>"
