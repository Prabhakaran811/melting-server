from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.raw_material_stock_schema import (
    RawMaterialStockCreate,
    RawMaterialStockUpdate,
    RawMaterialStockResponse
)

from app.services.raw_material_stock_service import (
    RawMaterialStockService
)


router = APIRouter(
    prefix="/raw-material-stocks",
    tags=["Raw Material Stocks"]
)


@router.post(
    "/",
    response_model=RawMaterialStockResponse,
    status_code=status.HTTP_201_CREATED
)
def create_stock(
    data: RawMaterialStockCreate,
    db: Session = Depends(get_db)
):
    return RawMaterialStockService.create_stock(
        db, data.model_dump()
    )


@router.get(
    "/",
    response_model=list[RawMaterialStockResponse]
)
def get_stocks(db: Session = Depends(get_db)):
    return RawMaterialStockService.get_stocks(db)


@router.put(
    "/{stock_id}",
    response_model=RawMaterialStockResponse
)
def update_stock(
    stock_id: int,
    data: RawMaterialStockUpdate,
    db: Session = Depends(get_db)
):
    return RawMaterialStockService.update_stock(
        db, stock_id, data.model_dump()
    )


@router.delete("/{stock_id}")
def delete_stock(
    stock_id: int,
    db: Session = Depends(get_db)
):
    return RawMaterialStockService.delete_stock(
        db, stock_id
    )