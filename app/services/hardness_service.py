from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.hardness_repository import HardnessRepository
from app.schemas.hardness_schema import HardnessCreate


class HardnessService:

    @staticmethod
    def create_hardness(db: Session, hardness_data: HardnessCreate):

        hardness_name = hardness_data.hardness_name.strip()

        if not hardness_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Hardness name cannot be empty"
            )

        existing = HardnessRepository.get_by_name(db, hardness_name)

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Hardness name already exists"
            )

        try:
            cleaned_data = HardnessCreate(hardness_name=hardness_name)
            return HardnessRepository.create(db, cleaned_data)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Hardness name already exists"
            )

    @staticmethod
    def get_hardnesses(db: Session):
        return HardnessRepository.get_all(db)

    @staticmethod
    def update_hardness(
        db: Session,
        hardness_id: int,
        hardness_data: HardnessCreate
    ):
        hardness = HardnessRepository.get_by_id(db, hardness_id)

        if not hardness:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hardness not found"
            )

        hardness_name = hardness_data.hardness_name.strip()

        if not hardness_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Hardness name cannot be empty"
            )

        existing = HardnessRepository.get_by_name(db, hardness_name)

        if existing and existing.id != hardness_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Hardness name already exists"
            )

        try:
            return HardnessRepository.update(
                db, hardness, hardness_name
            )
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Hardness name already exists"
            )

    @staticmethod
    def delete_hardness(db: Session, hardness_id: int):
        hardness = HardnessRepository.get_by_id(db, hardness_id)

        if not hardness:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hardness not found"
            )

        HardnessRepository.delete(db, hardness)

        return {"message": "Hardness permanently deleted"}