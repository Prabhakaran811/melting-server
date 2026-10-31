from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerCreate(BaseModel):
    customer_name: str = Field(min_length=2, max_length=150)
    address: str = Field(min_length=5)
    phone_number: str = Field(min_length=7, max_length=20)
    email: EmailStr


class CustomerUpdate(BaseModel):
    customer_name: Optional[str] = Field(
        default=None, min_length=2, max_length=150
    )
    address: Optional[str] = Field(default=None, min_length=5)
    phone_number: Optional[str] = Field(
        default=None, min_length=7, max_length=20
    )
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class CustomerResponse(BaseModel):
    id: int
    customer_name: str
    address: str
    phone_number: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)