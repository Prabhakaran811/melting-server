from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Numeric,
    DateTime,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Aim(Base):
    __tablename__ = "aims"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    drawing_no = Column(String(100), nullable=False, index=True)

    iron_type_id = Column(
        Integer,
        ForeignKey("iron_types.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    packing_id = Column(
        Integer,
        ForeignKey("packings.id", ondelete="RESTRICT"),
        nullable=False,
    )

    hardness_id = Column(
        Integer,
        ForeignKey("hardnesses.id", ondelete="RESTRICT"),
        nullable=False,
    )

    inoculant_id = Column(
        Integer,
        ForeignKey("inoculants.id", ondelete="RESTRICT"),
        nullable=False,
    )

    pouring_weight_kg = Column(Numeric(12, 3), nullable=False)

    casting_weight_kg = Column(Numeric(12, 3), nullable=False)

    no_of_casting = Column(Integer, nullable=False)

    no_of_cavity = Column(Integer, nullable=False)

    # Master relationships
    customer = relationship("Customer", lazy="joined")
    product = relationship("Product", lazy="joined")
    iron_type = relationship("IronType", lazy="joined")
    packing = relationship("Packing", lazy="joined")
    hardness = relationship("Hardness", lazy="joined")
    inoculant = relationship("Inoculant", lazy="joined")

    # Child element values
    elements = relationship(
        "AimElement",
        back_populates="aim",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class AimElement(Base):
    __tablename__ = "aim_elements"

    __table_args__ = (
        UniqueConstraint(
            "aim_id",
            "element_id",
            name="uq_aim_element",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    aim_id = Column(
        Integer,
        ForeignKey("aims.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    element_id = Column(
        Integer,
        ForeignKey("elements.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    exact_value = Column(Numeric(12, 4), nullable=False)

    plus_value = Column(Numeric(12, 4), nullable=False)

    minus_value = Column(Numeric(12, 4), nullable=False)

    aim = relationship(
        "Aim",
        back_populates="elements",
    )

    element = relationship(
        "Element",
        lazy="joined",
    )