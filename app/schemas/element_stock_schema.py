from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ElementStockCreate(BaseModel):
    element_id: int = Field(..., gt=0)
    quantity: Decimal = Field(..., gt=0)
    supplier_id: int = Field(..., gt=0)
    received_date: date
    pickup_percentage: Decimal = Field(..., ge=0, le=100)
    rate_per_kg: Decimal = Field(..., ge=0)


class ElementStockUpdate(BaseModel):
    element_id: int = Field(..., gt=0)
    quantity: Decimal = Field(..., gt=0)
    supplier_id: int = Field(..., gt=0)
    received_date: date
    pickup_percentage: Decimal = Field(..., ge=0, le=100)
    rate_per_kg: Decimal = Field(..., ge=0)


class ElementStockElementResponse(BaseModel):
    id: int
    name: str
    abbreviation: str

    model_config = ConfigDict(from_attributes=True)


class ElementStockSupplierResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class ElementStockResponse(BaseModel):
    id: int
    element_id: int
    element: ElementStockElementResponse

    quantity: Decimal

    supplier_id: int
    supplier: ElementStockSupplierResponse

    received_date: date
    pickup_percentage: Decimal
    rate_per_kg: Decimal

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)