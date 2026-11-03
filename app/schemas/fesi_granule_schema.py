from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class FeSiGranuleCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)


class FeSiGranuleUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)


class FeSiGranuleResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)