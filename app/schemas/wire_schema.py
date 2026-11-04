from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WireCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    raw_material_id: int = Field(..., gt=0)


class WireUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    raw_material_id: int = Field(..., gt=0)


class WireRawMaterialResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class WireResponse(BaseModel):
    id: int
    name: str
    raw_material_id: int
    raw_material: WireRawMaterialResponse
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)