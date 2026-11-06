from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.database import get_db

from app.schemas.aim_schema import (
    AimCreate,
    AimUpdate,
    AimResponse,
)

from app.services.aim_service import AimService


router = APIRouter(
    prefix="/aims",
    tags=["Aims"]
)


# CREATE
@router.post(
    "/",
    response_model=AimResponse,
    status_code=status.HTTP_201_CREATED
)
def create_aim(
    data: AimCreate,
    db: Session = Depends(get_db)
):
    try:
        return AimService.create_aim(db, data)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Database constraint error while creating Aim"
        )


# GET ALL
@router.get(
    "/",
    response_model=list[AimResponse]
)
def get_aims(
    db: Session = Depends(get_db)
):
    return AimService.get_aims(db)


# GET BY ID
@router.get(
    "/{aim_id}",
    response_model=AimResponse
)
def get_aim(
    aim_id: int,
    db: Session = Depends(get_db)
):
    try:
        return AimService.get_aim(db, aim_id)

    except LookupError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# UPDATE
@router.put(
    "/{aim_id}",
    response_model=AimResponse
)
def update_aim(
    aim_id: int,
    data: AimUpdate,
    db: Session = Depends(get_db)
):
    try:
        return AimService.update_aim(
            db,
            aim_id,
            data
        )

    except LookupError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Database constraint error while updating Aim"
        )


# DELETE
@router.delete("/{aim_id}")
def delete_aim(
    aim_id: int,
    db: Session = Depends(get_db)
):
    try:
        AimService.delete_aim(db, aim_id)

        return {
            "message": "Aim deleted successfully"
        }

    except LookupError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Aim cannot be deleted because it is being used"
        )