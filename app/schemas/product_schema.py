from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    product_name: str = Field(
        min_length=2,
        max_length=150
    )


class ProductUpdate(BaseModel):
    product_name: str = Field(
        min_length=2,
        max_length=150
    )


class ProductResponse(BaseModel):
    id: int
    product_name: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)