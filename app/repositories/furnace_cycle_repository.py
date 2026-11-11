

from uuid import uuid4

from sqlalchemy.orm import Session, joinedload, selectinload

from app.models.furnace_cycle import (
    FurnaceCycle,
    FurnaceCycleStage
)


class FurnaceCycleRepository:

    @staticmethod
    def get_by_id(db: Session, cycle_id: int):
        return (
            db.query(FurnaceCycle)
            .options(
                joinedload(FurnaceCycle.furnace),
                joinedload(FurnaceCycle.order),
                selectinload(FurnaceCycle.stages)
            )
            .filter(FurnaceCycle.id == cycle_id)
            .first()
        )

    @staticmethod
    def get_running_by_furnace(db: Session, furnace_id: int):
        return (
            db.query(FurnaceCycle)
            .options(
                joinedload(FurnaceCycle.furnace),
                joinedload(FurnaceCycle.order),
                selectinload(FurnaceCycle.stages)
            )
            .filter(
                FurnaceCycle.furnace_id == furnace_id,
                FurnaceCycle.status == "Running"
            )
            .first()
        )

    @staticmethod
    def get_all_by_furnace(db: Session, furnace_id: int):
        return (
            db.query(FurnaceCycle)
            .options(
                joinedload(FurnaceCycle.order),
                selectinload(FurnaceCycle.stages)
            )
            .filter(FurnaceCycle.furnace_id == furnace_id)
            .order_by(FurnaceCycle.id.desc())
            .all()
        )

    @staticmethod
    def create(db: Session, cycle: FurnaceCycle):
        try:
            # Temporary unique value within VARCHAR(30)
            cycle.heat_no = f"TEMP-{uuid4().hex[:20]}"

            db.add(cycle)
            db.flush()

            # Generate final heat number from database ID
            cycle.heat_no = f"HEAT-{cycle.id:06d}"

            db.commit()

            return FurnaceCycleRepository.get_by_id(
                db,
                cycle.id
            )

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def update(db: Session, cycle: FurnaceCycle):
        try:
            db.commit()

            return FurnaceCycleRepository.get_by_id(
                db,
                cycle.id
            )

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def add_stage(db: Session, stage: FurnaceCycleStage):
        try:
            db.add(stage)
            db.commit()
            db.refresh(stage)
            return stage

        except Exception:
            db.rollback()
            raise
