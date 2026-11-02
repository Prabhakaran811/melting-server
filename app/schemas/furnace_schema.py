from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class FurnaceCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    furnace_no: str = Field(min_length=1, max_length=50)
    ref_no: str = Field(min_length=1, max_length=50)
    capacity: Decimal = Field(gt=0, max_digits=12, decimal_places=2)


class FurnaceUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    furnace_no: Optional[str] = Field(default=None, min_length=1, max_length=50)
    ref_no: Optional[str] = Field(default=None, min_length=1, max_length=50)
    capacity: Optional[Decimal] = Field(
        default=None,
        gt=0,
        max_digits=12,
        decimal_places=2
    )


class FurnaceStatusUpdate(BaseModel):
    is_active: bool


class FurnaceResponse(BaseModel):
    id: int
    name: str
    furnace_no: str
    ref_no: str
    capacity: Decimal
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)