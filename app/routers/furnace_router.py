from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.furnace_schema import (
    FurnaceCreate,
    FurnaceUpdate,
    FurnaceStatusUpdate,
    FurnaceResponse,
)

from app.services.furnace_service import FurnaceService


router = APIRouter(
    prefix="/furnaces",
    tags=["Furnace Master"]
)


# CREATE FURNACE
@router.post(
    "/",
    response_model=FurnaceResponse,
    status_code=status.HTTP_201_CREATED
)
def create_furnace(
    furnace_data: FurnaceCreate,
    db: Session = Depends(get_db)
):
    return FurnaceService.create_furnace(db, furnace_data)


# GET ALL FURNACES
@router.get(
    "/",
    response_model=List[FurnaceResponse]
)
def get_furnaces(
    db: Session = Depends(get_db)
):
    return FurnaceService.get_furnaces(db)


# UPDATE FURNACE
@router.put(
    "/{furnace_id}",
    response_model=FurnaceResponse
)
def update_furnace(
    furnace_id: int,
    furnace_data: FurnaceUpdate,
    db: Session = Depends(get_db)
):
    return FurnaceService.update_furnace(
        db,
        furnace_id,
        furnace_data
    )


# ACTIVATE / DEACTIVATE FURNACE
@router.patch(
    "/{furnace_id}/status",
    response_model=FurnaceResponse
)
def update_furnace_status(
    furnace_id: int,
    status_data: FurnaceStatusUpdate,
    db: Session = Depends(get_db)
):
    return FurnaceService.update_furnace_status(
        db,
        furnace_id,
        status_data.is_active
    )