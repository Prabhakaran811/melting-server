from pydantic import BaseModel, ConfigDict, Field


class InoculantCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)


class InoculantUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)


class InoculantResponse(BaseModel):
    id: int
    name: str
    created_at: object
    updated_at: object

    model_config = ConfigDict(from_attributes=True)