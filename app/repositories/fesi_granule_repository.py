from sqlalchemy.orm import Session
from app.models.fesi_granule import FeSiGranule


class FeSiGranuleRepository:

    @staticmethod
    def create(db: Session, name: str):
        try:
            granule = FeSiGranule(name=name)
            db.add(granule)
            db.commit()
            db.refresh(granule)
            return granule
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(FeSiGranule)
            .order_by(FeSiGranule.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, granule_id: int):
        return db.query(FeSiGranule).filter(
            FeSiGranule.id == granule_id
        ).first()

    @staticmethod
    def get_by_name(db: Session, name: str):
        return db.query(FeSiGranule).filter(
            FeSiGranule.name == name
        ).first()

    @staticmethod
    def update(db: Session, granule, name: str):
        try:
            granule.name = name
            db.commit()
            db.refresh(granule)
            return granule
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete(db: Session, granule):
        try:
            db.delete(granule)
            db.commit()
        except Exception:
            db.rollback()
            raise