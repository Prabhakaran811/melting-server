
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

        # Support the legacy format if the literal suffix
        # reaches FastAPI instead of being stripped as a URL fragment.
        furnace_number = None

        if "#&fur:" in payload:
            payload, furnace_part = payload.rsplit("#&fur:", 1)
            furnace_number = furnace_part.strip()

        if payload.startswith("$"):
            payload = payload[1:]

        values = payload.split(",")

        operator_name = None
        elements = {}

        for index, item in enumerate(values):

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

            if key == "T":
                operator_name = value
                continue

            if not key:
                raise HTTPException(
                    status_code=400,
                    detail="Element symbol cannot be empty",
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

        if not elements:
            raise HTTPException(
                status_code=400,
                detail="No chemical elements found",
            )

        return {
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

            # Use an explicit query parameter first.
            # Legacy suffix is supported only if it was actually
            # transmitted to the application.
            furnace_number = (
                furnace_number
                or parsed["furnace_number_from_payload"]
            )

            if not furnace_number:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Furnace number was not received. "
                        "The URL fragment after # is not sent by "
                        "standard HTTP clients. Provide fur as a "
                        "query parameter or configure a reliable "
                        "machine-to-furnace mapping."
                    ),
                )

            furnace_number = str(furnace_number).strip()

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

            if cycle.active_stage != "Spectrum Testing":
                raise HTTPException(
                    status_code=409,
                    detail=(
                        "Furnace Cycle is not in Spectrum Testing. "
                        f"Current stage: {cycle.active_stage}"
                    ),
                )

            charge_mix = Repository.get_confirmed_charge_mix(
                db,
                cycle.id,
            )

            if not charge_mix:
                raise HTTPException(
                    status_code=409,
                    detail="Charge Mix is not confirmed",
                )

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

            for symbol, percentage in parsed["elements"].items():

                element = SpectrumResultElement(
                    element_symbol=symbol,
                    element_name=ELEMENT_NAMES.get(symbol),
                    percentage=percentage,
                )

                result.elements.append(element)

            Repository.create_result(db, result)

            db.commit()

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
