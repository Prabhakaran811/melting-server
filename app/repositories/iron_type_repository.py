from sqlalchemy.orm import Session, selectinload

from app.models.iron_type import IronType
from app.models.element import Element


class IronTypeRepository:

    @staticmethod
    def create(db: Session, name: str, elements: list):
        try:
            iron_type = IronType(
                name=name,
                elements=elements
            )

            db.add(iron_type)
            db.commit()
            db.refresh(iron_type)

            return iron_type

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(IronType)
            .options(selectinload(IronType.elements))
            .order_by(IronType.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, iron_type_id: int):
        return (
            db.query(IronType)
            .options(selectinload(IronType.elements))
            .filter(IronType.id == iron_type_id)
            .first()
        )

    @staticmethod
    def get_by_name(db: Session, name: str):
        return db.query(IronType).filter(
            IronType.name == name
        ).first()

    @staticmethod
    def get_elements_by_ids(db: Session, element_ids: list[int]):
        return db.query(Element).filter(
            Element.id.in_(element_ids)
        ).all()

    @staticmethod
    def update(db: Session, iron_type, name: str, elements: list):
        try:
            iron_type.name = name
            iron_type.elements = elements

            db.commit()
            db.refresh(iron_type)

            return iron_type

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete(db: Session, iron_type):
        try:
            db.delete(iron_type)
            db.commit()

        except Exception:
            db.rollback()
            raise