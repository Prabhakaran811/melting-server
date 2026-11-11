
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.furnace_charge_mix_schema import (
    FurnaceChargeItemCreate,
    FurnaceChargeItemUpdate,
)
from app.services.furnace_charge_mix_service import (
    FurnaceChargeMixService,
)


router = APIRouter(
    prefix="/furnaces",
    tags=["Furnace Charge Mix"],
)


@router.post(
    "/{furnace_id}/charge-mix",
    status_code=status.HTTP_201_CREATED,
)
def create_charge_mix(
    furnace_id: int,
    db: Session = Depends(get_db),
):
    result = FurnaceChargeMixService.create_charge_mix(
        db=db,
        furnace_id=furnace_id,
    )

    return {
        "success": True,
        "message": "Charge Mix created successfully",
        "data": result,
    }


@router.get("/{furnace_id}/charge-mix")
def get_charge_mix(
    furnace_id: int,
    db: Session = Depends(get_db),
):
    result = FurnaceChargeMixService.get_charge_mix(
        db=db,
        furnace_id=furnace_id,
    )

    return {
        "success": True,
        "message": "Charge Mix retrieved successfully",
        "data": result,
    }


@router.post(
    "/{furnace_id}/charge-mix/items",
    status_code=status.HTTP_201_CREATED,
)
def add_charge_item(
    furnace_id: int,
    data: FurnaceChargeItemCreate,
    db: Session = Depends(get_db),
):
    result = FurnaceChargeMixService.add_charge_item(
        db=db,
        furnace_id=furnace_id,
        data=data,
    )

    return {
        "success": True,
        "message": "Raw material added to Charge Mix successfully",
        "data": result,
    }


@router.put(
    "/{furnace_id}/charge-mix/items/{item_id}"
)
def update_charge_item(
    furnace_id: int,
    item_id: int,
    data: FurnaceChargeItemUpdate,
    db: Session = Depends(get_db),
):
    result = FurnaceChargeMixService.update_charge_item(
        db=db,
        furnace_id=furnace_id,
        item_id=item_id,
        data=data,
    )

    return {
        "success": True,
        "message": "Charge item updated successfully",
        "data": result,
    }


@router.delete(
    "/{furnace_id}/charge-mix/items/{item_id}"
)
def delete_charge_item(
    furnace_id: int,
    item_id: int,
    db: Session = Depends(get_db),
):
    return FurnaceChargeMixService.delete_charge_item(
        db=db,
        furnace_id=furnace_id,
        item_id=item_id,
    )


@router.patch(
    "/{furnace_id}/charge-mix/confirm"
)
def confirm_charge_mix(
    furnace_id: int,
    db: Session = Depends(get_db),
):
    result = FurnaceChargeMixService.confirm_charge_mix(
        db=db,
        furnace_id=furnace_id,
    )

    return {
        "success": True,
        "message": "Charge Mix confirmed successfully",
        "data": result,
    }
