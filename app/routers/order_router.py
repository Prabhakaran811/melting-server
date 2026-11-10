from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.order_schema import (
    OrderCreate,
    OrderUpdate,
    OrderResponse
)
from app.services.order_service import OrderService


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED
)
def create_order(
    data: OrderCreate,
    db: Session = Depends(get_db)
):
    return OrderService.create_order(db, data)


@router.get(
    "/",
    response_model=list[OrderResponse]
)
def get_orders(db: Session = Depends(get_db)):
    return OrderService.get_orders(db)


@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    return OrderService.get_order(db, order_id)


@router.put(
    "/{order_id}",
    response_model=OrderResponse
)
def update_order(
    order_id: int,
    data: OrderUpdate,
    db: Session = Depends(get_db)
):
    return OrderService.update_order(db, order_id, data)


@router.delete(
    "/{order_id}"
)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    return OrderService.delete_order(db, order_id)