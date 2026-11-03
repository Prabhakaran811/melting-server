from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.packing_repository import PackingRepository


class PackingService:

    @staticmethod
    def create_packing(db: Session, name: str):
        name = name.strip()

        if not name:
            raise HTTPException(
                status_code=422,
                detail="Packing name cannot be empty"
            )

        if PackingRepository.get_by_name(db, name):
            raise HTTPException(
                status_code=409,
                detail="Packing already exists"
            )

        try:
            return PackingRepository.create(db, name)
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Packing already exists"
            )

    @staticmethod
    def get_packings(db: Session):
        return PackingRepository.get_all(db)

    @staticmethod
    def update_packing(db: Session, packing_id: int, name: str):
        name = name.strip()

        if not name:
            raise HTTPException(
                status_code=422,
                detail="Packing name cannot be empty"
            )

        packing = PackingRepository.get_by_id(db, packing_id)

        if not packing:
            raise HTTPException(
                status_code=404,
                detail="Packing not found"
            )

        existing = PackingRepository.get_by_name(db, name)

        if existing and existing.id != packing_id:
            raise HTTPException(
                status_code=409,
                detail="Packing name already exists"
            )

        try:
            return PackingRepository.update(db, packing, name)
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Packing name already exists"
            )

    @staticmethod
    def delete_packing(db: Session, packing_id: int):
        packing = PackingRepository.get_by_id(db, packing_id)

        if not packing:
            raise HTTPException(
                status_code=404,
                detail="Packing not found"
            )

        PackingRepository.delete(db, packing)

        return {"message": "Packing permanently deleted"}