
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class FurnaceChargeItemCreate(BaseModel):
    raw_material_stock_id: int = Field(gt=0)
    weight: Decimal = Field(gt=0, max_digits=12, decimal_places=3)
    bunker_name: Optional[str] = Field(default=None, max_length=100)


class FurnaceChargeItemUpdate(BaseModel):
    raw_material_stock_id: Optional[int] = Field(default=None, gt=0)
    weight: Optional[Decimal] = Field(
        default=None,
        gt=0,
        max_digits=12,
        decimal_places=3,
    )
    bunker_name: Optional[str] = Field(default=None, max_length=100)


class FurnaceChargeElementResponse(BaseModel):
    element_id: int
    percentage: Decimal
    element_name: Optional[str] = None
    abbreviation: Optional[str] = None


class FurnaceChargeItemResponse(BaseModel):
    id: int
    charge_mix_id: int
    raw_material_stock_id: int
    weight: Decimal
    rate_per_kg: Decimal
    bunker_name: Optional[str]
    elements: list[FurnaceChargeElementResponse] = []

    model_config = ConfigDict(from_attributes=True)


class FurnaceChargeElementSummary(BaseModel):
    element_id: int
    element_name: str
    abbreviation: str
    percentage: Decimal


class FurnaceChargeMixResponse(BaseModel):
    id: int
    furnace_cycle_id: int
    charging_capacity: Decimal
    total_charged_weight: Decimal
    remaining_capacity: Decimal
    status: str
    confirmed_at: Optional[datetime]
    items: list[FurnaceChargeItemResponse]
    element_composition: list[FurnaceChargeElementSummary]

    model_config = ConfigDict(from_attributes=True)


class FurnaceChargeMixCreateResponse(BaseModel):
    success: bool
    message: str
    data: FurnaceChargeMixResponse
