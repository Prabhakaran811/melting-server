from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.report_service import ReportService


router = APIRouter(
    prefix="/reports",
    tags=["Furnace Cycle Reports"],
)


@router.get("/furnace-cycles")
def get_furnace_cycle_reports(
    furnace_id: int | None = Query(default=None),
    heat_no: str | None = Query(default=None),
    order_number: str | None = Query(default=None),
    cycle_status: str | None = Query(default=None, alias="status"),
    from_date: date | None = Query(default=None),
    to_date: date | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    data = ReportService.get_cycle_reports(
        db=db,
        furnace_id=furnace_id,
        heat_no=heat_no,
        order_number=order_number,
        cycle_status=cycle_status,
        from_date=from_date,
        to_date=to_date,
        page=page,
        page_size=page_size,
    )

    return {
        "success": True,
        "message": "Furnace cycle reports retrieved successfully",
        "data": data,
    }


@router.get("/furnace-cycles/{cycle_id}")
def get_furnace_cycle_report(
    cycle_id: int,
    db: Session = Depends(get_db),
):
    data = ReportService.get_cycle_report(
        db=db,
        cycle_id=cycle_id,
    )

    return {
        "success": True,
        "message": "Furnace cycle report retrieved successfully",
        "data": data,
    }