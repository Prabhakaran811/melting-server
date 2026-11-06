from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.raw_material_stock_repository import (
    RawMaterialStockRepository
)


class RawMaterialStockService:

    @staticmethod
    def validate_stock_data(db: Session, data: dict):

        raw_material_id = data["raw_material_id"]
        supplier_id = data["supplier_id"]
        element_percentages = data["element_percentages"]

        # Validate Raw Material
        raw_material = (
            RawMaterialStockRepository.get_raw_material_by_id(
                db, raw_material_id
            )
        )

        if not raw_material:
            raise HTTPException(
                status_code=404,
                detail="Selected Raw Material not found"
            )

        # Validate Supplier
        supplier = RawMaterialStockRepository.get_supplier_by_id(
            db, supplier_id
        )

        if not supplier:
            raise HTTPException(
                status_code=404,
                detail="Selected Supplier not found"
            )

        # Get elements belonging to selected Raw Material
        raw_material_elements = (
            RawMaterialStockRepository.get_raw_material_elements(
                db, raw_material_id
            )
        )

        allowed_element_ids = {
            element.id for element in raw_material_elements
        }

        selected_element_ids = [
            item["element_id"] for item in element_percentages
        ]

        # Prevent duplicate elements
        if len(selected_element_ids) != len(set(selected_element_ids)):
            raise HTTPException(
                status_code=422,
                detail="Duplicate elements are not allowed"
            )

        # Check that every selected element belongs to the Raw Material
        invalid_elements = (
            set(selected_element_ids) - allowed_element_ids
        )

        if invalid_elements:
            raise HTTPException(
                status_code=422,
                detail=(
                    "Selected elements do not belong to the "
                    "selected Raw Material. Invalid element IDs: "
                    f"{sorted(invalid_elements)}"
                )
            )

    @staticmethod
    def create_stock(db: Session, data: dict):

        RawMaterialStockService.validate_stock_data(db, data)

        return RawMaterialStockRepository.create(db, data)

    @staticmethod
    def get_stocks(db: Session):
        return RawMaterialStockRepository.get_all(db)

    @staticmethod
    def update_stock(
        db: Session,
        stock_id: int,
        data: dict
    ):

        stock = RawMaterialStockRepository.get_by_id(
            db, stock_id
        )

        if not stock:
            raise HTTPException(
                status_code=404,
                detail="Raw Material Stock not found"
            )

        RawMaterialStockService.validate_stock_data(db, data)

        return RawMaterialStockRepository.update(
            db, stock, data
        )

    @staticmethod
    def delete_stock(db: Session, stock_id: int):

        stock = RawMaterialStockRepository.get_by_id(
            db, stock_id
        )

        if not stock:
            raise HTTPException(
                status_code=404,
                detail="Raw Material Stock not found"
            )

        RawMaterialStockRepository.delete(db, stock)

        return {
            "message": "Raw Material Stock permanently deleted"
        }