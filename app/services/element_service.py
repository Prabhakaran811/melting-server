from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.element_repository import ElementRepository


class ElementService:

    @staticmethod
    def create_element(db: Session, data: dict):
        data["name"] = data["name"].strip()
        data["abbreviation"] = data["abbreviation"].strip().upper()

        if not data["name"] or not data["abbreviation"]:
            raise HTTPException(
                status_code=422,
                detail="Name and abbreviation cannot be empty"
            )

        if ElementRepository.get_by_name(db, data["name"]):
            raise HTTPException(
                status_code=409,
                detail="Element name already exists"
            )

        if ElementRepository.get_by_abbreviation(
            db, data["abbreviation"]
        ):
            raise HTTPException(
                status_code=409,
                detail="Element abbreviation already exists"
            )

        try:
            return ElementRepository.create(db, data)
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Element name or abbreviation already exists"
            )

    @staticmethod
    def get_elements(db: Session):
        return ElementRepository.get_all(db)

    @staticmethod
    def update_element(db: Session, element_id: int, data: dict):
        data["name"] = data["name"].strip()
        data["abbreviation"] = data["abbreviation"].strip().upper()

        if not data["name"] or not data["abbreviation"]:
            raise HTTPException(
                status_code=422,
                detail="Name and abbreviation cannot be empty"
            )

        element = ElementRepository.get_by_id(db, element_id)

        if not element:
            raise HTTPException(
                status_code=404,
                detail="Element not found"
            )

        existing_name = ElementRepository.get_by_name(db, data["name"])

        if existing_name and existing_name.id != element_id:
            raise HTTPException(
                status_code=409,
                detail="Element name already exists"
            )

        existing_abbreviation = (
            ElementRepository.get_by_abbreviation(
                db, data["abbreviation"]
            )
        )

        if (
            existing_abbreviation
            and existing_abbreviation.id != element_id
        ):
            raise HTTPException(
                status_code=409,
                detail="Element abbreviation already exists"
            )

        try:
            return ElementRepository.update(db, element, data)
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Element name or abbreviation already exists"
            )

    @staticmethod
    def delete_element(db: Session, element_id: int):
        element = ElementRepository.get_by_id(db, element_id)

        if not element:
            raise HTTPException(
                status_code=404,
                detail="Element not found"
            )

        ElementRepository.delete(db, element)

        return {"message": "Element permanently deleted"}