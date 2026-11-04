from sqlalchemy.orm import Session, selectinload

from app.models.wire import Wire
from app.models.raw_material import RawMaterial


class WireRepository:

    @staticmethod
    def create(db: Session, name: str, raw_material_id: int):
        try:
            wire = Wire(
                name=name,
                raw_material_id=raw_material_id
            )

            db.add(wire)
            db.commit()
            db.refresh(wire)

            return WireRepository.get_by_id(db, wire.id)

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(Wire)
            .options(selectinload(Wire.raw_material))
            .order_by(Wire.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, wire_id: int):
        return (
            db.query(Wire)
            .options(selectinload(Wire.raw_material))
            .filter(Wire.id == wire_id)
            .first()
        )

    @staticmethod
    def get_by_name(db: Session, name: str):
        return (
            db.query(Wire)
            .filter(Wire.name == name)
            .first()
        )

    @staticmethod
    def get_raw_material_by_id(
        db: Session,
        raw_material_id: int
    ):
        return (
            db.query(RawMaterial)
            .filter(RawMaterial.id == raw_material_id)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        wire: Wire,
        name: str,
        raw_material_id: int
    ):
        try:
            wire.name = name
            wire.raw_material_id = raw_material_id

            db.commit()
            db.refresh(wire)

            return WireRepository.get_by_id(db, wire.id)

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete(db: Session, wire: Wire):
        try:
            db.delete(wire)
            db.commit()

        except Exception:
            db.rollback()
            raise