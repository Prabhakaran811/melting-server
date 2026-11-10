
from sqlalchemy.orm import Session, joinedload
from uuid import uuid4

from app.models.order import Order


class OrderRepository:

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(Order)
            .options(joinedload(Order.aim))
            .order_by(Order.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, order_id: int):
        return (
            db.query(Order)
            .options(joinedload(Order.aim))
            .filter(Order.id == order_id)
            .first()
        )

    @staticmethod
    def create(db: Session, order: Order):
        try:
            # Generate a temporary unique number within 30 characters
            order.order_number = f"TEMP-{uuid4().hex[:20]}"

            db.add(order)
            db.flush()

            # Generate the final order number using the database ID
            order.order_number = f"ORD-{order.id:06d}"

            db.commit()
            db.refresh(order)

            return OrderRepository.get_by_id(db, order.id)

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def update(db: Session, order: Order):
        try:
            db.commit()
            db.refresh(order)

            return OrderRepository.get_by_id(db, order.id)

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete(db: Session, order: Order):
        try:
            db.delete(order)
            db.commit()
            return True

        except Exception:
            db.rollback()
            raise
