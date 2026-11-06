from sqlalchemy.orm import Session

from app.models.aim import Aim

from app.models.customer import Customer
from app.models.product import Product
from app.models.iron_type import IronType
from app.models.packing import Packing
from app.models.hardness import Hardness
from app.models.inoculant import Inoculant

from app.repositories.aim_repository import AimRepository


class AimService:

    @staticmethod
    def validate_references(db: Session, data):

        # Validate Customer
        customer = db.get(Customer, data.customer_id)

        if not customer:
            raise ValueError("Selected Customer does not exist")

        # Validate Product
        product = db.get(Product, data.product_id)

        if not product:
            raise ValueError("Selected Product does not exist")

        # Validate Iron Type
        iron_type = db.get(IronType, data.iron_type_id)

        if not iron_type:
            raise ValueError("Selected Iron Type does not exist")

        # Validate Packing
        packing = db.get(Packing, data.packing_id)

        if not packing:
            raise ValueError("Selected Packing does not exist")

        # Validate Hardness
        hardness = db.get(Hardness, data.hardness_id)

        if not hardness:
            raise ValueError("Selected Hardness does not exist")

        # Validate Inoculant
        inoculant = db.get(Inoculant, data.inoculant_id)

        if not inoculant:
            raise ValueError("Selected Inoculant does not exist")

        # Get all Elements belonging to selected Iron Type
        valid_element_ids = {
            element.id for element in iron_type.elements
        }

        submitted_element_ids = [
            item.element_id for item in data.elements
        ]

        # Check duplicate Elements
        if len(submitted_element_ids) != len(set(submitted_element_ids)):
            raise ValueError(
                "Duplicate Elements are not allowed"
            )

        submitted_ids = set(submitted_element_ids)

        # Check Elements not belonging to Iron Type
        invalid_ids = submitted_ids - valid_element_ids

        if invalid_ids:
            raise ValueError(
                f"Elements {sorted(invalid_ids)} do not belong "
                "to the selected Iron Type"
            )

        # Require every Element of the Iron Type
        missing_ids = valid_element_ids - submitted_ids

        if missing_ids:
            raise ValueError(
                f"Missing Element values for IDs: {sorted(missing_ids)}"
            )

    @staticmethod
    def create_aim(db: Session, data):

        AimService.validate_references(db, data)

        aim_data = data.model_dump()

        return AimRepository.create(db, aim_data)

    @staticmethod
    def get_aims(db: Session):

        return AimRepository.get_all(db)

    @staticmethod
    def get_aim(db: Session, aim_id: int):

        aim = AimRepository.get_by_id(db, aim_id)

        if not aim:
            raise LookupError("Aim not found")

        return aim

    @staticmethod
    def update_aim(db: Session, aim_id: int, data):

        aim = AimRepository.get_by_id(db, aim_id)

        if not aim:
            raise LookupError("Aim not found")

        AimService.validate_references(db, data)

        aim_data = data.model_dump()

        return AimRepository.update(
            db,
            aim,
            aim_data,
        )

    @staticmethod
    def delete_aim(db: Session, aim_id: int):

        aim = AimRepository.get_by_id(db, aim_id)

        if not aim:
            raise LookupError("Aim not found")

        return AimRepository.delete(db, aim)