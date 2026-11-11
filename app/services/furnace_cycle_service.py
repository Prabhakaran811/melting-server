
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.furnace import Furnace
from app.models.order import Order

from app.models.furnace_cycle import (
    FurnaceCycle,
    FurnaceCycleStage
)

from app.repositories.furnace_cycle_repository import (
    FurnaceCycleRepository
)

from app.schemas.furnace_cycle_schema import (
    FurnaceCycleStart
)


class FurnaceCycleService:

    @staticmethod
    def start_cycle(
        db: Session,
        furnace_id: int,
        data: FurnaceCycleStart
    ):

        furnace = (
            db.query(Furnace)
            .filter(
                Furnace.id == furnace_id,
                Furnace.is_active == True
            )
            .first()
        )

        if not furnace:
            raise HTTPException(
                status_code=404,
                detail="Furnace not found or inactive"
            )

        order = (
            db.query(Order)
            .filter(Order.id == data.order_id)
            .first()
        )

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Selected order not found"
            )

        if order.status in ["Completed", "Cancelled"]:
            raise HTTPException(
                status_code=400,
                detail="Cannot start a cycle for a completed or cancelled order"
            )

        if furnace.capacity is None or furnace.capacity <= 0:
            raise HTTPException(
                status_code=400,
                detail="Furnace capacity is not configured"
            )

        existing_cycle = (
            FurnaceCycleRepository.get_running_by_furnace(
                db,
                furnace_id
            )
        )

        if existing_cycle:
            raise HTTPException(
                status_code=409,
                detail=(
                    f"Furnace already has an active cycle: "
                    f"{existing_cycle.heat_no}"
                )
            )

        cycle = FurnaceCycle(
            furnace_id=furnace.id,
            order_id=order.id,
            furnace_capacity=furnace.capacity,
            status="Running",
            active_stage="Started",
            shift=data.shift
        )

        try:
            created_cycle = FurnaceCycleRepository.create(
                db,
                cycle
            )

            initial_stage = FurnaceCycleStage(
                furnace_cycle_id=created_cycle.id,
                stage_name="Started"
            )

            FurnaceCycleRepository.add_stage(
                db,
                initial_stage
            )

            return FurnaceCycleRepository.get_by_id(
                db,
                created_cycle.id
            )

        except IntegrityError:
            db.rollback()

            raise HTTPException(
                status_code=409,
                detail="Another operator has already started a cycle on this furnace"
            )

    @staticmethod
    def get_current_cycle(
        db: Session,
        furnace_id: int
    ):

        furnace = (
            db.query(Furnace)
            .filter(Furnace.id == furnace_id)
            .first()
        )

        if not furnace:
            raise HTTPException(
                status_code=404,
                detail="Furnace not found"
            )

        return FurnaceCycleRepository.get_running_by_furnace(
            db,
            furnace_id
        )

    @staticmethod
    def get_cycle_history(
        db: Session,
        furnace_id: int
    ):

        furnace = (
            db.query(Furnace)
            .filter(Furnace.id == furnace_id)
            .first()
        )

        if not furnace:
            raise HTTPException(
                status_code=404,
                detail="Furnace not found"
            )

        return FurnaceCycleRepository.get_all_by_furnace(
            db,
            furnace_id
        )
