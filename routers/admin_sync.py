from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.data_sync_log import DataSyncLog, SyncStatus
from models.user import User
from services.data_sync import PROVIDERS, run_sync
from utils.dependencies import get_current_admin

router = APIRouter(prefix="/admin/sync", tags=["Admin — Data Sync"])


# ── Response schemas (inline — admin-only, not part of public API) ────────────

class SyncLogResponse(BaseModel):
    id: int
    source_name: str
    started_at: datetime
    finished_at: Optional[datetime] = None
    status: SyncStatus
    programs_created: int
    programs_updated: int
    error_message: Optional[str] = None

    model_config = {"from_attributes": True}


class SyncLogListResponse(BaseModel):
    items: list[SyncLogResponse]
    total: int


class SyncTriggerResponse(BaseModel):
    message: str
    log: SyncLogResponse


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/{source_name}", response_model=SyncTriggerResponse)
async def trigger_sync(
    source_name: str,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """
    [Admin] Manually trigger a data sync for the given source.

    Available sources: daad, campusfrance

    NOTE: All current providers are placeholders — they return 0 programs
    until real API access is configured. The endpoint still creates a
    DataSyncLog record so the infrastructure can be tested.
    """
    if source_name not in PROVIDERS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown provider: {source_name!r}. Available: {list(PROVIDERS.keys())}",
        )
    log = await run_sync(source_name, db)
    return SyncTriggerResponse(
        message=f"Sync completed: {log.programs_created} created, {log.programs_updated} updated",
        log=SyncLogResponse.model_validate(log),
    )


@router.get("/logs", response_model=SyncLogListResponse)
async def list_sync_logs(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    source_name: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """[Admin] List data sync history."""
    from sqlalchemy import func
    base = select(DataSyncLog)
    if source_name:
        base = base.where(DataSyncLog.source_name == source_name)
    total = (await db.execute(select(func.count()).select_from(base.subquery()))).scalar_one()
    result = await db.execute(
        base.order_by(DataSyncLog.started_at.desc()).offset((page - 1) * size).limit(size)
    )
    logs = list(result.scalars().all())
    return SyncLogListResponse(items=logs, total=total)
