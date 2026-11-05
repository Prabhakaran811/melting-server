from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.element_stock_repository import (
    ElementStockRepository
)


class ElementStockService:

    @staticmethod
    def validate_references(
        db: Session,
        element_id: int,
        supplier_id: int
    ):

        element = ElementStockRepository.get_element_by_id(
            db, element_id
        )

        if not element:
            raise HTTPException(
                status_code=404,
                detail="Selected Element not found"
            )

        supplier = ElementStockRepository.get_supplier_by_id(
            db, supplier_id
        )

        if not supplier:
            raise HTTPException(
                status_code=404,
                detail="Selected Supplier not found"
            )

    @staticmethod
    def create_stock(db: Session, data: dict):

        ElementStockService.validate_references(
            db,
            data["element_id"],
            data["supplier_id"]
        )

        return ElementStockRepository.create(db, data)

    @staticmethod
    def get_stocks(db: Session):
        return ElementStockRepository.get_all(db)

    @staticmethod
    def update_stock(
        db: Session,
        stock_id: int,
        data: dict
    ):

        stock = ElementStockRepository.get_by_id(
            db, stock_id
        )

        if not stock:
            raise HTTPException(
                status_code=404,
                detail="Element Stock not found"
            )

        ElementStockService.validate_references(
            db,
            data["element_id"],
            data["supplier_id"]
        )

        return ElementStockRepository.update(
            db, stock, data
        )

    @staticmethod
    def delete_stock(db: Session, stock_id: int):

        stock = ElementStockRepository.get_by_id(
            db, stock_id
        )

        if not stock:
            raise HTTPException(
                status_code=404,
                detail="Element Stock not found"
            )

        ElementStockRepository.delete(db, stock)

        return {
            "message": "Element Stock permanently deleted"
        }