from sqlalchemy.orm import Session, selectinload

from app.models.raw_material import RawMaterial
from app.models.element import Element


class RawMaterialRepository:

    @staticmethod
    def create(db: Session, name: str, elements: list):
        try:
            raw_material = RawMaterial(
                name=name,
                elements=elements
            )

            db.add(raw_material)
            db.commit()
            db.refresh(raw_material)

            return raw_material

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(RawMaterial)
            .options(
                selectinload(RawMaterial.elements)
                .selectinload(Element.iron_types)
            )
            .order_by(RawMaterial.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, raw_material_id: int):
        return (
            db.query(RawMaterial)
            .options(
                selectinload(RawMaterial.elements)
                .selectinload(Element.iron_types)
            )
            .filter(RawMaterial.id == raw_material_id)
            .first()
        )

    @staticmethod
    def get_by_name(db: Session, name: str):
        return db.query(RawMaterial).filter(
            RawMaterial.name == name
        ).first()

    @staticmethod
    def get_elements_by_ids(db: Session, element_ids: list[int]):
        return db.query(Element).filter(
            Element.id.in_(element_ids)
        ).all()

    @staticmethod
    def update(db: Session, raw_material, name: str, elements: list):
        try:
            raw_material.name = name
            raw_material.elements = elements

            db.commit()
            db.refresh(raw_material)

            return raw_material

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete(db: Session, raw_material):
        try:
            db.delete(raw_material)
            db.commit()

        except Exception:
            db.rollback()
            raise