
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.services.spectrum_result_service import (
    SpectrumResultService,
)

from app.repositories.spectrum_result_repository import (
    SpectrumResultRepository,
)


router = APIRouter(
    prefix="/spectrum-results",
    tags=["Spectrum Results"],
)


# Machine receiver
@router.get("/receive")
def receive_spectrum_result(
    d: str = Query(..., description="Raw spectrum machine data"),
    fur: str | None = Query(
        default=None,
        description="Machine furnace number",
    ),
    db: Session = Depends(get_db),
):
    return SpectrumResultService.receive_result(
        db=db,
        payload=d,
        furnace_number=fur,
    )


# Get one spectrum result
@router.get("/{result_id}")
def get_spectrum_result(
    result_id: int,
    db: Session = Depends(get_db),
):

    result = SpectrumResultRepository.get_result_by_id(
        db,
        result_id,
    )

    if not result:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="Spectrum Result not found",
        )

    return {
        "success": True,
        "message": "Spectrum Result retrieved successfully",
        "data": result,
    }


# Get all spectrum results for a Furnace Cycle
@router.get("/cycles/{cycle_id}")
def get_cycle_spectrum_results(
    cycle_id: int,
    db: Session = Depends(get_db),
):

    results = SpectrumResultRepository.get_results_by_cycle(
        db,
        cycle_id,
    )

    return {
        "success": True,
        "message": "Spectrum Results retrieved successfully",
        "data": results,
    }
