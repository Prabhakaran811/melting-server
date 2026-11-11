
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.furnace import Furnace
from app.models.furnace_cycle import FurnaceCycle
from app.models.furnace_charge_mix import FurnaceChargeMix
from app.models.spectrum_result import (
    SpectrumResult,
)


class SpectrumResultRepository:

    @staticmethod
    def get_furnace_by_number(db: Session, furnace_no: str):
        return (
            db.query(Furnace)
            .filter(
                Furnace.furnace_no == furnace_no,
                Furnace.is_active.is_(True),
            )
            .first()
        )

    @staticmethod
    def get_running_cycle_for_update(
        db: Session,
        furnace_id: int,
    ):
        return (
            db.query(FurnaceCycle)
            .filter(
                FurnaceCycle.furnace_id == furnace_id,
                FurnaceCycle.status == "Running",
            )
            .with_for_update()
            .first()
        )

    @staticmethod
    def get_confirmed_charge_mix(
        db: Session,
        cycle_id: int,
    ):
        return (
            db.query(FurnaceChargeMix)
            .filter(
                FurnaceChargeMix.furnace_cycle_id == cycle_id,
                FurnaceChargeMix.status == "Confirmed",
            )
            .first()
        )

    @staticmethod
    def get_next_test_number(
        db: Session,
        cycle_id: int,
    ) -> int:
        current_number = (
            db.query(
                func.max(SpectrumResult.test_number)
            )
            .filter(
                SpectrumResult.furnace_cycle_id == cycle_id
            )
            .scalar()
        )

        return (current_number or 0) + 1

    @staticmethod
    def create_result(
        db: Session,
        result: SpectrumResult,
    ):
        db.add(result)
        db.flush()
        return result

    @staticmethod
    def get_result_by_id(
        db: Session,
        result_id: int,
    ):
        return (
            db.query(SpectrumResult)
            .options(
                joinedload(SpectrumResult.elements)
            )
            .filter(SpectrumResult.id == result_id)
            .first()
        )

    @staticmethod
    def get_results_by_cycle(
        db: Session,
        cycle_id: int,
    ):
        return (
            db.query(SpectrumResult)
            .options(
                joinedload(SpectrumResult.elements)
            )
            .filter(
                SpectrumResult.furnace_cycle_id == cycle_id
            )
            .order_by(SpectrumResult.test_number.asc())
            .all()
        )

    @staticmethod
    def get_results_by_furnace(
        db: Session,
        furnace_id: int,
    ):
        return (
            db.query(SpectrumResult)
            .join(
                FurnaceCycle,
                FurnaceCycle.id == SpectrumResult.furnace_cycle_id,
            )
            .options(
                joinedload(SpectrumResult.elements)
            )
            .filter(
                FurnaceCycle.furnace_id == furnace_id
            )
            .order_by(SpectrumResult.received_at.desc())
            .all()
        )
