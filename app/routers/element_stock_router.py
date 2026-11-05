from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.element_stock_schema import (
    ElementStockCreate,
    ElementStockUpdate,
    ElementStockResponse
)

from app.services.element_stock_service import (
    ElementStockService
)


router = APIRouter(
    prefix="/element-stocks",
    tags=["Element Stocks"]
)


@router.post(
    "/",
    response_model=ElementStockResponse,
    status_code=status.HTTP_201_CREATED
)
def create_stock(
    data: ElementStockCreate,
    db: Session = Depends(get_db)
):
    return ElementStockService.create_stock(
        db, data.model_dump()
    )


@router.get(
    "/",
    response_model=list[ElementStockResponse]
)
def get_stocks(db: Session = Depends(get_db)):
    return ElementStockService.get_stocks(db)


@router.put(
    "/{stock_id}",
    response_model=ElementStockResponse
)
def update_stock(
    stock_id: int,
    data: ElementStockUpdate,
    db: Session = Depends(get_db)
):
    return ElementStockService.update_stock(
        db, stock_id, data.model_dump()
    )


@router.delete("/{stock_id}")
def delete_stock(
    stock_id: int,
    db: Session = Depends(get_db)
):
    return ElementStockService.delete_stock(
        db, stock_id
    )