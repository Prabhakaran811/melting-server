from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.iron_type_repository import IronTypeRepository


class IronTypeService:

    @staticmethod
    def validate_elements(db: Session, element_ids: list[int]):
        if len(element_ids) != len(set(element_ids)):
            raise HTTPException(
                status_code=422,
                detail="Duplicate element IDs are not allowed"
            )

        elements = IronTypeRepository.get_elements_by_ids(
            db, element_ids
        )

        if len(elements) != len(element_ids):
            raise HTTPException(
                status_code=404,
                detail="One or more selected elements were not found"
            )

        return elements

    @staticmethod
    def create_iron_type(db: Session, data: dict):
        name = data["name"].strip()
        element_ids = data["element_ids"]

        if not name:
            raise HTTPException(
                status_code=422,
                detail="Iron Type name cannot be empty"
            )

        existing = IronTypeRepository.get_by_name(db, name)

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Iron Type already exists"
            )

        elements = IronTypeService.validate_elements(
            db, element_ids
        )

        try:
            return IronTypeRepository.create(
                db, name, elements
            )

        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Iron Type already exists"
            )

    @staticmethod
    def get_iron_types(db: Session):
        return IronTypeRepository.get_all(db)

    @staticmethod
    def update_iron_type(
        db: Session,
        iron_type_id: int,
        data: dict
    ):
        name = data["name"].strip()
        element_ids = data["element_ids"]

        if not name:
            raise HTTPException(
                status_code=422,
                detail="Iron Type name cannot be empty"
            )

        iron_type = IronTypeRepository.get_by_id(
            db, iron_type_id
        )

        if not iron_type:
            raise HTTPException(
                status_code=404,
                detail="Iron Type not found"
            )

        existing = IronTypeRepository.get_by_name(db, name)

        if existing and existing.id != iron_type_id:
            raise HTTPException(
                status_code=409,
                detail="Iron Type name already exists"
            )

        elements = IronTypeService.validate_elements(
            db, element_ids
        )

        try:
            return IronTypeRepository.update(
                db, iron_type, name, elements
            )

        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Iron Type name already exists"
            )

    @staticmethod
    def delete_iron_type(db: Session, iron_type_id: int):
        iron_type = IronTypeRepository.get_by_id(
            db, iron_type_id
        )

        if not iron_type:
            raise HTTPException(
                status_code=404,
                detail="Iron Type not found"
            )

        IronTypeRepository.delete(db, iron_type)

        return {"message": "Iron Type permanently deleted"}