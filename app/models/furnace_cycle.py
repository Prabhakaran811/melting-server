
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    ForeignKey,
    Index,
    func,
    text,
)
from app.db.base import Base


class FurnaceCycle(Base):
    __tablename__ = "furnace_cycles"

    id = Column(Integer, primary_key=True, index=True)

    furnace_id = Column(
        Integer,
        ForeignKey("furnaces.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    heat_no = Column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
    )

    furnace_capacity = Column(
        Numeric(12, 2),
        nullable=False,
    )

    status = Column(
        String(30),
        nullable=False,
        default="Running",
        server_default="Running",
        index=True,
    )

    active_stage = Column(
        String(50),
        nullable=False,
        default="Charging",
        server_default="Charging",
    )

    started_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    completed_at = Column(
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

    __table_args__ = (
        Index(
            "uq_furnace_cycles_one_running_per_furnace",
            "furnace_id",
            unique=True,
            postgresql_where=text("status = 'Running'"),
        ),
    )
