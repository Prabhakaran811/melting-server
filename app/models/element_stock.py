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


class ElementStock(Base):
    __tablename__ = "element_stocks"

    id = Column(Integer, primary_key=True, index=True)

    element_id = Column(
        Integer,
        ForeignKey("elements.id", ondelete="RESTRICT"),
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

    received_date = Column(
        Date,
        nullable=False
    )

    pickup_percentage = Column(
        Numeric(5, 2),
        nullable=False
    )

    rate_per_kg = Column(
        Numeric(12, 2),
        nullable=False
    )

    element = relationship(
        "Element",
        lazy="selectin"
    )

    supplier = relationship(
        "Supplier",
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