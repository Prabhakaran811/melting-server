from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.packing_schema import (
    PackingCreate,
    PackingUpdate,
    PackingResponse
)
from app.services.packing_service import PackingService


router = APIRouter(
    prefix="/packings",
    tags=["Packings"]
)


@router.post(
    "/",
    response_model=PackingResponse,
    status_code=status.HTTP_201_CREATED
)
def create_packing(
    data: PackingCreate,
    db: Session = Depends(get_db)
):
    return PackingService.create_packing(db, data.name)


@router.get("/", response_model=list[PackingResponse])
def get_packings(db: Session = Depends(get_db)):
    return PackingService.get_packings(db)


@router.put("/{packing_id}", response_model=PackingResponse)
def update_packing(
    packing_id: int,
    data: PackingUpdate,
    db: Session = Depends(get_db)
):
    return PackingService.update_packing(
        db, packing_id, data.name
    )


@router.delete("/{packing_id}")
def delete_packing(
    packing_id: int,
    db: Session = Depends(get_db)
):
    return PackingService.delete_packing(db, packing_id)