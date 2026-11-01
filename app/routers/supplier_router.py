from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.supplier import (
    SupplierCreate,
    SupplierUpdate,
    SupplierResponse
)
from app.services.supplier_service import SupplierService


router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"]
)


@router.post(
    "/",
    response_model=SupplierResponse,
    status_code=status.HTTP_201_CREATED
)
def create_supplier(
    supplier_data: SupplierCreate,
    db: Session = Depends(get_db)
):
    return SupplierService.create_supplier(db, supplier_data)


@router.get(
    "/",
    response_model=list[SupplierResponse]
)
def get_suppliers(
    db: Session = Depends(get_db)
):
    return SupplierService.get_all_suppliers(db)


@router.put(
    "/{supplier_id}",
    response_model=SupplierResponse
)
def update_supplier(
    supplier_id: int,
    supplier_data: SupplierUpdate,
    db: Session = Depends(get_db)
):
    return SupplierService.update_supplier(
        db,
        supplier_id,
        supplier_data
    )


@router.delete(
    "/{supplier_id}"
)
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    return SupplierService.delete_supplier(db, supplier_id)