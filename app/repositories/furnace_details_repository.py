
from sqlalchemy.orm import Session, joinedload, selectinload

from app import db
from app.models.furnace import Furnace
from app.models.furnace_cycle import FurnaceCycle
from app.models.furnace_charge_mix import (
    FurnaceChargeMix,
    FurnaceChargeItem,
    FurnaceChargeItemElement,
)
from app.models.spectrum_result import SpectrumResult
from app.models.order import Order
from sqlalchemy.orm import joinedload
from app.models.aim import Aim


class FurnaceDetailsRepository:

    @staticmethod
    def get_furnace(db: Session, furnace_id: int):
        return (
            db.query(Furnace)
            .filter(Furnace.id == furnace_id)
            .first()
        )

    @staticmethod
    def get_current_cycle(db: Session, furnace_id: int):
        return (
            db.query(FurnaceCycle)
            .filter(
                FurnaceCycle.furnace_id == furnace_id,
                FurnaceCycle.status == "Running",
            )
            .first()
        )

    @staticmethod
    def get_charge_mix(db: Session, cycle_id: int):
        return (
            db.query(FurnaceChargeMix)
            .options(
                selectinload(FurnaceChargeMix.items)
                .selectinload(FurnaceChargeItem.raw_material_stock),

                selectinload(FurnaceChargeMix.items)
                .selectinload(FurnaceChargeItem.elements)
                .joinedload(FurnaceChargeItemElement.element),
            )
            .filter(
                FurnaceChargeMix.furnace_cycle_id == cycle_id
            )
            .first()
        )

    @staticmethod
    def get_spectrum_results(db: Session, cycle_id: int):
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
    def get_order(db: Session, order_id: int):
        return (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )
    

    @staticmethod
    def get_current_cycle_for_update(db: Session, furnace_id: int):
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
    def get_cycle_history(db: Session, furnace_id: int):
        return (
            db.query(FurnaceCycle)
            .filter(
                FurnaceCycle.furnace_id == furnace_id,
                FurnaceCycle.status == "Completed",
            )
            .order_by(FurnaceCycle.started_at.desc())
            .all()
        )
