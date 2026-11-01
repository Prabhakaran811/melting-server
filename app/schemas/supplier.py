from pydantic import BaseModel, ConfigDict, Field


class SupplierCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    address: str = Field(..., min_length=2, max_length=500)
    phone_number: str = Field(..., min_length=7, max_length=20)


class SupplierUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=150)
    address: str | None = Field(None, min_length=2, max_length=500)
    phone_number: str | None = Field(None, min_length=7, max_length=20)


class SupplierResponse(BaseModel):
    id: int
    name: str
    address: str
    phone_number: str

    model_config = ConfigDict(from_attributes=True)