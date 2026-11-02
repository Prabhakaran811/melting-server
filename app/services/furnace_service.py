from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.furnace_repository import FurnaceRepository
from app.schemas.furnace_schema import FurnaceCreate, FurnaceUpdate


class FurnaceService:

    @staticmethod
    def create_furnace(db: Session, furnace_data: FurnaceCreate):

        if FurnaceRepository.get_by_furnace_no(
            db, furnace_data.furnace_no
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Furnace number already exists"
            )

        if FurnaceRepository.get_by_ref_no(db, furnace_data.ref_no):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Reference number already exists"
            )

        try:
            return FurnaceRepository.create(db, furnace_data)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Furnace number or reference number already exists"
            )

    @staticmethod
    def get_furnaces(db: Session):
        return FurnaceRepository.get_all(db)

    @staticmethod
    def update_furnace(
        db: Session,
        furnace_id: int,
        furnace_data: FurnaceUpdate
    ):
        furnace = FurnaceRepository.get_by_id(db, furnace_id)

        if not furnace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Furnace not found"
            )

        update_data = furnace_data.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update"
            )

        furnace_no = update_data.get("furnace_no")
        ref_no = update_data.get("ref_no")

        if furnace_no and furnace_no != furnace.furnace_no:
            existing = FurnaceRepository.get_by_furnace_no(db, furnace_no)

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Furnace number already exists"
                )

        if ref_no and ref_no != furnace.ref_no:
            existing = FurnaceRepository.get_by_ref_no(db, ref_no)

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Reference number already exists"
                )

        try:
            return FurnaceRepository.update(db, furnace, update_data)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Furnace number or reference number already exists"
            )

    @staticmethod
    def update_furnace_status(
        db: Session,
        furnace_id: int,
        is_active: bool
    ):
        furnace = FurnaceRepository.get_by_id(db, furnace_id)

        if not furnace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Furnace not found"
            )

        return FurnaceRepository.update_status(db, furnace, is_active)