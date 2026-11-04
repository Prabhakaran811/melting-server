from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.iron_type_schema import (
    IronTypeCreate,
    IronTypeUpdate,
    IronTypeResponse
)

from app.services.iron_type_service import IronTypeService


router = APIRouter(
    prefix="/iron-types",
    tags=["Iron Types"]
)


@router.post(
    "/",
    response_model=IronTypeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_iron_type(
    data: IronTypeCreate,
    db: Session = Depends(get_db)
):
    return IronTypeService.create_iron_type(
        db, data.model_dump()
    )


@router.get(
    "/",
    response_model=list[IronTypeResponse]
)
def get_iron_types(db: Session = Depends(get_db)):
    return IronTypeService.get_iron_types(db)


@router.put(
    "/{iron_type_id}",
    response_model=IronTypeResponse
)
def update_iron_type(
    iron_type_id: int,
    data: IronTypeUpdate,
    db: Session = Depends(get_db)
):
    return IronTypeService.update_iron_type(
        db,
        iron_type_id,
        data.model_dump()
    )


@router.delete("/{iron_type_id}")
def delete_iron_type(
    iron_type_id: int,
    db: Session = Depends(get_db)
):
    return IronTypeService.delete_iron_type(
        db, iron_type_id
    )