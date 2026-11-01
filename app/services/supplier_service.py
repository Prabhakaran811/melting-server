from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.supplier_repository import SupplierRepository
from app.schemas.supplier import SupplierCreate, SupplierUpdate


class SupplierService:

    @staticmethod
    def create_supplier(db: Session, supplier_data: SupplierCreate):
        return SupplierRepository.create(db, supplier_data)

    @staticmethod
    def get_all_suppliers(db: Session):
        return SupplierRepository.get_all(db)

    @staticmethod
    def update_supplier(
        db: Session,
        supplier_id: int,
        supplier_data: SupplierUpdate
    ):
        supplier = SupplierRepository.get_by_id(db, supplier_id)

        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supplier not found"
            )

        return SupplierRepository.update(db, supplier, supplier_data)

    @staticmethod
    def delete_supplier(db: Session, supplier_id: int):
        supplier = SupplierRepository.get_by_id(db, supplier_id)

        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supplier not found"
            )

        SupplierRepository.delete(db, supplier)

        return {"message": "Supplier deleted successfully"}