
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.furnace_details_repository import (
    FurnaceDetailsRepository,
)


class FurnaceDetailsService:

    # --------------------------------------------------
    # MASTER DATA SERIALIZER
    # --------------------------------------------------

    @staticmethod
    def serialize_master(master):
        if master is None:
            return None

        return {
            "id": master.id,
            "name": getattr(master, "name", None),
        }

    # --------------------------------------------------
    # AIM SERIALIZER
    # --------------------------------------------------

    @staticmethod
    def serialize_aim(aim):

        if aim is None:
            return None

        aim_composition = {}

        for item in aim.elements:

            # Element model uses abbreviation, not symbol
            abbreviation = (
                item.element.abbreviation
                if item.element else None
            )

            if not abbreviation:
                continue

            exact = float(item.exact_value)
            plus = float(item.plus_value)
            minus = float(item.minus_value)

            aim_composition[abbreviation] = {
                "exact_value": exact,
                "plus_value": plus,
                "minus_value": minus,
                "min_value": exact - minus,
                "max_value": exact + plus,
            }

        return {
            "id": aim.id,
            "drawing_no": aim.drawing_no,

            "product": FurnaceDetailsService.serialize_master(
                aim.product
            ),

            "customer": FurnaceDetailsService.serialize_master(
                aim.customer
            ),

            "grade": FurnaceDetailsService.serialize_master(
                aim.iron_type
            ),

            "packing": FurnaceDetailsService.serialize_master(
                aim.packing
            ),

            "hardness": FurnaceDetailsService.serialize_master(
                aim.hardness
            ),

            "inoculant": FurnaceDetailsService.serialize_master(
                aim.inoculant
            ),

            "pouring_weight_kg": float(
                aim.pouring_weight_kg
            ),

            "casting_weight_kg": float(
                aim.casting_weight_kg
            ),

            "no_of_casting": aim.no_of_casting,
            "no_of_cavity": aim.no_of_cavity,

            "aim_composition": aim_composition,

            "created_at": aim.created_at,
            "updated_at": aim.updated_at,
        }

    # --------------------------------------------------
    # FURNACE DETAILS
    # --------------------------------------------------

    @staticmethod
    def get_furnace_details(
        db: Session,
        furnace_id: int
    ):

        # 1. Get Furnace
        furnace = FurnaceDetailsRepository.get_furnace(
            db,
            furnace_id
        )

        if not furnace:
            raise HTTPException(
                status_code=404,
                detail="Furnace not found",
            )

        # 2. Initialize response
        response = {
            "furnace": {
                "id": furnace.id,
                "name": furnace.name,
                "furnace_no": furnace.furnace_no,
                "ref_no": furnace.ref_no,
                "capacity": float(furnace.capacity),
                "is_active": furnace.is_active,
                "created_at": furnace.created_at,
                "updated_at": furnace.updated_at,
            },

            "current_cycle": None,
            "order": None,
            "charge_mix": None,
            "spectrum_results": [],
        }

        # 3. Get current running cycle
        cycle = FurnaceDetailsRepository.get_current_cycle(
            db,
            furnace_id
        )

        if not cycle:
            return response

        response["current_cycle"] = {
            "id": cycle.id,
            "order_id": cycle.order_id,
            "heat_no": cycle.heat_no,
            "furnace_capacity": float(
                cycle.furnace_capacity
            ),
            "status": cycle.status,
            "active_stage": cycle.active_stage,
            "started_at": cycle.started_at,
            "completed_at": cycle.completed_at,
        }

        # 4. Get complete Order
        order = FurnaceDetailsRepository.get_order(
            db,
            cycle.order_id
        )

        if order:

            response["order"] = {
                "id": order.id,
                "order_number": order.order_number,
                "status": order.status,
                "customer_delivery_date": (
                    order.customer_delivery_date
                ),
                "created_at": order.created_at,
                "updated_at": order.updated_at,

                "aim": FurnaceDetailsService.serialize_aim(
                    order.aim
                ),
            }

        # 5. Get Charge Mix
        charge_mix = FurnaceDetailsRepository.get_charge_mix(
            db,
            cycle.id
        )

        if charge_mix:

            items = []

            for item in charge_mix.items:

                elements = []

                # Charge item element composition
                for element in item.elements:

                    elements.append({
                        "element_id": element.element_id,

                        "element_name": (
                            element.element.name
                            if element.element else None
                        ),

                        "percentage": float(
                            element.percentage
                        ),
                    })

                # Raw material stock
                stock = item.raw_material_stock

                items.append({
                    "id": item.id,

                    "raw_material_stock_id": (
                        item.raw_material_stock_id
                    ),

                    "raw_material_stock": (
                        {
                            "id": stock.id,
                            "name": getattr(
                                stock,
                                "name",
                                None
                            ),
                        }
                        if stock else None
                    ),

                    "weight": float(item.weight),

                    "rate_per_kg": float(
                        item.rate_per_kg
                    ),

                    "bunker_name": item.bunker_name,

                    "elements": elements,
                })

            response["charge_mix"] = {
                "id": charge_mix.id,

                "charging_capacity": float(
                    charge_mix.charging_capacity
                ),

                "total_charged_weight": float(
                    charge_mix.total_charged_weight
                ),

                "remaining_capacity": float(
                    charge_mix.charging_capacity
                    - charge_mix.total_charged_weight
                ),

                "status": charge_mix.status,
                "confirmed_at": charge_mix.confirmed_at,

                "items": items,
            }

        # 6. Get all Spectrum Results
        spectrum_results = (
            FurnaceDetailsRepository.get_spectrum_results(
                db,
                cycle.id
            )
        )

        for result in spectrum_results:

            spectrum_data = {
                "test_number": result.test_number,
                "stage": result.test_stage,
                "T": result.operator_name,
            }

            # Add all chemical element values
            for element in result.elements:

                spectrum_data[
                    element.element_symbol
                ] = float(element.percentage)

            spectrum_data["fur"] = furnace.furnace_no

            response["spectrum_results"].append(
                spectrum_data
            )

        # 7. Return complete Furnace Details
        return response

    
    @staticmethod
    def complete_melt(db: Session, furnace_id: int):

        # 1. Check furnace
        furnace = FurnaceDetailsRepository.get_furnace(
            db, furnace_id
        )

        if not furnace:
            raise HTTPException(
                status_code=404,
                detail="Furnace not found",
            )

        # 2. Get running cycle with row lock
        cycle = FurnaceDetailsRepository.get_current_cycle_for_update(
            db, furnace_id
        )

        if not cycle:
            raise HTTPException(
                status_code=404,
                detail="No running furnace cycle found",
            )

        try:
            # 3. Verify confirmed charge mix
            charge_mix = FurnaceDetailsRepository.get_charge_mix(
                db, cycle.id
            )

            if not charge_mix:
                raise HTTPException(
                    status_code=400,
                    detail="Charge mix not found",
                )

            if charge_mix.status != "Confirmed":
                raise HTTPException(
                    status_code=400,
                    detail="Charge mix must be confirmed before completing melt",
                )

            # 4. Verify at least one spectrum result exists
            spectrum_results = (
                FurnaceDetailsRepository.get_spectrum_results(
                    db, cycle.id
                )
            )

            if not spectrum_results:
                raise HTTPException(
                    status_code=400,
                    detail="Spectrum testing must be completed before completing melt",
                )

            # 5. Complete furnace cycle
            from sqlalchemy import func

            cycle.status = "Completed"
            cycle.active_stage = "Completed"
            cycle.completed_at = func.now()

            db.commit()
            db.refresh(cycle)

            return {
                "furnace_id": furnace.id,
                "furnace_no": furnace.furnace_no,
                "cycle_id": cycle.id,
                "heat_no": cycle.heat_no,
                "status": cycle.status,
                "active_stage": cycle.active_stage,
                "started_at": cycle.started_at,
                "completed_at": cycle.completed_at,
                "message": "Melt completed successfully",
            }

        except Exception:
            db.rollback()
            raise

    
    @staticmethod
    def get_furnace_history(db: Session, furnace_id: int):

        # Check furnace
        furnace = FurnaceDetailsRepository.get_furnace(
            db, furnace_id
        )

        if not furnace:
            raise HTTPException(
                status_code=404,
                detail="Furnace not found",
            )

        # Get completed cycles
        cycles = FurnaceDetailsRepository.get_cycle_history(
            db, furnace_id
        )

        history = []

        for cycle in cycles:

            # Get associated order
            order = FurnaceDetailsRepository.get_order(
                db, cycle.order_id
            )

            # Get charge mix
            charge_mix = FurnaceDetailsRepository.get_charge_mix(
                db, cycle.id
            )

            # Get spectrum results
            spectrum_results = (
                FurnaceDetailsRepository.get_spectrum_results(
                    db, cycle.id
                )
            )

            history.append({
                "cycle_id": cycle.id,
                "heat_no": cycle.heat_no,

                "order": {
                    "id": order.id,
                    "order_number": order.order_number,
                    "status": order.status,
                } if order else None,

                "furnace_capacity": float(
                    cycle.furnace_capacity
                ),

                "status": cycle.status,
                "active_stage": cycle.active_stage,

                "started_at": cycle.started_at,
                "completed_at": cycle.completed_at,

                "charge_mix": {
                    "id": charge_mix.id,
                    "status": charge_mix.status,
                    "total_charged_weight": float(
                        charge_mix.total_charged_weight
                    ),
                } if charge_mix else None,

                "spectrum_test_count": len(spectrum_results),
            })

        return {
            "furnace": {
                "id": furnace.id,
                "name": furnace.name,
                "furnace_no": furnace.furnace_no,
            },
            "total_melts": len(history),
            "history": history,
        }
