from sqlalchemy.orm import Session
from sqlalchemy import desc, inspect

from app.models.furnace_cycle import FurnaceCycle
from app.models.furnace import Furnace
from app.models.order import Order
from app.models.furnace_charge_mix import (
    FurnaceChargeMix,
    FurnaceChargeItem,
)
from app.models.spectrum_result import SpectrumResult


class ReportRepository:

    @staticmethod
    def serialize_model(obj):
        """
        Serialize actual database columns from any SQLAlchemy model.
        Does not guess column names.
        """
        if obj is None:
            return None

        mapper = inspect(obj.__class__)

        return {
            column.key: getattr(obj, column.key)
            for column in mapper.column_attrs
        }

    @staticmethod
    def get_filtered_cycles(
        db: Session,
        furnace_id: int | None = None,
        heat_no: str | None = None,
        order_number: str | None = None,
        status: str | None = None,
        from_date=None,
        to_date=None,
        page: int = 1,
        page_size: int = 20,
    ):
        query = (
            db.query(FurnaceCycle)
            .join(
                Furnace,
                Furnace.id == FurnaceCycle.furnace_id,
            )
            .join(
                Order,
                Order.id == FurnaceCycle.order_id,
            )
        )

        if furnace_id is not None:
            query = query.filter(
                FurnaceCycle.furnace_id == furnace_id
            )

        if heat_no:
            query = query.filter(
                FurnaceCycle.heat_no.ilike(f"%{heat_no}%")
            )

        if order_number:
            query = query.filter(
                Order.order_number.ilike(f"%{order_number}%")
            )

        if status:
            query = query.filter(
                FurnaceCycle.status.ilike(status)
            )

        if from_date:
            query = query.filter(
                FurnaceCycle.started_at >= from_date
            )

        if to_date:
            query = query.filter(
                FurnaceCycle.started_at < to_date
            )

        total = query.count()

        cycles = (
            query
            .order_by(desc(FurnaceCycle.started_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return cycles, total

    @staticmethod
    def get_cycle_by_id(db: Session, cycle_id: int):
        return (
            db.query(FurnaceCycle)
            .filter(FurnaceCycle.id == cycle_id)
            .first()
        )

    @staticmethod
    def get_furnace(db: Session, furnace_id: int):
        return (
            db.query(Furnace)
            .filter(Furnace.id == furnace_id)
            .first()
        )

    @staticmethod
    def get_order(db: Session, order_id: int):
        return (
            db.query(Order)
            .filter(Order.id == order_id)
            .first()
        )

    @staticmethod
    def get_charge_mix(db: Session, cycle_id: int):
        return (
            db.query(FurnaceChargeMix)
            .filter(
                FurnaceChargeMix.furnace_cycle_id == cycle_id
            )
            .first()
        )

    @staticmethod
    def get_spectrum_results(db: Session, cycle_id: int):
        return (
            db.query(SpectrumResult)
            .filter(
                SpectrumResult.furnace_cycle_id == cycle_id
            )
            .order_by(SpectrumResult.test_number.asc())
            .all()
        )

    @classmethod
    def build_cycle_report(cls, db: Session, cycle: FurnaceCycle):
        furnace = cls.get_furnace(db, cycle.furnace_id)
        order = cls.get_order(db, cycle.order_id)

        charge_mix = cls.get_charge_mix(db, cycle.id)
        spectrum_results = cls.get_spectrum_results(db, cycle.id)

        # Order.aim is an existing relationship in your Order model.
        aim = order.aim if order else None

        charge_mix_data = None
        total_charge_cost = 0

        if charge_mix:
            charge_items = []

            for item in charge_mix.items:
                stock = item.raw_material_stock

                item_data = cls.serialize_model(item)

                # Include raw material stock columns without
                # assuming its actual field names.
                item_data["raw_material_stock"] = (
                    cls.serialize_model(stock)
                )

                item_data["elements"] = []

                for element_row in item.elements:
                    element_data = cls.serialize_model(element_row)
                    element_data["element"] = cls.serialize_model(
                        element_row.element
                    )
                    item_data["elements"].append(element_data)

                item_cost = (
                    float(item.weight or 0)
                    * float(item.rate_per_kg or 0)
                )

                total_charge_cost += item_cost
                item_data["total_cost"] = round(item_cost, 2)

                charge_items.append(item_data)

            charge_mix_data = cls.serialize_model(charge_mix)
            charge_mix_data["items"] = charge_items
            charge_mix_data["total_cost"] = round(
                total_charge_cost, 2
            )

            capacity = float(charge_mix.charging_capacity or 0)
            charged_weight = float(
                charge_mix.total_charged_weight or 0
            )

            charge_mix_data["remaining_capacity"] = round(
                capacity - charged_weight, 3
            )

        spectrum_data = []

        for result in spectrum_results:
            result_data = cls.serialize_model(result)
            result_data["elements"] = [
                cls.serialize_model(element)
                for element in result.elements
            ]
            spectrum_data.append(result_data)

        return {
            "cycle": cls.serialize_model(cycle),
            "furnace": cls.serialize_model(furnace),
            "order": cls.serialize_model(order),
            "aim": cls.serialize_model(aim),
            "charge_mix": charge_mix_data,
            "spectrum_results": spectrum_data,
            "summary": {
                "furnace_capacity": float(
                    cycle.furnace_capacity or 0
                ),
                "total_charged_weight": (
                    float(charge_mix.total_charged_weight or 0)
                    if charge_mix else 0
                ),
                "total_charge_cost": round(total_charge_cost, 2),
                "total_spectrum_tests": len(spectrum_results),
                "cycle_status": cycle.status,
                "started_at": cycle.started_at,
                "completed_at": cycle.completed_at,
            },
        }