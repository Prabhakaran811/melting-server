from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.aim_schema import AimResponse


OrderStatus = Literal[
    "Pending",
    "In Progress",
    "Completed",
    "Cancelled"
]


class OrderCreate(BaseModel):
    aim_id: int = Field(gt=0)
    customer_delivery_date: date


class OrderUpdate(BaseModel):
    aim_id: int = Field(gt=0)
    status: OrderStatus
    customer_delivery_date: date


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderResponse(BaseModel):
    id: int
    order_number: str
    aim_id: int
    aim: AimResponse
    status: OrderStatus
    customer_delivery_date: date
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)