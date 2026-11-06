from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Numeric,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class WireStock(Base):
    __tablename__ = "wire_stocks"

    id = Column(Integer, primary_key=True, index=True)

    wire_id = Column(
        Integer,
        ForeignKey("wires.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    powder_weight_per_meter = Column(
        Numeric(12, 3),
        nullable=False,
    )

    quantity = Column(
        Numeric(12, 3),
        nullable=False,
    )

    supplier_id = Column(
        Integer,
        ForeignKey("suppliers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    rate_per_meter = Column(
        Numeric(12, 2),
        nullable=False,
    )

    wire = relationship("Wire", lazy="joined")
    supplier = relationship("Supplier", lazy="joined")

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