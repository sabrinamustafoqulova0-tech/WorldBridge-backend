from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.external_scholarship import ExternalScholarship, ScholarshipCategory
from models.user import User
from schemas.scholarship import ScholarshipListResponse, ScholarshipResponse
from services.scholarship_tracker import sync_all_sources
from utils.dependencies import get_current_admin

router = APIRouter(prefix="/scholarships", tags=["Scholarships"])


# ── Admin sync (declared before any /{id} wildcard) ──────────────────────────

@router.post("/admin/sync")
async def trigger_sync(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """[Admin] Manually trigger a full sync of all RSS scholarship sources."""
    results = await sync_all_sources(db)
    return {"status": "ok", "results": results}


# ── Public listing ────────────────────────────────────────────────────────────

@router.get("", response_model=ScholarshipListResponse)
async def list_scholarships(
    page:     int = Query(1, ge=1),
    size:     int = Query(20, ge=1, le=100),
    category: Optional[ScholarshipCategory] = None,
    country:  Optional[str] = Query(None, max_length=100),
    search:   Optional[str] = Query(None, max_length=100),
    db: AsyncSession = Depends(get_db),
):
    """List active external scholarships with optional filters."""
    base = select(ExternalScholarship).where(ExternalScholarship.is_active.is_(True))

    if category:
        base = base.where(ExternalScholarship.category == category)
    if country:
        base = base.where(ExternalScholarship.country.ilike(f"%{country}%"))
    if search:
        p = f"%{search}%"
        base = base.where(
            or_(
                ExternalScholarship.title.ilike(p),
                ExternalScholarship.description.ilike(p),
            )
        )

    total = (
        await db.execute(select(func.count()).select_from(base.subquery()))
    ).scalar_one()

    result = await db.execute(
        base.order_by(ExternalScholarship.published_at.desc().nullslast())
            .offset((page - 1) * size)
            .limit(size)
    )
    items = list(result.scalars().all())

    return ScholarshipListResponse(items=items, total=total, page=page, size=size)
