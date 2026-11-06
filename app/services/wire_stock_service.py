from sqlalchemy.orm import Session

from app.models.wire import Wire
from app.models.supplier import Supplier

from app.repositories.wire_stock_repository import (
    WireStockRepository,
)


class WireStockService:

    @staticmethod
    def validate_references(
        db: Session,
        wire_id: int,
        supplier_id: int,
    ):

        wire = (
            db.query(Wire)
            .filter(Wire.id == wire_id)
            .first()
        )

        if not wire:
            raise ValueError("Selected Wire does not exist")

        supplier = (
            db.query(Supplier)
            .filter(Supplier.id == supplier_id)
            .first()
        )

        if not supplier:
            raise ValueError("Selected Supplier does not exist")

    @staticmethod
    def create_wire_stock(db: Session, data):

        WireStockService.validate_references(
            db=db,
            wire_id=data.wire_id,
            supplier_id=data.supplier_id,
        )

        return WireStockRepository.create(
            db,
            data.model_dump(),
        )

    @staticmethod
    def get_wire_stocks(db: Session):
        return WireStockRepository.get_all(db)

    @staticmethod
    def get_wire_stock(db: Session, stock_id: int):

        stock = WireStockRepository.get_by_id(db, stock_id)

        if not stock:
            raise LookupError("Wire Stock not found")

        return stock

    @staticmethod
    def update_wire_stock(
        db: Session,
        stock_id: int,
        data,
    ):

        stock = WireStockRepository.get_by_id(db, stock_id)

        if not stock:
            raise LookupError("Wire Stock not found")

        WireStockService.validate_references(
            db=db,
            wire_id=data.wire_id,
            supplier_id=data.supplier_id,
        )

        return WireStockRepository.update(
            db,
            stock,
            data.model_dump(),
        )

    @staticmethod
    def delete_wire_stock(db: Session, stock_id: int):

        stock = WireStockRepository.get_by_id(db, stock_id)

        if not stock:
            raise LookupError("Wire Stock not found")

        return WireStockRepository.delete(db, stock)