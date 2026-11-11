
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.furnace_cycle_schema import (
    FurnaceCycleStart,
    FurnaceCycleResponse,
)
from app.services.furnace_cycle_service import FurnaceCycleService


router = APIRouter(
    prefix="/furnaces",
    tags=["Furnace Operations"],
)


@router.post(
    "/{furnace_id}/start",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
)
def start_furnace(
    furnace_id: int,
    data: FurnaceCycleStart,
    db: Session = Depends(get_db),
):
    cycle = FurnaceCycleService.start_furnace(
        db=db,
        furnace_id=furnace_id,
        data=data,
    )

    return {
        "success": True,
        "message": "Furnace started successfully",
        "data": FurnaceCycleResponse.model_validate(cycle),
    }


@router.get(
    "/{furnace_id}/current-cycle",
    response_model=dict,
)
def get_current_cycle(
    furnace_id: int,
    db: Session = Depends(get_db),
):
    cycle = FurnaceCycleService.get_current_cycle(
        db=db,
        furnace_id=furnace_id,
    )

    if not cycle:
        return {
            "success": True,
            "message": "No running cycle found",
            "data": None,
        }

    return {
        "success": True,
        "message": "Current furnace cycle retrieved successfully",
        "data": FurnaceCycleResponse.model_validate(cycle),
    }


@router.get(
    "/{furnace_id}/cycles",
    response_model=dict,
)
def get_cycle_history(
    furnace_id: int,
    db: Session = Depends(get_db),
):
    cycles = FurnaceCycleService.get_cycle_history(
        db=db,
        furnace_id=furnace_id,
    )

    return {
        "success": True,
        "message": "Furnace cycle history retrieved successfully",
        "data": [
            FurnaceCycleResponse.model_validate(cycle)
            for cycle in cycles
        ],
    }
