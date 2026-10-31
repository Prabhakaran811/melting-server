from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.customer_schema import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate
)
from app.services.customer_service import CustomerService


router = APIRouter(
    prefix="/customers",
    tags=["Customer Management"]
)


# CREATE CUSTOMER
@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED
)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):
    return CustomerService.create_customer(db, customer_data)


# GET ALL CUSTOMERS
@router.get(
    "/",
    response_model=List[CustomerResponse]
)
def get_customers(
    db: Session = Depends(get_db)
):
    return CustomerService.get_customers(db)


# UPDATE CUSTOMER
@router.put(
    "/{customer_id}",
    response_model=CustomerResponse
)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db)
):
    try:
        return CustomerService.update_customer(
            db, customer_id, customer_data
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
            if str(error) == "Customer not found"
            else status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


# PERMANENT DELETE CUSTOMER
@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_200_OK
)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    try:
        return CustomerService.delete_customer(db, customer_id)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )