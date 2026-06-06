"""
Abstract base provider for data sync.

Each provider fetches program data from an external source and returns
a list of ProgramSyncDTO objects. The sync service then upserts these
into the database.

NOTE: Most educational portals (DAAD, Campus France, etc.) do NOT provide
free public APIs. Providers here are either:
  - Placeholder stubs (return []) pending official access
  - Adapters for portals that DO expose public data (future implementation)
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class ProgramSyncDTO:
    """Normalized program data from any external provider."""
    # Required
    external_id: str          # unique ID in the source system
    source_name: str          # e.g. "daad", "campusfrance"
    title_ru: str
    category: str             # must match ProgramCategory enum value
    country_slug: str

    # Descriptive (optional — never invent values)
    title_en: Optional[str] = None
    short_description_ru: Optional[str] = None
    short_description_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None

    # University info
    university_name: Optional[str] = None
    university_slug: Optional[str] = None
    city: Optional[str] = None
    university_address: Optional[str] = None
    website_url: Optional[str] = None
    program_page_url: Optional[str] = None

    # Cost info (strings — "€500/semester", "free", etc.)
    tuition_fee: Optional[str] = None
    tuition_currency: Optional[str] = None
    accommodation_cost: Optional[str] = None
    language_course_cost: Optional[str] = None

    # Scholarship
    scholarship_available: bool = False
    scholarship_amount: Optional[str] = None

    # Contacts (only from official contact pages)
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None

    # Program details
    duration_months: Optional[int] = None
    language_requirement: Optional[str] = None
    deadline: Optional[str] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    documents: Optional[str] = None
    application_steps: Optional[str] = None
    career_opportunities: Optional[str] = None
    official_url: Optional[str] = None

    # Images
    cover_image_url: Optional[str] = None
    gallery_urls: List[str] = field(default_factory=list)

    fetched_at: datetime = field(default_factory=datetime.utcnow)


class DataProvider(ABC):
    """Abstract base class for all data sync providers."""

    source_name: str

    @abstractmethod
    async def fetch_programs(self) -> List[ProgramSyncDTO]:
        """
        Fetch the full list of programs from the external source.
        Return empty list if source is unavailable or access is not configured.
        """
        ...

    @abstractmethod
    async def fetch_program_detail(self, external_id: str) -> Optional[ProgramSyncDTO]:
        """
        Fetch detailed data for a single program by its external ID.
        Return None if not found.
        """
        ...

    def is_configured(self) -> bool:
        """Return True if this provider has the required credentials/config."""
        return False
