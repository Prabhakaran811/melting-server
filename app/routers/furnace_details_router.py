
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.repositories.furnace_details_repository import (
    FurnaceDetailsRepository,
)
from app.services.furnace_details_service import (
    FurnaceDetailsService,
)

# Replace this import with the actual get_db import
# already used by your existing routers.
from app.db.database import get_db


router = APIRouter()


@router.get("/{furnace_id}/details")
def get_furnace_details(
    furnace_id: int,
    db: Session = Depends(get_db),
):
    data = FurnaceDetailsService.get_furnace_details(
        db, furnace_id
    )

    return {
        "success": True,
        "message": "Furnace details retrieved successfully",
        "data": data,
    }



@router.post("/{furnace_id}/complete-melt")
def complete_furnace_melt(
    furnace_id: int,
    db: Session = Depends(get_db),
):
    data = FurnaceDetailsService.complete_melt(
        db=db,
        furnace_id=furnace_id,
    )

    return {
        "success": True,
        "message": "Furnace melt completed successfully",
        "data": data,
    }



@router.get("/{furnace_id}/history")
def get_furnace_history(
    furnace_id: int,
    db: Session = Depends(get_db),
):
    data = FurnaceDetailsService.get_furnace_history(
        db=db,
        furnace_id=furnace_id,
    )

    return {
        "success": True,
        "message": "Furnace history retrieved successfully",
        "data": data,
    }
