from sqlalchemy.orm import Session
from app.models.element import Element


class ElementRepository:

    @staticmethod
    def create(db: Session, data: dict):
        try:
            element = Element(**data)
            db.add(element)
            db.commit()
            db.refresh(element)
            return element
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(Element)
            .order_by(Element.sequence_order.asc(), Element.id.asc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, element_id: int):
        return db.query(Element).filter(
            Element.id == element_id
        ).first()

    @staticmethod
    def get_by_name(db: Session, name: str):
        return db.query(Element).filter(
            Element.name == name
        ).first()

    @staticmethod
    def get_by_abbreviation(db: Session, abbreviation: str):
        return db.query(Element).filter(
            Element.abbreviation == abbreviation
        ).first()

    @staticmethod
    def update(db: Session, element, data: dict):
        try:
            for key, value in data.items():
                setattr(element, key, value)

            db.commit()
            db.refresh(element)
            return element
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete(db: Session, element):
        try:
            db.delete(element)
            db.commit()
        except Exception:
            db.rollback()
            raise