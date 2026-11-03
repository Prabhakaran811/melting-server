from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.element_schema import (
    ElementCreate,
    ElementUpdate,
    ElementResponse
)
from app.services.element_service import ElementService


router = APIRouter(
    prefix="/elements",
    tags=["Elements"]
)


@router.post(
    "/",
    response_model=ElementResponse,
    status_code=status.HTTP_201_CREATED
)
def create_element(
    data: ElementCreate,
    db: Session = Depends(get_db)
):
    return ElementService.create_element(
        db, data.model_dump()
    )


@router.get("/", response_model=list[ElementResponse])
def get_elements(db: Session = Depends(get_db)):
    return ElementService.get_elements(db)


@router.put("/{element_id}", response_model=ElementResponse)
def update_element(
    element_id: int,
    data: ElementUpdate,
    db: Session = Depends(get_db)
):
    return ElementService.update_element(
        db, element_id, data.model_dump()
    )


@router.delete("/{element_id}")
def delete_element(
    element_id: int,
    db: Session = Depends(get_db)
):
    return ElementService.delete_element(db, element_id)