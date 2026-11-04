from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.wire_schema import (
    WireCreate,
    WireUpdate,
    WireResponse
)

from app.services.wire_service import WireService


router = APIRouter(
    prefix="/wires",
    tags=["Wires"]
)


@router.post(
    "/",
    response_model=WireResponse,
    status_code=status.HTTP_201_CREATED
)
def create_wire(
    data: WireCreate,
    db: Session = Depends(get_db)
):
    return WireService.create_wire(
        db,
        data.model_dump()
    )


@router.get(
    "/",
    response_model=list[WireResponse]
)
def get_wires(db: Session = Depends(get_db)):
    return WireService.get_wires(db)


@router.put(
    "/{wire_id}",
    response_model=WireResponse
)
def update_wire(
    wire_id: int,
    data: WireUpdate,
    db: Session = Depends(get_db)
):
    return WireService.update_wire(
        db,
        wire_id,
        data.model_dump()
    )


@router.delete("/{wire_id}")
def delete_wire(
    wire_id: int,
    db: Session = Depends(get_db)
):
    return WireService.delete_wire(
        db,
        wire_id
    )