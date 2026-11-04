from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.raw_material_repository import (
    RawMaterialRepository
)


class RawMaterialService:

    @staticmethod
    def validate_elements(db: Session, element_ids: list[int]):

        if len(element_ids) != len(set(element_ids)):
            raise HTTPException(
                status_code=422,
                detail="Duplicate element IDs are not allowed"
            )

        elements = RawMaterialRepository.get_elements_by_ids(
            db, element_ids
        )

        if len(elements) != len(element_ids):
            raise HTTPException(
                status_code=404,
                detail="One or more selected elements were not found"
            )

        return elements

    @staticmethod
    def create_raw_material(db: Session, data: dict):

        name = data["name"].strip()
        element_ids = data["element_ids"]

        if not name:
            raise HTTPException(
                status_code=422,
                detail="Raw material name cannot be empty"
            )

        existing = RawMaterialRepository.get_by_name(db, name)

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Raw material already exists"
            )

        elements = RawMaterialService.validate_elements(
            db, element_ids
        )

        try:
            return RawMaterialRepository.create(
                db, name, elements
            )

        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Raw material already exists"
            )

    @staticmethod
    def get_raw_materials(db: Session):
        return RawMaterialRepository.get_all(db)

    @staticmethod
    def update_raw_material(
        db: Session,
        raw_material_id: int,
        data: dict
    ):

        name = data["name"].strip()
        element_ids = data["element_ids"]

        if not name:
            raise HTTPException(
                status_code=422,
                detail="Raw material name cannot be empty"
            )

        raw_material = RawMaterialRepository.get_by_id(
            db, raw_material_id
        )

        if not raw_material:
            raise HTTPException(
                status_code=404,
                detail="Raw material not found"
            )

        existing = RawMaterialRepository.get_by_name(db, name)

        if existing and existing.id != raw_material_id:
            raise HTTPException(
                status_code=409,
                detail="Raw material name already exists"
            )

        elements = RawMaterialService.validate_elements(
            db, element_ids
        )

        try:
            return RawMaterialRepository.update(
                db, raw_material, name, elements
            )

        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Raw material name already exists"
            )

    @staticmethod
    def delete_raw_material(db: Session, raw_material_id: int):

        raw_material = RawMaterialRepository.get_by_id(
            db, raw_material_id
        )

        if not raw_material:
            raise HTTPException(
                status_code=404,
                detail="Raw material not found"
            )

        RawMaterialRepository.delete(db, raw_material)

        return {
            "message": "Raw material permanently deleted"
        }