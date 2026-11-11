
from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class FurnaceChargeMix(Base):
    __tablename__ = "furnace_charge_mixes"

    id = Column(Integer, primary_key=True, index=True)

    furnace_cycle_id = Column(
        Integer,
        ForeignKey("furnace_cycles.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
        index=True,
    )

    charging_capacity = Column(
        Numeric(12, 2),
        nullable=False,
    )

    total_charged_weight = Column(
        Numeric(12, 3),
        nullable=False,
        default=0,
        server_default="0",
    )

    status = Column(
        String(30),
        nullable=False,
        default="Draft",
        server_default="Draft",
        index=True,
    )

    confirmed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    items = relationship(
        "FurnaceChargeItem",
        back_populates="charge_mix",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class FurnaceChargeItem(Base):
    __tablename__ = "furnace_charge_items"

    id = Column(Integer, primary_key=True, index=True)

    charge_mix_id = Column(
        Integer,
        ForeignKey("furnace_charge_mixes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    raw_material_stock_id = Column(
        Integer,
        ForeignKey("raw_material_stocks.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    weight = Column(
        Numeric(12, 3),
        nullable=False,
    )

    rate_per_kg = Column(
        Numeric(12, 2),
        nullable=False,
    )

    bunker_name = Column(
        String(100),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    charge_mix = relationship(
        "FurnaceChargeMix",
        back_populates="items",
    )

    raw_material_stock = relationship(
        "RawMaterialStock",
        lazy="selectin",
    )

    elements = relationship(
        "FurnaceChargeItemElement",
        back_populates="charge_item",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    __table_args__ = (
        CheckConstraint("weight > 0", name="ck_charge_item_weight_positive"),
        CheckConstraint("rate_per_kg >= 0", name="ck_charge_item_rate_nonnegative"),
    )


class FurnaceChargeItemElement(Base):
    __tablename__ = "furnace_charge_elements"

    id = Column(Integer, primary_key=True, index=True)

    charge_item_id = Column(
        Integer,
        ForeignKey("furnace_charge_items.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    element_id = Column(
        Integer,
        ForeignKey("elements.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    percentage = Column(
        Numeric(5, 2),
        nullable=False,
    )

    charge_item = relationship(
        "FurnaceChargeItem",
        back_populates="elements",
    )

    element = relationship(
        "Element",
        lazy="joined",
    )

    __table_args__ = (
        UniqueConstraint(
            "charge_item_id",
            "element_id",
            name="uq_charge_item_element",
        ),
        CheckConstraint(
            "percentage >= 0 AND percentage <= 100",
            name="ck_charge_item_element_percentage",
        ),
    )
