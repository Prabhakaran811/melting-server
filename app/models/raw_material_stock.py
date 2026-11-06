from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    Date,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class RawMaterialStock(Base):
    __tablename__ = "raw_material_stocks"

    id = Column(Integer, primary_key=True, index=True)

    raw_material_id = Column(
        Integer,
        ForeignKey("raw_materials.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    quantity = Column(
        Numeric(12, 3),
        nullable=False
    )

    supplier_id = Column(
        Integer,
        ForeignKey("suppliers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    received_date = Column(Date, nullable=False)

    rate_per_kg = Column(
        Numeric(12, 2),
        nullable=False
    )

    raw_material = relationship(
        "RawMaterial",
        lazy="selectin"
    )

    supplier = relationship(
        "Supplier",
        lazy="selectin"
    )

    element_percentages = relationship(
        "RawMaterialStockElement",
        back_populates="stock",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


class RawMaterialStockElement(Base):
    __tablename__ = "raw_material_stock_elements"

    id = Column(Integer, primary_key=True, index=True)

    stock_id = Column(
        Integer,
        ForeignKey("raw_material_stocks.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    element_id = Column(
        Integer,
        ForeignKey("elements.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    percentage = Column(
        Numeric(5, 2),
        nullable=False
    )

    stock = relationship(
        "RawMaterialStock",
        back_populates="element_percentages"
    )

    element = relationship(
        "Element",
        lazy="joined"
    )