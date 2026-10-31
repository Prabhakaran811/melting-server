from sqlalchemy.orm import Session

from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer_schema import CustomerCreate, CustomerUpdate


class CustomerService:

    @staticmethod
    def create_customer(db: Session, customer_data: CustomerCreate):
        return CustomerRepository.create(db, customer_data)

    @staticmethod
    def get_customers(db: Session):
        return CustomerRepository.get_all(db)

    @staticmethod
    def update_customer(
        db: Session,
        customer_id: int,
        customer_data: CustomerUpdate
    ):
        customer = CustomerRepository.get_by_id(db, customer_id)

        if not customer:
            raise ValueError("Customer not found")

        update_data = customer_data.model_dump(exclude_unset=True)

        if not update_data:
            raise ValueError("No fields provided for update")

        return CustomerRepository.update(db, customer, update_data)

    @staticmethod
    def delete_customer(db: Session, customer_id: int):
        customer = CustomerRepository.get_by_id(db, customer_id)

        if not customer:
            raise ValueError("Customer not found")

        CustomerRepository.delete(db, customer)

        return {"message": "Customer permanently deleted"}