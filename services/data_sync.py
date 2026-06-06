"""
Data sync orchestrator.

Runs a named provider, fetches program data, upserts into DB,
and records a DataSyncLog entry.
"""
from datetime import datetime, timezone
from typing import Dict, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.data_sync_log import DataSyncLog, SyncStatus
from models.program import Program, ProgramCategory
from services.providers.base import DataProvider, ProgramSyncDTO
from services.providers.daad import DAADProvider
from services.providers.campusfrance import CampusFranceProvider

# Registry of available providers
PROVIDERS: Dict[str, Type[DataProvider]] = {
    "daad": DAADProvider,
    "campusfrance": CampusFranceProvider,
}


async def run_sync(source_name: str, db: AsyncSession) -> DataSyncLog:
    """
    Trigger a sync for the given source.

    Returns a DataSyncLog record with the result.
    Providers that are placeholders return 0 programs (no error).
    """
    if source_name not in PROVIDERS:
        log = DataSyncLog(
            source_name=source_name,
            status=SyncStatus.FAILED,
            error_message=f"Unknown provider: {source_name}. Available: {list(PROVIDERS.keys())}",
            finished_at=datetime.now(timezone.utc),
        )
        db.add(log)
        await db.commit()
        return log

    log = DataSyncLog(source_name=source_name, status=SyncStatus.RUNNING)
    db.add(log)
    await db.flush()

    try:
        provider: DataProvider = PROVIDERS[source_name]()
        dtos = await provider.fetch_programs()

        created = 0
        updated = 0

        for dto in dtos:
            slug = _build_slug(dto)
            existing = (
                await db.execute(select(Program).where(Program.slug == slug))
            ).scalar_one_or_none()

            if existing:
                _apply_dto(existing, dto)
                updated += 1
            else:
                program = Program(slug=slug, is_published=False)
                _apply_dto(program, dto)
                db.add(program)
                created += 1

        await db.flush()

        log.status = SyncStatus.SUCCESS
        log.programs_created = created
        log.programs_updated = updated

    except Exception as exc:
        log.status = SyncStatus.FAILED
        log.error_message = str(exc)

    log.finished_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(log)
    return log


def _build_slug(dto: ProgramSyncDTO) -> str:
    """Build a DB slug from source name + external ID."""
    clean_id = dto.external_id.lower().replace(" ", "-")[:80]
    return f"{dto.source_name}-{clean_id}"


def _apply_dto(program: Program, dto: ProgramSyncDTO) -> None:
    """Apply ProgramSyncDTO fields onto a Program ORM instance."""
    # Only update fields that the provider actually provided
    if dto.title_ru:
        program.title = dto.title_ru
    if dto.title_en:
        program.title_en = dto.title_en
    if dto.short_description_ru:
        program.short_description = dto.short_description_ru
    if dto.short_description_en:
        program.short_description_en = dto.short_description_en
    if dto.description_ru:
        program.description = dto.description_ru
    if dto.description_en:
        program.description_en = dto.description_en

    # Try to map category string to enum
    try:
        program.category = ProgramCategory(dto.category)
    except ValueError:
        program.category = ProgramCategory.STUDIUM  # safe default

    program.country_slug = dto.country_slug

    # Enrichment fields
    program.university_name = dto.university_name
    program.city = dto.city
    program.university_address = dto.university_address
    program.website_url = dto.website_url if dto.website_url else None
    program.official_url = dto.official_url or dto.website_url
    program.program_page_url = dto.program_page_url
    program.tuition_fee = dto.tuition_fee
    program.tuition_currency = dto.tuition_currency
    program.accommodation_cost = dto.accommodation_cost
    program.language_course_cost = dto.language_course_cost
    program.scholarship_available = dto.scholarship_available
    program.scholarship_amount = dto.scholarship_amount
    program.contact_email = dto.contact_email
    program.contact_phone = dto.contact_phone
    program.duration_months = dto.duration_months
    program.language_requirement = dto.language_requirement
    program.deadline = dto.deadline
    program.min_age = dto.min_age
    program.max_age = dto.max_age
    program.documents = dto.documents
    program.application_steps = dto.application_steps
    program.career_opportunities = dto.career_opportunities
    program.cover_image_url = dto.cover_image_url
    program.data_source = dto.source_name
    program.last_synced_at = dto.fetched_at
