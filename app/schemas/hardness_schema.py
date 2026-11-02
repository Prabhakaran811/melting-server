from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HardnessCreate(BaseModel):
    hardness_name: str = Field(
        min_length=2,
        max_length=150
    )


class HardnessUpdate(BaseModel):
    hardness_name: str = Field(
        min_length=2,
        max_length=150
    )


class HardnessResponse(BaseModel):
    id: int
    hardness_name: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)