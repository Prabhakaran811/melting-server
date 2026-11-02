from sqlalchemy.orm import Session

from app.models.furnace import Furnace
from app.schemas.furnace_schema import FurnaceCreate


class FurnaceRepository:

    @staticmethod
    def create(db: Session, furnace_data: FurnaceCreate):
        furnace = Furnace(**furnace_data.model_dump())

        try:
            db.add(furnace)
            db.commit()
            db.refresh(furnace)
            return furnace
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(Furnace)
            .order_by(Furnace.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, furnace_id: int):
        return (
            db.query(Furnace)
            .filter(Furnace.id == furnace_id)
            .first()
        )

    @staticmethod
    def get_by_furnace_no(db: Session, furnace_no: str):
        return (
            db.query(Furnace)
            .filter(Furnace.furnace_no == furnace_no)
            .first()
        )

    @staticmethod
    def get_by_ref_no(db: Session, ref_no: str):
        return (
            db.query(Furnace)
            .filter(Furnace.ref_no == ref_no)
            .first()
        )

    @staticmethod
    def update(db: Session, furnace: Furnace, update_data: dict):
        try:
            for field, value in update_data.items():
                setattr(furnace, field, value)

            db.commit()
            db.refresh(furnace)
            return furnace
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def update_status(db: Session, furnace: Furnace, is_active: bool):
        try:
            furnace.is_active = is_active

            db.commit()
            db.refresh(furnace)
            return furnace
        except Exception:
            db.rollback()
            raise