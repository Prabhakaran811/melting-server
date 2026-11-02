from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.inoculant_schema import (
    InoculantCreate,
    InoculantUpdate,
    InoculantResponse
)
from app.services.inoculant_service import InoculantService

router = APIRouter(prefix="/inoculants", tags=["Inoculants"])


@router.post("/", response_model=InoculantResponse,
             status_code=status.HTTP_201_CREATED)
def create_inoculant(
    data: InoculantCreate,
    db: Session = Depends(get_db)
):
    return InoculantService.create_inoculant(db, data.name)


@router.get("/", response_model=list[InoculantResponse])
def get_inoculants(db: Session = Depends(get_db)):
    return InoculantService.get_inoculants(db)


@router.put("/{inoculant_id}", response_model=InoculantResponse)
def update_inoculant(
    inoculant_id: int,
    data: InoculantUpdate,
    db: Session = Depends(get_db)
):
    return InoculantService.update_inoculant(
        db, inoculant_id, data.name
    )


@router.delete("/{inoculant_id}")
def delete_inoculant(
    inoculant_id: int,
    db: Session = Depends(get_db)
):
    return InoculantService.delete_inoculant(db, inoculant_id)