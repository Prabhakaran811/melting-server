
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SpectrumResultElementResponse(BaseModel):
    id: int
    element_symbol: str
    element_name: Optional[str] = None
    percentage: Decimal

    model_config = ConfigDict(from_attributes=True)


class SpectrumResultResponse(BaseModel):
    id: int
    furnace_cycle_id: int
    test_number: int
    test_stage: Optional[str] = None
    operator_name: Optional[str] = None
    result_status: str
    received_at: datetime
    elements: list[SpectrumResultElementResponse]

    model_config = ConfigDict(from_attributes=True)


class SpectrumResultReceiveResponse(BaseModel):
    success: bool
    message: str
    data: dict


class SpectrumResultListResponse(BaseModel):
    success: bool
    message: str
    data: list[SpectrumResultResponse]
