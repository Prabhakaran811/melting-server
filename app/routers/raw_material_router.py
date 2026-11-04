from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.raw_material_schema import (
    RawMaterialCreate,
    RawMaterialUpdate,
    RawMaterialResponse
)

from app.services.raw_material_service import RawMaterialService


router = APIRouter(
    prefix="/raw-materials",
    tags=["Raw Materials"]
)


@router.post(
    "/",
    response_model=RawMaterialResponse,
    status_code=status.HTTP_201_CREATED
)
def create_raw_material(
    data: RawMaterialCreate,
    db: Session = Depends(get_db)
):
    return RawMaterialService.create_raw_material(
        db, data.model_dump()
    )


@router.get(
    "/",
    response_model=list[RawMaterialResponse]
)
def get_raw_materials(db: Session = Depends(get_db)):
    return RawMaterialService.get_raw_materials(db)


@router.put(
    "/{raw_material_id}",
    response_model=RawMaterialResponse
)
def update_raw_material(
    raw_material_id: int,
    data: RawMaterialUpdate,
    db: Session = Depends(get_db)
):
    return RawMaterialService.update_raw_material(
        db,
        raw_material_id,
        data.model_dump()
    )


@router.delete("/{raw_material_id}")
def delete_raw_material(
    raw_material_id: int,
    db: Session = Depends(get_db)
):
    return RawMaterialService.delete_raw_material(
        db, raw_material_id
    )