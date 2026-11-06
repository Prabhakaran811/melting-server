from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.database import get_db

from app.schemas.wire_stock_schema import (
    WireStockCreate,
    WireStockUpdate,
    WireStockResponse
)

from app.services.wire_stock_service import (
    WireStockService
)


router = APIRouter(
    prefix="/wire-stocks",
    tags=["Wire Stocks"]
)


@router.post(
    "/",
    response_model=WireStockResponse,
    status_code=status.HTTP_201_CREATED
)
def create_stock(
    data: WireStockCreate,
    db: Session = Depends(get_db)
):
    try:
        return WireStockService.create_wire_stock(db, data)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Database constraint error while creating wire stock"
        )


@router.get(
    "/",
    response_model=list[WireStockResponse]
)
def get_stocks(db: Session = Depends(get_db)):
    return WireStockService.get_wire_stocks(db)


@router.get(
    "/{stock_id}",
    response_model=WireStockResponse
)
def get_stock(
    stock_id: int,
    db: Session = Depends(get_db)
):
    try:
        return WireStockService.get_wire_stock(db, stock_id)

    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/{stock_id}",
    response_model=WireStockResponse
)
def update_stock(
    stock_id: int,
    data: WireStockUpdate,
    db: Session = Depends(get_db)
):
    try:
        return WireStockService.update_wire_stock(db, stock_id, data)

    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Database constraint error while updating wire stock"
        )


@router.delete("/{stock_id}")
def delete_stock(
    stock_id: int,
    db: Session = Depends(get_db)
):
    try:
        WireStockService.delete_wire_stock(db, stock_id)

        return {"message": "Wire Stock deleted successfully"}

    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Wire Stock cannot be deleted because it is being used"
        )