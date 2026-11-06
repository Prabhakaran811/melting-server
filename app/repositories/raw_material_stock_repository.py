from sqlalchemy.orm import Session, joinedload, selectinload

from app.models.raw_material_stock import (
    RawMaterialStock,
    RawMaterialStockElement
)

from app.models.raw_material import RawMaterial
from app.models.element import Element
from app.models.supplier import Supplier


class RawMaterialStockRepository:

    @staticmethod
    def create(db: Session, data: dict):
        try:
            element_percentages = data.pop("element_percentages")

            stock = RawMaterialStock(**data)

            for item in element_percentages:
                stock.element_percentages.append(
                    RawMaterialStockElement(
                        element_id=item["element_id"],
                        percentage=item["percentage"]
                    )
                )

            db.add(stock)
            db.commit()
            db.refresh(stock)

            return RawMaterialStockRepository.get_by_id(
                db, stock.id
            )

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(RawMaterialStock)
            .options(
                joinedload(RawMaterialStock.raw_material),
                joinedload(RawMaterialStock.supplier),
                selectinload(
                    RawMaterialStock.element_percentages
                ).joinedload(
                    RawMaterialStockElement.element
                )
            )
            .order_by(RawMaterialStock.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, stock_id: int):
        return (
            db.query(RawMaterialStock)
            .options(
                joinedload(RawMaterialStock.raw_material),
                joinedload(RawMaterialStock.supplier),
                selectinload(
                    RawMaterialStock.element_percentages
                ).joinedload(
                    RawMaterialStockElement.element
                )
            )
            .filter(RawMaterialStock.id == stock_id)
            .first()
        )

    @staticmethod
    def get_raw_material_by_id(db: Session, raw_material_id: int):
        return db.query(RawMaterial).filter(
            RawMaterial.id == raw_material_id
        ).first()

    @staticmethod
    def get_supplier_by_id(db: Session, supplier_id: int):
        return db.query(Supplier).filter(
            Supplier.id == supplier_id
        ).first()

    @staticmethod
    def get_raw_material_elements(
        db: Session,
        raw_material_id: int
    ):
        raw_material = (
            db.query(RawMaterial)
            .options(selectinload(RawMaterial.elements))
            .filter(RawMaterial.id == raw_material_id)
            .first()
        )

        if not raw_material:
            return None

        return raw_material.elements

    @staticmethod
    def update(db: Session, stock, data: dict):
        try:
            element_percentages = data.pop("element_percentages")

            stock.raw_material_id = data["raw_material_id"]
            stock.quantity = data["quantity"]
            stock.supplier_id = data["supplier_id"]
            stock.received_date = data["received_date"]
            stock.rate_per_kg = data["rate_per_kg"]

            # Replace old percentage records with the new ones
            stock.element_percentages.clear()

            for item in element_percentages:
                stock.element_percentages.append(
                    RawMaterialStockElement(
                        element_id=item["element_id"],
                        percentage=item["percentage"]
                    )
                )

            db.commit()
            db.refresh(stock)

            return RawMaterialStockRepository.get_by_id(
                db, stock.id
            )

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete(db: Session, stock):
        try:
            db.delete(stock)
            db.commit()

        except Exception:
            db.rollback()
            raise