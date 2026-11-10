from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    order_number = Column(
        String(30),
        unique=True,
        nullable=False,
        index=True
    )

    aim_id = Column(
        Integer,
        ForeignKey("aims.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    status = Column(
        String(30),
        nullable=False,
        default="Pending",
        server_default="Pending"
    )

    customer_delivery_date = Column(
        Date,
        nullable=False
    )

    aim = relationship(
        "Aim",
        lazy="joined"
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