from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class FurnaceCycleReportFilters(BaseModel):
    furnace_id: int | None = None
    heat_no: str | None = None
    order_number: str | None = None
    status: str | None = None
    from_date: date | None = None
    to_date: date | None = None
    page: int = 1
    page_size: int = 20


class FurnaceCycleReportResponse(BaseModel):
    success: bool = True
    message: str
    data: dict[str, Any]


class FurnaceCycleReportListResponse(BaseModel):
    success: bool = True
    message: str
    data: dict[str, Any]