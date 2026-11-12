from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.report_repository import ReportRepository


class ReportService:

    @staticmethod
    def get_cycle_reports(
        db: Session,
        furnace_id: int | None = None,
        heat_no: str | None = None,
        order_number: str | None = None,
        cycle_status: str | None = None,
        from_date=None,
        to_date=None,
        page: int = 1,
        page_size: int = 20,
    ):
        if page < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Page must be greater than zero",
            )

        if page_size < 1 or page_size > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Page size must be between 1 and 100",
            )

        if from_date and to_date and from_date > to_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="from_date cannot be later than to_date",
            )

        cycles, total = ReportRepository.get_filtered_cycles(
            db=db,
            furnace_id=furnace_id,
            heat_no=heat_no,
            order_number=order_number,
            status=cycle_status,
            from_date=from_date,
            to_date=to_date,
            page=page,
            page_size=page_size,
        )

        reports = [
            ReportRepository.build_cycle_report(db, cycle)
            for cycle in cycles
        ]

        return {
            "items": reports,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_records": total,
                "total_pages": (
                    (total + page_size - 1) // page_size
                ),
            },
        }

    @staticmethod
    def get_cycle_report(db: Session, cycle_id: int):
        cycle = ReportRepository.get_cycle_by_id(
            db=db,
            cycle_id=cycle_id,
        )

        if not cycle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Furnace cycle {cycle_id} not found",
            )

        return ReportRepository.build_cycle_report(
            db=db,
            cycle=cycle,
        )