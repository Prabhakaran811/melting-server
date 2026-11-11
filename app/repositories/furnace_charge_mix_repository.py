
from sqlalchemy.orm import Session, joinedload, selectinload, lazyload

from app.models.furnace import Furnace
from app.models.furnace_cycle import FurnaceCycle
from app.models.furnace_charge_mix import (
    FurnaceChargeMix,
    FurnaceChargeItem,
    FurnaceChargeItemElement,
    
)
from app.models.raw_material_stock import (RawMaterialStock, RawMaterialStockElement)


class FurnaceChargeMixRepository:

    @staticmethod
    def get_furnace_for_update(db: Session, furnace_id: int):
        return (
            db.query(Furnace)
            .filter(Furnace.id == furnace_id)
            .with_for_update(of=Furnace)
            .first()
        )

    @staticmethod
    def get_running_cycle(db: Session, furnace_id: int):
        return (
            db.query(FurnaceCycle)
            .options(lazyload("*"))
            .filter(
                FurnaceCycle.furnace_id == furnace_id,
                FurnaceCycle.status == "Running",
            )
            .with_for_update(of=FurnaceCycle)
            .first()
        )

    @staticmethod
    def get_mix_by_cycle(db: Session, cycle_id: int):
        return (
            db.query(FurnaceChargeMix)
            .options(
                selectinload(FurnaceChargeMix.items)
                .joinedload(FurnaceChargeItem.raw_material_stock),

                selectinload(FurnaceChargeMix.items)
                .selectinload(FurnaceChargeItem.elements)
                .joinedload(FurnaceChargeItemElement.element),
            )
            .filter(FurnaceChargeMix.furnace_cycle_id == cycle_id)
            .first()
        )

    @staticmethod
    def get_mix_for_update(db: Session, cycle_id: int):
        return (
            db.query(FurnaceChargeMix)
            .options(lazyload("*"))
            .filter(FurnaceChargeMix.furnace_cycle_id == cycle_id)
            .with_for_update(of=FurnaceChargeMix)
            .first()
        )

    @staticmethod
    def get_mix_by_id(db: Session, mix_id: int):
        return (
            db.query(FurnaceChargeMix)
            .options(
                selectinload(FurnaceChargeMix.items)
                .joinedload(FurnaceChargeItem.raw_material_stock),

                selectinload(FurnaceChargeMix.items)
                .selectinload(FurnaceChargeItem.elements)
                .joinedload(FurnaceChargeItemElement.element),
            )
            .filter(FurnaceChargeMix.id == mix_id)
            .first()
        )

    @staticmethod
    def get_stock_for_update(db: Session, stock_id: int):
        return (
            db.query(RawMaterialStock)
            .options(
                lazyload("*"),
                selectinload(RawMaterialStock.element_percentages)
                .joinedload(RawMaterialStockElement.element)
            )
            .filter(RawMaterialStock.id == stock_id)
            .with_for_update(of=RawMaterialStock)
            .first()
        )

    @staticmethod
    def get_item(db: Session, mix_id: int, item_id: int):
        return (
            db.query(FurnaceChargeItem)
            .filter(
                FurnaceChargeItem.id == item_id,
                FurnaceChargeItem.charge_mix_id == mix_id,
            )
            .first()
        )

    @staticmethod
    def create_mix(db: Session, cycle: FurnaceCycle):
        mix = FurnaceChargeMix(
            furnace_cycle_id=cycle.id,
            charging_capacity=cycle.furnace_capacity,
            total_charged_weight=0,
            status="Draft",
        )

        db.add(mix)
        db.flush()

        return mix

    @staticmethod
    def add_item(
        db: Session,
        mix_id: int,
        stock: RawMaterialStock,
        weight,
        bunker_name,
    ):
        item = FurnaceChargeItem(
            charge_mix_id=mix_id,
            raw_material_stock_id=stock.id,
            weight=weight,
            rate_per_kg=stock.rate_per_kg,
            bunker_name=bunker_name,
        )

        db.add(item)
        db.flush()

        for stock_element in stock.element_percentages:
            db.add(
                FurnaceChargeItemElement(
                    charge_item_id=item.id,
                    element_id=stock_element.element_id,
                    percentage=stock_element.percentage,
                )
            )

        db.flush()
        return item

    @staticmethod
    def update_item(
        db: Session,
        item: FurnaceChargeItem,
        stock: RawMaterialStock,
        weight,
        bunker_name,
    ):
        item.raw_material_stock_id = stock.id
        item.weight = weight
        item.rate_per_kg = stock.rate_per_kg
        item.bunker_name = bunker_name

        # Replace the saved element snapshot.
        item.elements.clear()

        db.flush()

        for stock_element in stock.element_percentages:
            item.elements.append(
                FurnaceChargeItemElement(
                    element_id=stock_element.element_id,
                    percentage=stock_element.percentage,
                )
            )

        db.flush()
        return item

    @staticmethod
    def delete_item(db: Session, item: FurnaceChargeItem):
        db.delete(item)
        db.flush()

    @staticmethod
    def recalculate_total(db: Session, mix: FurnaceChargeMix):
        total = sum(
            (item.weight for item in mix.items),
            start=0,
        )

        mix.total_charged_weight = total
        db.flush()

        return total
