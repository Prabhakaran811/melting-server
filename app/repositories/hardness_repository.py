from sqlalchemy.orm import Session

from app.models.hardness import Hardness
from app.schemas.hardness_schema import HardnessCreate


class HardnessRepository:

    @staticmethod
    def create(db: Session, hardness_data: HardnessCreate):
        hardness = Hardness(**hardness_data.model_dump())

        try:
            db.add(hardness)
            db.commit()
            db.refresh(hardness)
            return hardness
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(Hardness)
            .order_by(Hardness.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, hardness_id: int):
        return (
            db.query(Hardness)
            .filter(Hardness.id == hardness_id)
            .first()
        )

    @staticmethod
    def get_by_name(db: Session, hardness_name: str):
        return (
            db.query(Hardness)
            .filter(Hardness.hardness_name == hardness_name)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        hardness: Hardness,
        hardness_name: str
    ):
        try:
            hardness.hardness_name = hardness_name

            db.commit()
            db.refresh(hardness)

            return hardness
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete(db: Session, hardness: Hardness):
        try:
            db.delete(hardness)
            db.commit()
            return True
        except Exception:
            db.rollback()
            raise