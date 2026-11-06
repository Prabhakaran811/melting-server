from sqlalchemy.orm import Session, joinedload, selectinload

from app.models.aim import Aim, AimElement


class AimRepository:

    @staticmethod
    def get_query(db: Session):
        return (
            db.query(Aim)
            .options(
                joinedload(Aim.customer),
                joinedload(Aim.product),
                joinedload(Aim.iron_type),
                joinedload(Aim.packing),
                joinedload(Aim.hardness),
                joinedload(Aim.inoculant),
                selectinload(Aim.elements).joinedload(
                    AimElement.element
                ),
            )
        )

    @staticmethod
    def create(db: Session, data: dict):

        try:
            element_data = data.pop("elements")

            aim = Aim(**data)

            for item in element_data:
                aim.elements.append(
                    AimElement(**item)
                )

            db.add(aim)
            db.commit()
            db.refresh(aim)

            return AimRepository.get_by_id(db, aim.id)

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session):

        return (
            AimRepository.get_query(db)
            .order_by(Aim.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, aim_id: int):

        return (
            AimRepository.get_query(db)
            .filter(Aim.id == aim_id)
            .first()
        )

    @staticmethod
    def update(db: Session, aim: Aim, data: dict):

        try:
            element_data = data.pop("elements")

            for key, value in data.items():
                setattr(aim, key, value)

            # Replace the existing element specifications.
            aim.elements.clear()

            for item in element_data:
                aim.elements.append(
                    AimElement(**item)
                )

            db.commit()
            db.refresh(aim)

            return AimRepository.get_by_id(db, aim.id)

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete(db: Session, aim: Aim):

        try:
            db.delete(aim)
            db.commit()

            return True

        except Exception:
            db.rollback()
            raise