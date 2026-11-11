
from datetime import datetime, timezone
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.furnace_charge_mix_repository import (
    FurnaceChargeMixRepository as Repository,
)
from app.schemas.furnace_charge_mix_schema import (
    FurnaceChargeItemCreate,
    FurnaceChargeItemUpdate,
)
from app.models.furnace_charge_mix import (
    FurnaceChargeMix,
    FurnaceChargeItem,
)


class FurnaceChargeMixService:

    @staticmethod
    def _get_running_cycle(db: Session, furnace_id: int):
        cycle = Repository.get_running_cycle(db, furnace_id)

        if not cycle:
            raise HTTPException(
                status_code=404,
                detail="No running furnace cycle found",
            )

        return cycle

    @staticmethod
    def _get_draft_mix(db: Session, cycle_id: int):
        mix = Repository.get_mix_for_update(db, cycle_id)

        if not mix:
            raise HTTPException(
                status_code=404,
                detail="Charge Mix not found",
            )

        if mix.status != "Draft":
            raise HTTPException(
                status_code=409,
                detail="Charge Mix is confirmed and cannot be modified",
            )

        return mix

    @staticmethod
    def _validate_stock_usage(
        db: Session,
        mix: FurnaceChargeMix,
        stock_id: int,
        requested_weight: Decimal,
        exclude_item_id: int | None = None,
    ):
        stock = Repository.get_stock_for_update(db, stock_id)

        if not stock:
            raise HTTPException(
                status_code=404,
                detail="Raw material stock not found",
            )

        if stock.quantity <= 0:
            raise HTTPException(
                status_code=400,
                detail="Raw material stock is unavailable",
            )

        existing_weight = sum(
            (
                item.weight
                for item in mix.items
                if item.raw_material_stock_id == stock_id
                and item.id != exclude_item_id
            ),
            start=Decimal("0"),
        )

        if existing_weight + requested_weight > stock.quantity:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Insufficient stock. Available: {stock.quantity}, "
                    f"already added to this Charge Mix: {existing_weight}, "
                    f"requested: {requested_weight}"
                ),
            )

        return stock

    @staticmethod
    def _validate_capacity(
        mix: FurnaceChargeMix,
        requested_weight: Decimal,
        old_weight: Decimal = Decimal("0"),
    ):
        new_total = (
            mix.total_charged_weight
            - old_weight
            + requested_weight
        )

        if new_total > mix.charging_capacity:
            remaining = (
                mix.charging_capacity
                - mix.total_charged_weight
                + old_weight
            )

            raise HTTPException(
                status_code=400,
                detail=f"Furnace capacity exceeded. Remaining capacity: {remaining}",
            )

        if new_total < 0:
            raise HTTPException(
                status_code=400,
                detail="Invalid charge weight",
            )

        return new_total

    @staticmethod
    def _build_response(mix: FurnaceChargeMix):
        total_weight = Decimal(str(mix.total_charged_weight))
        capacity = Decimal(str(mix.charging_capacity))

        remaining_capacity = capacity - total_weight

        element_totals = {}

        for item in mix.items:
            item_weight = Decimal(str(item.weight))

            for item_element in item.elements:
                element_id = item_element.element_id
                percentage = Decimal(str(item_element.percentage))

                if element_id not in element_totals:
                    element_totals[element_id] = {
                        "element_id": element_id,
                        "element_name": item_element.element.name,
                        "abbreviation": item_element.element.abbreviation,
                        "weighted_value": Decimal("0"),
                    }

                element_totals[element_id]["weighted_value"] += (
                    item_weight * percentage / Decimal("100")
                )

        composition = []

        if total_weight > 0:
            for element in element_totals.values():
                average_percentage = (
                    element["weighted_value"]
                    / total_weight
                    * Decimal("100")
                )

                composition.append({
                    "element_id": element["element_id"],
                    "element_name": element["element_name"],
                    "abbreviation": element["abbreviation"],
                    "percentage": average_percentage.quantize(
                        Decimal("0.0001")
                    ),
                })

        composition.sort(
            key=lambda element: element["element_id"]
        )

        items = []

        for item in mix.items:
            items.append({
                "id": item.id,
                "charge_mix_id": item.charge_mix_id,
                "raw_material_stock_id": item.raw_material_stock_id,
                "weight": item.weight,
                "rate_per_kg": item.rate_per_kg,
                "bunker_name": item.bunker_name,
                "elements": [
                    {
                        "element_id": element.element_id,
                        "percentage": element.percentage,
                        "element_name": element.element.name,
                        "abbreviation": element.element.abbreviation,
                    }
                    for element in item.elements
                ],
            })

        return {
            "id": mix.id,
            "furnace_cycle_id": mix.furnace_cycle_id,
            "charging_capacity": capacity,
            "total_charged_weight": total_weight,
            "remaining_capacity": remaining_capacity,
            "status": mix.status,
            "confirmed_at": mix.confirmed_at,
            "items": items,
            "element_composition": composition,
        }

    @staticmethod
    def create_charge_mix(db: Session, furnace_id: int):
        try:
            cycle = FurnaceChargeMixService._get_running_cycle(
                db, furnace_id
            )

            existing = Repository.get_mix_by_cycle(db, cycle.id)

            if existing:
                raise HTTPException(
                    status_code=409,
                    detail="Charge Mix already exists for this furnace cycle",
                )

            mix = Repository.create_mix(db, cycle)

            db.commit()

            mix = Repository.get_mix_by_id(db, mix.id)

            return FurnaceChargeMixService._build_response(mix)

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_charge_mix(db: Session, furnace_id: int):
        cycle = Repository.get_running_cycle(db, furnace_id)

        if not cycle:
            raise HTTPException(
                status_code=404,
                detail="No running furnace cycle found",
            )

        mix = Repository.get_mix_by_cycle(db, cycle.id)

        if not mix:
            raise HTTPException(
                status_code=404,
                detail="Charge Mix not created for this furnace cycle",
            )

        return FurnaceChargeMixService._build_response(mix)

    @staticmethod
    def add_charge_item(
        db: Session,
        furnace_id: int,
        data: FurnaceChargeItemCreate,
    ):
        try:
            cycle = FurnaceChargeMixService._get_running_cycle(
                db, furnace_id
            )

            mix = FurnaceChargeMixService._get_draft_mix(
                db, cycle.id
            )

            mix = Repository.get_mix_by_id(db, mix.id)

            requested_weight = data.weight

            new_total = FurnaceChargeMixService._validate_capacity(
                mix,
                requested_weight,
            )

            stock = FurnaceChargeMixService._validate_stock_usage(
                db,
                mix,
                data.raw_material_stock_id,
                requested_weight,
            )

            Repository.add_item(
                db=db,
                mix_id=mix.id,
                stock=stock,
                weight=requested_weight,
                bunker_name=data.bunker_name,
            )

            mix.total_charged_weight = new_total

            db.commit()

            mix = Repository.get_mix_by_id(db, mix.id)

            return FurnaceChargeMixService._build_response(mix)

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def update_charge_item(
        db: Session,
        furnace_id: int,
        item_id: int,
        data: FurnaceChargeItemUpdate,
    ):
        try:
            cycle = FurnaceChargeMixService._get_running_cycle(
                db, furnace_id
            )

            mix = FurnaceChargeMixService._get_draft_mix(
                db, cycle.id
            )

            mix = Repository.get_mix_by_id(db, mix.id)

            item = Repository.get_item(
                db,
                mix.id,
                item_id,
            )

            if not item:
                raise HTTPException(
                    status_code=404,
                    detail="Charge item not found",
                )

            update_data = data.model_dump(exclude_unset=True)

            if not update_data:
                raise HTTPException(
                    status_code=400,
                    detail="No fields provided for update",
                )

            stock_id = update_data.get(
                "raw_material_stock_id",
                item.raw_material_stock_id,
            )

            weight = update_data.get("weight", item.weight)

            bunker_name = update_data.get(
                "bunker_name",
                item.bunker_name,
            )

            old_weight = Decimal(str(item.weight))
            requested_weight = Decimal(str(weight))

            new_total = FurnaceChargeMixService._validate_capacity(
                mix,
                requested_weight,
                old_weight,
            )

            stock = FurnaceChargeMixService._validate_stock_usage(
                db,
                mix,
                stock_id,
                requested_weight,
                exclude_item_id=item.id,
            )

            Repository.update_item(
                db=db,
                item=item,
                stock=stock,
                weight=requested_weight,
                bunker_name=bunker_name,
            )

            mix.total_charged_weight = new_total

            db.commit()

            mix = Repository.get_mix_by_id(db, mix.id)

            return FurnaceChargeMixService._build_response(mix)

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete_charge_item(
        db: Session,
        furnace_id: int,
        item_id: int,
    ):
        try:
            cycle = FurnaceChargeMixService._get_running_cycle(
                db, furnace_id
            )

            mix = FurnaceChargeMixService._get_draft_mix(
                db, cycle.id
            )

            mix = Repository.get_mix_by_id(db, mix.id)

            item = Repository.get_item(
                db,
                mix.id,
                item_id,
            )

            if not item:
                raise HTTPException(
                    status_code=404,
                    detail="Charge item not found",
                )

            mix.total_charged_weight -= item.weight

            Repository.delete_item(db, item)

            db.commit()

            return {
                "success": True,
                "message": "Charge item deleted successfully",
                "total_charged_weight": mix.total_charged_weight,
            }

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def confirm_charge_mix(db: Session, furnace_id: int):
        try:
            cycle = FurnaceChargeMixService._get_running_cycle(
                db, furnace_id
            )

            mix = FurnaceChargeMixService._get_draft_mix(
                db, cycle.id
            )

            if mix.total_charged_weight <= 0:
                raise HTTPException(
                    status_code=400,
                    detail="Cannot confirm an empty Charge Mix",
                )

            mix.status = "Confirmed"
            mix.confirmed_at = datetime.now(timezone.utc)

            cycle.active_stage = "Spectrum Testing"

            db.commit()

            mix = Repository.get_mix_by_id(db, mix.id)

            return FurnaceChargeMixService._build_response(mix)

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise
