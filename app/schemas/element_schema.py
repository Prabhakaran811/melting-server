from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ElementCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    abbreviation: str = Field(..., min_length=1, max_length=20)
    sequence_order: int = Field(..., ge=1)


class ElementUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    abbreviation: str = Field(..., min_length=1, max_length=20)
    sequence_order: int = Field(..., ge=1)


class ElementResponse(BaseModel):
    id: int
    name: str
    abbreviation: str
    sequence_order: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)