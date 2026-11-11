
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


CycleStatus = Literal[
    "Running",
    "Completed",
    "Cancelled"
]

CycleStageName = Literal[
    "Started",
    "Charge Mix",
    "Spectrum Testing",
    "Completed"
]


class FurnaceCycleStart(BaseModel):
    order_id: int = Field(gt=0)
    shift: int | None = Field(default=None, ge=1, le=3)


class FurnaceCycleStageResponse(BaseModel):
    id: int
    stage_name: str
    started_at: datetime
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class FurnaceCycleResponse(BaseModel):
    id: int
    furnace_id: int
    order_id: int
    heat_no: str
    furnace_capacity: Decimal
    status: CycleStatus
    active_stage: CycleStageName
    shift: int | None
    started_at: datetime
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime
    stages: list[FurnaceCycleStageResponse] = []

    model_config = ConfigDict(from_attributes=True)
