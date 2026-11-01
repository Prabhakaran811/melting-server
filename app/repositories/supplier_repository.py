from sqlalchemy.orm import Session

from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate


class SupplierRepository:

    @staticmethod
    def create(db: Session, supplier_data: SupplierCreate):
        supplier = Supplier(**supplier_data.model_dump())

        db.add(supplier)
        db.commit()
        db.refresh(supplier)

        return supplier

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(Supplier)
            .order_by(Supplier.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, supplier_id: int):
        return (
            db.query(Supplier)
            .filter(Supplier.id == supplier_id)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        supplier: Supplier,
        supplier_data: SupplierUpdate
    ):
        update_data = supplier_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(supplier, field, value)

        db.commit()
        db.refresh(supplier)

        return supplier

    @staticmethod
    def delete(db: Session, supplier: Supplier):
        db.delete(supplier)
        db.commit()