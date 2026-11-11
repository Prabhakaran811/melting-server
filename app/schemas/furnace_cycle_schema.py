
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class FurnaceCycleStart(BaseModel):
    order_id: int = Field(gt=0)


class FurnaceCycleResponse(BaseModel):
    id: int
    furnace_id: int
    order_id: int
    heat_no: str
    furnace_capacity: Decimal
    status: str
    active_stage: str
    started_at: datetime
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FurnaceCycleStartResponse(BaseModel):
    success: bool
    message: str
    data: FurnaceCycleResponse


class FurnaceCycleListResponse(BaseModel):
    success: bool
    message: str
    data: list[FurnaceCycleResponse]
