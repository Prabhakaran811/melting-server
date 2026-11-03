from sqlalchemy.orm import Session
from app.models.packing import Packing


class PackingRepository:

    @staticmethod
    def create(db: Session, name: str):
        try:
            packing = Packing(name=name)
            db.add(packing)
            db.commit()
            db.refresh(packing)
            return packing
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(Packing)
            .order_by(Packing.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, packing_id: int):
        return db.query(Packing).filter(
            Packing.id == packing_id
        ).first()

    @staticmethod
    def get_by_name(db: Session, name: str):
        return db.query(Packing).filter(
            Packing.name == name
        ).first()

    @staticmethod
    def update(db: Session, packing, name: str):
        try:
            packing.name = name
            db.commit()
            db.refresh(packing)
            return packing
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete(db: Session, packing):
        try:
            db.delete(packing)
            db.commit()
        except Exception:
            db.rollback()
            raise