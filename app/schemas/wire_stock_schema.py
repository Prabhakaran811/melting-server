from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# CREATE
class WireStockCreate(BaseModel):
    wire_id: int = Field(..., gt=0)
    powder_weight_per_meter: Decimal = Field(..., ge=0)
    quantity: Decimal = Field(..., gt=0)
    supplier_id: int = Field(..., gt=0)
    rate_per_meter: Decimal = Field(..., ge=0)


# UPDATE
class WireStockUpdate(BaseModel):
    wire_id: int = Field(..., gt=0)
    powder_weight_per_meter: Decimal = Field(..., ge=0)
    quantity: Decimal = Field(..., gt=0)
    supplier_id: int = Field(..., gt=0)
    rate_per_meter: Decimal = Field(..., ge=0)


# RELATED SCHEMAS
class WireStockWireDetail(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class WireStockSupplierDetail(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


# RESPONSE
class WireStockResponse(BaseModel):
    id: int

    wire_id: int
    wire: WireStockWireDetail

    powder_weight_per_meter: Decimal
    quantity: Decimal

    supplier_id: int
    supplier: WireStockSupplierDetail

    rate_per_meter: Decimal

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)