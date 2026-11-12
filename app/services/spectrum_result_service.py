
from decimal import Decimal, InvalidOperation
from urllib.parse import unquote

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.spectrum_result import (
    SpectrumResult,
    SpectrumResultElement,
)

from app.repositories.spectrum_result_repository import (
    SpectrumResultRepository as Repository,
)


ELEMENT_NAMES = {
    "C": "Carbon",
    "Si": "Silicon",
    "Mn": "Manganese",
    "P": "Phosphorus",
    "S": "Sulphur",
    "Cu": "Copper",
    "Cr": "Chromium",
    "Sn": "Tin",
    "Mg": "Magnesium",
    "Mo": "Molybdenum",
    "Ni": "Nickel",
    "Al": "Aluminium",
    "Ti": "Titanium",
    "V": "Vanadium",
    "B": "Boron",
    "Pb": "Lead",
    "As": "Arsenic",
    "Zr": "Zirconium",
    "Sb": "Antimony",
    "Zn": "Zinc",
    "Ce": "Cerium",
    "Co": "Cobalt",
    "Bi": "Bismuth",
    "Ca": "Calcium",
    "Fe": "Iron",
    "Nb": "Niobium",
    "Ceq": "Carbon Equivalent",
}


class SpectrumResultService:

    @staticmethod
    def parse_spectrum_payload(payload: str):

        if not payload:
            raise HTTPException(
                status_code=400,
                detail="Spectrum data is missing",
            )

        payload = unquote(payload).strip()

        furnace_number = None

        # Support legacy payload format.
        if "#&fur:" in payload:
            payload, furnace_part = payload.rsplit("#&fur:", 1)
            furnace_number = furnace_part.strip()

        if payload.startswith("$"):
            payload = payload[1:]

        values = payload.split(",")

        heat_no = None
        operator_name = None
        elements = {}

        for item in values:

            item = item.strip()

            if not item:
                continue

            if ":" not in item:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid spectrum field: {item}",
                )

            key, value = item.split(":", 1)

            key = key.strip()
            value = value.strip()

            # Heat number is text, not a chemical element.
            if key == "H":
                if heat_no is not None:
                    raise HTTPException(
                        status_code=400,
                        detail="Duplicate heat number field",
                    )

                heat_no = value
                continue

            # Operator name is also text.
            if key == "T":
                if operator_name is not None:
                    raise HTTPException(
                        status_code=400,
                        detail="Duplicate operator field",
                    )

                operator_name = value
                continue

            if not key:
                raise HTTPException(
                    status_code=400,
                    detail="Element symbol cannot be empty",
                )

            if key not in ELEMENT_NAMES:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported element symbol: {key}",
                )

            if key in elements:
                raise HTTPException(
                    status_code=400,
                    detail=f"Duplicate element: {key}",
                )

            try:
                number = Decimal(value)

                if not number.is_finite() or number < 0:
                    raise ValueError()

                if key != "Ceq" and number > 100:
                    raise ValueError()

            except (InvalidOperation, ValueError):
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid numeric value for {key}: {value}",
                )

            elements[key] = number

        if not heat_no:
            raise HTTPException(
                status_code=400,
                detail="Heat number is missing",
            )

        if not operator_name:
            raise HTTPException(
                status_code=400,
                detail="Operator name is missing",
            )

        if not elements:
            raise HTTPException(
                status_code=400,
                detail="No chemical elements found",
            )

        return {
            "heat_no": heat_no,
            "operator_name": operator_name,
            "elements": elements,
            "furnace_number_from_payload": furnace_number,
        }

    @staticmethod
    def receive_result(
        db: Session,
        payload: str,
        furnace_number: str | None,
    ):

        try:

            parsed = SpectrumResultService.parse_spectrum_payload(
                payload
            )

            furnace_number = (
                furnace_number
                or parsed["furnace_number_from_payload"]
            )

            if not furnace_number:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Furnace number is missing. "
                        "Provide fur as a query parameter."
                    ),
                )

            furnace_number = str(furnace_number).strip()
            heat_no = parsed["heat_no"]

            # Find furnace using its machine furnace number.
            furnace = Repository.get_furnace_by_number(
                db,
                furnace_number,
            )

            if not furnace:
                raise HTTPException(
                    status_code=404,
                    detail=(
                        f"Active Furnace {furnace_number} not found"
                    ),
                )

            # Lock and find the current running cycle.
            cycle = Repository.get_running_cycle_for_update(
                db,
                furnace.id,
            )

            if not cycle:
                raise HTTPException(
                    status_code=409,
                    detail=(
                        f"No Running Furnace Cycle found "
                        f"for Furnace {furnace_number}"
                    ),
                )

            # Ensure machine result belongs to this exact heat.
            if cycle.heat_no != heat_no:
                raise HTTPException(
                    status_code=409,
                    detail=(
                        f"Heat number mismatch. "
                        f"Machine sent {heat_no}, "
                        f"but current furnace heat is {cycle.heat_no}"
                    ),
                )

            if cycle.active_stage != "Spectrum Testing":
                raise HTTPException(
                    status_code=409,
                    detail=(
                        "Furnace Cycle is not in Spectrum Testing. "
                        f"Current stage: {cycle.active_stage}"
                    ),
                )

            # Charge Mix must be confirmed before spectrum testing.
            charge_mix = Repository.get_confirmed_charge_mix(
                db,
                cycle.id,
            )

            if not charge_mix:
                raise HTTPException(
                    status_code=409,
                    detail="Charge Mix is not confirmed",
                )

            # Generate the next test number.
            test_number = Repository.get_next_test_number(
                db,
                cycle.id,
            )

            result = SpectrumResult(
                furnace_cycle_id=cycle.id,
                test_number=test_number,
                operator_name=parsed["operator_name"],
                result_status="Pending",
                raw_payload=payload,
            )

            # Save individual chemical element values.
            for symbol, percentage in parsed["elements"].items():

                element = SpectrumResultElement(
                    element_symbol=symbol,
                    element_name=ELEMENT_NAMES[symbol],
                    percentage=percentage,
                )

                result.elements.append(element)

            Repository.create_result(db, result)

            db.commit()

            db.refresh(result)

            saved_result = Repository.get_result_by_id(
                db,
                result.id,
            )

            return {
                "success": True,
                "message": "Spectrum result received successfully",
                "data": {
                    "spectrum_result_id": saved_result.id,
                    "furnace_id": furnace.id,
                    "furnace_number": furnace.furnace_no,
                    "furnace_cycle_id": cycle.id,
                    "heat_no": cycle.heat_no,
                    "test_number": saved_result.test_number,
                    "operator_name": saved_result.operator_name,
                    "element_count": len(saved_result.elements),
                    "result_status": saved_result.result_status,
                },
            }

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise
