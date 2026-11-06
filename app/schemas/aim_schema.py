from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# ==================================
# AIM ELEMENT INPUT
# ==================================

class AimElementInput(BaseModel):
    element_id: int = Field(..., gt=0)

    exact_value: Decimal = Field(..., ge=0)

    plus_value: Decimal = Field(..., ge=0)

    minus_value: Decimal = Field(..., ge=0)


# ==================================
# CREATE AIM
# ==================================

class AimCreate(BaseModel):
    customer_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)

    drawing_no: str = Field(..., min_length=1, max_length=100)

    iron_type_id: int = Field(..., gt=0)

    packing_id: int = Field(..., gt=0)
    hardness_id: int = Field(..., gt=0)
    inoculant_id: int = Field(..., gt=0)

    pouring_weight_kg: Decimal = Field(..., gt=0)
    casting_weight_kg: Decimal = Field(..., gt=0)

    no_of_casting: int = Field(..., gt=0)
    no_of_cavity: int = Field(..., gt=0)

    elements: list[AimElementInput] = Field(..., min_length=1)


# ==================================
# UPDATE AIM
# ==================================

class AimUpdate(BaseModel):
    customer_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)

    drawing_no: str = Field(..., min_length=1, max_length=100)

    iron_type_id: int = Field(..., gt=0)

    packing_id: int = Field(..., gt=0)
    hardness_id: int = Field(..., gt=0)
    inoculant_id: int = Field(..., gt=0)

    pouring_weight_kg: Decimal = Field(..., gt=0)
    casting_weight_kg: Decimal = Field(..., gt=0)

    no_of_casting: int = Field(..., gt=0)
    no_of_cavity: int = Field(..., gt=0)

    elements: list[AimElementInput] = Field(..., min_length=1)


# ==================================
# MASTER RESPONSE DETAILS
# ==================================

class AimCustomerDetail(BaseModel):
    id: int
    customer_name: str

    model_config = ConfigDict(from_attributes=True)


class AimProductDetail(BaseModel):
    id: int
    product_name: str

    model_config = ConfigDict(from_attributes=True)


class AimIronTypeDetail(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class AimPackingDetail(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class AimHardnessDetail(BaseModel):
    id: int
    hardness_name: str

    model_config = ConfigDict(from_attributes=True)


class AimInoculantDetail(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class AimElementMasterDetail(BaseModel):
    id: int
    name: str
    abbreviation: str

    model_config = ConfigDict(from_attributes=True)


# ==================================
# AIM ELEMENT RESPONSE
# ==================================

class AimElementResponse(BaseModel):
    id: int
    element_id: int

    element: AimElementMasterDetail

    exact_value: Decimal
    plus_value: Decimal
    minus_value: Decimal

    model_config = ConfigDict(from_attributes=True)


# ==================================
# AIM RESPONSE
# ==================================

class AimResponse(BaseModel):
    id: int

    customer_id: int
    customer: AimCustomerDetail

    product_id: int
    product: AimProductDetail

    drawing_no: str

    iron_type_id: int
    iron_type: AimIronTypeDetail

    packing_id: int
    packing: AimPackingDetail

    hardness_id: int
    hardness: AimHardnessDetail

    inoculant_id: int
    inoculant: AimInoculantDetail

    pouring_weight_kg: Decimal
    casting_weight_kg: Decimal

    no_of_casting: int
    no_of_cavity: int

    elements: list[AimElementResponse]

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)