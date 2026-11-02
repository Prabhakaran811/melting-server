from sqlalchemy.orm import Session
from app.models.inoculant import Inoculant


class InoculantRepository:

    @staticmethod
    def create(db: Session, name: str):
        try:
            inoculant = Inoculant(name=name)
            db.add(inoculant)
            db.commit()
            db.refresh(inoculant)
            return inoculant
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(Inoculant)
            .order_by(Inoculant.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, inoculant_id: int):
        return db.query(Inoculant).filter(
            Inoculant.id == inoculant_id
        ).first()

    @staticmethod
    def get_by_name(db: Session, name: str):
        return db.query(Inoculant).filter(
            Inoculant.name == name
        ).first()

    @staticmethod
    def update(db: Session, inoculant, name: str):
        try:
            inoculant.name = name
            db.commit()
            db.refresh(inoculant)
            return inoculant
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete(db: Session, inoculant):
        try:
            db.delete(inoculant)
            db.commit()
        except Exception:
            db.rollback()
            raise