from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class IronTypeCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    element_ids: list[int] = Field(..., min_length=1)


class IronTypeUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    element_ids: list[int] = Field(..., min_length=1)


class IronTypeElementResponse(BaseModel):
    id: int
    name: str
    abbreviation: str
    sequence_order: int

    model_config = ConfigDict(from_attributes=True)


class IronTypeResponse(BaseModel):
    id: int
    name: str
    elements: list[IronTypeElementResponse]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)