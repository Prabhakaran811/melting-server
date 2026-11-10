
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.aim import Aim

from app.repositories.order_repository import OrderRepository
from app.schemas.order_schema import OrderCreate, OrderUpdate


class OrderService:

    @staticmethod
    def create_order(db: Session, data: OrderCreate):

        aim = db.query(Aim).filter(
            Aim.id == data.aim_id
        ).first()

        if not aim:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Selected Aim not found"
            )

        order = Order(
            aim_id=data.aim_id,
            customer_delivery_date=data.customer_delivery_date,
            status="Pending"
        )

        return OrderRepository.create(db, order)

    @staticmethod
    def get_orders(db: Session):
        return OrderRepository.get_all(db)

    @staticmethod
    def get_order(db: Session, order_id: int):

        order = OrderRepository.get_by_id(db, order_id)

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        return order

    @staticmethod
    def update_order(
        db: Session,
        order_id: int,
        data: OrderUpdate
    ):

        order = OrderRepository.get_by_id(db, order_id)

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        aim = db.query(Aim).filter(
            Aim.id == data.aim_id
        ).first()

        if not aim:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Selected Aim not found"
            )

        order.aim_id = data.aim_id
        order.status = data.status
        order.customer_delivery_date = data.customer_delivery_date

        return OrderRepository.update(db, order)

    @staticmethod
    def delete_order(db: Session, order_id: int):

        order = OrderRepository.get_by_id(db, order_id)

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        OrderRepository.delete(db, order)

        return {
            "message": "Order deleted successfully"
        }
