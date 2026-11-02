from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.hardness_schema import (
    HardnessCreate,
    HardnessResponse
)

from app.services.hardness_service import HardnessService


router = APIRouter(
    prefix="/hardnesses",
    tags=["Hardness Master"]
)


# CREATE HARDNESS
@router.post(
    "/",
    response_model=HardnessResponse,
    status_code=status.HTTP_201_CREATED
)
def create_hardness(
    hardness_data: HardnessCreate,
    db: Session = Depends(get_db)
):
    return HardnessService.create_hardness(db, hardness_data)


# GET ALL HARDNESSES
@router.get(
    "/",
    response_model=List[HardnessResponse]
)
def get_hardnesses(
    db: Session = Depends(get_db)
):
    return HardnessService.get_hardnesses(db)


# UPDATE HARDNESS
@router.put(
    "/{hardness_id}",
    response_model=HardnessResponse
)
def update_hardness(
    hardness_id: int,
    hardness_data: HardnessCreate,
    db: Session = Depends(get_db)
):
    return HardnessService.update_hardness(
        db,
        hardness_id,
        hardness_data
    )


# PERMANENT DELETE HARDNESS
@router.delete(
    "/{hardness_id}"
)
def delete_hardness(
    hardness_id: int,
    db: Session = Depends(get_db)
):
    return HardnessService.delete_hardness(db, hardness_id)