from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.inoculant_repository import InoculantRepository


class InoculantService:

    @staticmethod
    def create_inoculant(db: Session, name: str):
        name = name.strip()

        if InoculantRepository.get_by_name(db, name):
            raise HTTPException(
                status_code=409,
                detail="Inoculant already exists"
            )

        try:
            return InoculantRepository.create(db, name)
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Inoculant already exists"
            )

    @staticmethod
    def get_inoculants(db: Session):
        return InoculantRepository.get_all(db)

    @staticmethod
    def update_inoculant(db: Session, inoculant_id: int, name: str):
        inoculant = InoculantRepository.get_by_id(db, inoculant_id)

        if not inoculant:
            raise HTTPException(
                status_code=404,
                detail="Inoculant not found"
            )

        name = name.strip()

        existing = InoculantRepository.get_by_name(db, name)

        if existing and existing.id != inoculant_id:
            raise HTTPException(
                status_code=409,
                detail="Inoculant name already exists"
            )

        try:
            return InoculantRepository.update(db, inoculant, name)
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Inoculant name already exists"
            )

    @staticmethod
    def delete_inoculant(db: Session, inoculant_id: int):
        inoculant = InoculantRepository.get_by_id(db, inoculant_id)

        if not inoculant:
            raise HTTPException(
                status_code=404,
                detail="Inoculant not found"
            )

        InoculantRepository.delete(db, inoculant)

        return {"message": "Inoculant permanently deleted"}