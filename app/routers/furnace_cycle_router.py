
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.furnace_cycle_schema import (
    FurnaceCycleStart,
    FurnaceCycleResponse
)

from app.services.furnace_cycle_service import (
    FurnaceCycleService
)


router = APIRouter(
    prefix="/furnace-cycles",
    tags=["Furnace Cycles"]
)


@router.post(
    "/furnaces/{furnace_id}/start",
    response_model=FurnaceCycleResponse,
    status_code=status.HTTP_201_CREATED
)
def start_furnace_cycle(
    furnace_id: int,
    data: FurnaceCycleStart,
    db: Session = Depends(get_db)
):
    return FurnaceCycleService.start_cycle(
        db,
        furnace_id,
        data
    )


@router.get(
    "/furnaces/{furnace_id}/current",
    response_model=FurnaceCycleResponse | None
)
def get_current_furnace_cycle(
    furnace_id: int,
    db: Session = Depends(get_db)
):
    return FurnaceCycleService.get_current_cycle(
        db,
        furnace_id
    )


@router.get(
    "/furnaces/{furnace_id}/history",
    response_model=list[FurnaceCycleResponse]
)
def get_furnace_cycle_history(
    furnace_id: int,
    db: Session = Depends(get_db)
):
    return FurnaceCycleService.get_cycle_history(
        db,
        furnace_id
    )
