
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.furnace_cycle_repository import (
    FurnaceCycleRepository,
)
from app.schemas.furnace_cycle_schema import FurnaceCycleStart


class FurnaceCycleService:

    @staticmethod
    def start_furnace(
        db: Session,
        furnace_id: int,
        data: FurnaceCycleStart,
    ):

        try:
            # Lock the Furnace Master row.
            furnace = FurnaceCycleRepository.get_furnace_for_update(
                db, furnace_id
            )

            if not furnace:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Furnace not found",
                )

            if not furnace.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Furnace is inactive",
                )

            # Prevent another running cycle.
            running_cycle = FurnaceCycleRepository.get_running_cycle(
                db, furnace_id
            )

            if running_cycle:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        f"Furnace already has a running cycle: "
                        f"{running_cycle.heat_no}"
                    ),
                )

            # Validate Order.
            order = FurnaceCycleRepository.get_order(
                db, data.order_id
            )

            if not order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found",
                )

            # Only Pending orders can start.
            if order.status != "Pending":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only Pending orders can start a furnace cycle",
                )

            # Generate global Heat Number.
            heat_no = FurnaceCycleRepository.generate_heat_number(db)

            # Create Furnace Cycle.
            cycle = FurnaceCycleRepository.create(
                db=db,
                furnace=furnace,
                order=order,
                heat_no=heat_no,
            )

            db.commit()
            db.refresh(cycle)

            return cycle

        except HTTPException:
            db.rollback()
            raise

        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "A running cycle already exists for this furnace "
                    "or the Heat Number conflicts"
                ),
            )

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_current_cycle(db: Session, furnace_id: int):

        furnace = FurnaceCycleRepository.get_furnace_for_update(
            db, furnace_id
        )

        if not furnace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Furnace not found",
            )

        return FurnaceCycleRepository.get_current_cycle(
            db, furnace_id
        )

    @staticmethod
    def get_cycle_history(db: Session, furnace_id: int):

        furnace = FurnaceCycleRepository.get_furnace_for_update(
            db, furnace_id
        )

        if not furnace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Furnace not found",
            )

        return FurnaceCycleRepository.get_history(
            db, furnace_id
        )
