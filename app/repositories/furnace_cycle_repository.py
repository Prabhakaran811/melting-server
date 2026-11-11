
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.furnace import Furnace
from app.models.order import Order
from app.models.furnace_cycle import FurnaceCycle


class FurnaceCycleRepository:

    @staticmethod
    def get_furnace_for_update(db: Session, furnace_id: int):
        return (
            db.query(Furnace)
            .filter(Furnace.id == furnace_id)
            .with_for_update(of=Furnace)
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
    def get_running_cycle(db: Session, furnace_id: int):
        return (
            db.query(FurnaceCycle)
            .filter(
                FurnaceCycle.furnace_id == furnace_id,
                FurnaceCycle.status == "Running",
            )
            .first()
        )

    @staticmethod
    def generate_heat_number(db: Session) -> str:
        result = db.execute(
            text("SELECT nextval('furnace_heat_number_seq')")
        )
        sequence_number = result.scalar_one()

        return f"H{sequence_number:05d}"

    @staticmethod
    def create(
        db: Session,
        furnace: Furnace,
        order: Order,
        heat_no: str,
    ):
        cycle = FurnaceCycle(
            furnace_id=furnace.id,
            order_id=order.id,
            heat_no=heat_no,
            furnace_capacity=furnace.capacity,
            status="Running",
            active_stage="Charging",
        )

        db.add(cycle)
        db.flush()

        return cycle

    @staticmethod
    def get_by_id(db: Session, cycle_id: int):
        return (
            db.query(FurnaceCycle)
            .filter(FurnaceCycle.id == cycle_id)
            .first()
        )

    @staticmethod
    def get_current_cycle(db: Session, furnace_id: int):
        return FurnaceCycleRepository.get_running_cycle(
            db, furnace_id
        )

    @staticmethod
    def get_history(db: Session, furnace_id: int):
        return (
            db.query(FurnaceCycle)
            .filter(FurnaceCycle.furnace_id == furnace_id)
            .order_by(FurnaceCycle.id.desc())
            .all()
        )
