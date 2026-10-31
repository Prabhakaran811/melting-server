from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer_schema import CustomerCreate


class CustomerRepository:

    @staticmethod
    def create(db: Session, customer_data: CustomerCreate):
        customer = Customer(**customer_data.model_dump())

        try:
            db.add(customer)
            db.commit()
            db.refresh(customer)
            return customer
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(Customer)
            .order_by(Customer.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, customer_id: int):
        return (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

    @staticmethod
    def update(db: Session, customer: Customer, update_data: dict):
        try:
            for field, value in update_data.items():
                setattr(customer, field, value)

            db.commit()
            db.refresh(customer)
            return customer
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete(db: Session, customer: Customer):
        try:
            db.delete(customer)
            db.commit()
            return True
        except Exception:
            db.rollback()
            raise