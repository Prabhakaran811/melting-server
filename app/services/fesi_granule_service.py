from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.fesi_granule_repository import (
    FeSiGranuleRepository
)


class FeSiGranuleService:

    @staticmethod
    def create_granule(db: Session, name: str):
        name = name.strip()

        if not name:
            raise HTTPException(
                status_code=422,
                detail="Name cannot be empty"
            )

        if FeSiGranuleRepository.get_by_name(db, name):
            raise HTTPException(
                status_code=409,
                detail="FeSi Granule already exists"
            )

        try:
            return FeSiGranuleRepository.create(db, name)
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="FeSi Granule already exists"
            )

    @staticmethod
    def get_granules(db: Session):
        return FeSiGranuleRepository.get_all(db)

    @staticmethod
    def update_granule(db: Session, granule_id: int, name: str):
        name = name.strip()

        if not name:
            raise HTTPException(
                status_code=422,
                detail="Name cannot be empty"
            )

        granule = FeSiGranuleRepository.get_by_id(db, granule_id)

        if not granule:
            raise HTTPException(
                status_code=404,
                detail="FeSi Granule not found"
            )

        existing = FeSiGranuleRepository.get_by_name(db, name)

        if existing and existing.id != granule_id:
            raise HTTPException(
                status_code=409,
                detail="FeSi Granule name already exists"
            )

        try:
            return FeSiGranuleRepository.update(db, granule, name)
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="FeSi Granule name already exists"
            )

    @staticmethod
    def delete_granule(db: Session, granule_id: int):
        granule = FeSiGranuleRepository.get_by_id(db, granule_id)

        if not granule:
            raise HTTPException(
                status_code=404,
                detail="FeSi Granule not found"
            )

        FeSiGranuleRepository.delete(db, granule)

        return {"message": "FeSi Granule permanently deleted"}