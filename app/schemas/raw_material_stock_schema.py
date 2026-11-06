from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# 1. Element input schema
class RawMaterialStockElementInput(BaseModel):
    element_id: int = Field(..., gt=0)
    percentage: Decimal = Field(..., ge=0, le=100)


# 2. Create schema
class RawMaterialStockCreate(BaseModel):
    raw_material_id: int = Field(..., gt=0)
    quantity: Decimal = Field(..., gt=0)
    supplier_id: int = Field(..., gt=0)
    received_date: date
    rate_per_kg: Decimal = Field(..., ge=0)
    element_percentages: list[RawMaterialStockElementInput] = Field(
        ..., min_length=1
    )


# 3. Update schema
class RawMaterialStockUpdate(BaseModel):
    raw_material_id: int = Field(..., gt=0)
    quantity: Decimal = Field(..., gt=0)
    supplier_id: int = Field(..., gt=0)
    received_date: date
    rate_per_kg: Decimal = Field(..., ge=0)
    element_percentages: list[RawMaterialStockElementInput] = Field(
        ..., min_length=1
    )


# 4. Related object schemas — define these before the response schema
class RawMaterialDetail(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class SupplierDetail(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class RawMaterialStockElementDetail(BaseModel):
    id: int
    name: str
    abbreviation: str

    model_config = ConfigDict(from_attributes=True)


class RawMaterialStockElementResponse(BaseModel):
    id: int
    element_id: int
    percentage: Decimal
    element: RawMaterialStockElementDetail

    model_config = ConfigDict(from_attributes=True)


# 5. Main response schema — define this last
class RawMaterialStockResponse(BaseModel):
    id: int

    raw_material_id: int
    raw_material: RawMaterialDetail

    quantity: Decimal

    supplier_id: int
    supplier: SupplierDetail

    received_date: date
    rate_per_kg: Decimal

    element_percentages: list[RawMaterialStockElementResponse]

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)