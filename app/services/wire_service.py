from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.wire_repository import WireRepository


class WireService:

    @staticmethod
    def validate_raw_material(db: Session, raw_material_id: int):
        raw_material = WireRepository.get_raw_material_by_id(
            db, raw_material_id
        )

        if not raw_material:
            raise HTTPException(
                status_code=404,
                detail="Selected Raw Material not found"
            )

        return raw_material

    @staticmethod
    def create_wire(db: Session, data: dict):
        name = data["name"].strip()
        raw_material_id = data["raw_material_id"]

        if not name:
            raise HTTPException(
                status_code=422,
                detail="Wire name cannot be empty"
            )

        existing = WireRepository.get_by_name(db, name)

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Wire name already exists"
            )

        WireService.validate_raw_material(db, raw_material_id)

        try:
            return WireRepository.create(
                db,
                name,
                raw_material_id
            )

        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Wire name already exists or Raw Material is invalid"
            )

    @staticmethod
    def get_wires(db: Session):
        return WireRepository.get_all(db)

    @staticmethod
    def update_wire(
        db: Session,
        wire_id: int,
        data: dict
    ):
        name = data["name"].strip()
        raw_material_id = data["raw_material_id"]

        if not name:
            raise HTTPException(
                status_code=422,
                detail="Wire name cannot be empty"
            )

        wire = WireRepository.get_by_id(db, wire_id)

        if not wire:
            raise HTTPException(
                status_code=404,
                detail="Wire not found"
            )

        existing = WireRepository.get_by_name(db, name)

        if existing and existing.id != wire_id:
            raise HTTPException(
                status_code=409,
                detail="Wire name already exists"
            )

        WireService.validate_raw_material(db, raw_material_id)

        try:
            return WireRepository.update(
                db,
                wire,
                name,
                raw_material_id
            )

        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Wire name already exists or Raw Material is invalid"
            )

    @staticmethod
    def delete_wire(db: Session, wire_id: int):
        wire = WireRepository.get_by_id(db, wire_id)

        if not wire:
            raise HTTPException(
                status_code=404,
                detail="Wire not found"
            )

        try:
            WireRepository.delete(db, wire)

        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Wire cannot be deleted because it is in use"
            )

        return {
            "message": "Wire permanently deleted"
        }