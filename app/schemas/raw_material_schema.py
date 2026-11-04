from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class RawMaterialCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    element_ids: list[int] = Field(..., min_length=1)


class RawMaterialUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    element_ids: list[int] = Field(..., min_length=1)


class RawMaterialIronTypeResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class RawMaterialElementResponse(BaseModel):
    id: int
    name: str
    abbreviation: str
    sequence_order: int
    iron_types: list[RawMaterialIronTypeResponse]

    model_config = ConfigDict(from_attributes=True)


class RawMaterialResponse(BaseModel):
    id: int
    name: str
    elements: list[RawMaterialElementResponse]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)