from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.fesi_granule_schema import (
    FeSiGranuleCreate,
    FeSiGranuleUpdate,
    FeSiGranuleResponse
)
from app.services.fesi_granule_service import FeSiGranuleService


router = APIRouter(
    prefix="/fesi-granules",
    tags=["FeSi Granules"]
)


@router.post(
    "/",
    response_model=FeSiGranuleResponse,
    status_code=status.HTTP_201_CREATED
)
def create_granule(
    data: FeSiGranuleCreate,
    db: Session = Depends(get_db)
):
    return FeSiGranuleService.create_granule(db, data.name)


@router.get("/", response_model=list[FeSiGranuleResponse])
def get_granules(db: Session = Depends(get_db)):
    return FeSiGranuleService.get_granules(db)


@router.put("/{granule_id}", response_model=FeSiGranuleResponse)
def update_granule(
    granule_id: int,
    data: FeSiGranuleUpdate,
    db: Session = Depends(get_db)
):
    return FeSiGranuleService.update_granule(
        db, granule_id, data.name
    )


@router.delete("/{granule_id}")
def delete_granule(
    granule_id: int,
    db: Session = Depends(get_db)
):
    return FeSiGranuleService.delete_granule(db, granule_id)