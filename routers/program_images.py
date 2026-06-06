from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.program import Program
from models.program_image import ProgramImage
from models.user import User
from schemas.program_image import (
    ProgramImageCreate,
    ProgramImageListResponse,
    ProgramImageResponse,
)
from utils.dependencies import get_current_admin

router = APIRouter(prefix="/programs", tags=["Program Images"])


@router.get("/{slug}/images", response_model=ProgramImageListResponse)
async def list_program_images(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """List all images for a program (public)."""
    program = (
        await db.execute(select(Program).where(Program.slug == slug))
    ).scalar_one_or_none()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    result = await db.execute(
        select(ProgramImage)
        .where(ProgramImage.program_id == program.id)
        .order_by(ProgramImage.display_order)
    )
    images = list(result.scalars().all())
    return ProgramImageListResponse(items=images, total=len(images))


@router.post(
    "/{slug}/images",
    response_model=ProgramImageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_program_image(
    slug: str,
    payload: ProgramImageCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """[Admin] Add an image to a program."""
    program = (
        await db.execute(select(Program).where(Program.slug == slug))
    ).scalar_one_or_none()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    image = ProgramImage(program_id=program.id, **payload.model_dump())
    db.add(image)
    await db.flush()
    await db.refresh(image)
    return image


@router.delete("/{slug}/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_program_image(
    slug: str,
    image_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """[Admin] Delete an image from a program."""
    program = (
        await db.execute(select(Program).where(Program.slug == slug))
    ).scalar_one_or_none()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    image = (
        await db.execute(
            select(ProgramImage).where(
                ProgramImage.id == image_id,
                ProgramImage.program_id == program.id,
            )
        )
    ).scalar_one_or_none()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    await db.delete(image)
