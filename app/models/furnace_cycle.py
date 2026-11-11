
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Date,
    ForeignKey,
    Numeric,
    func,
    Index,
    text,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class FurnaceCycle(Base):
    __tablename__ = "furnace_cycles"

    id = Column(Integer, primary_key=True, index=True)

    furnace_id = Column(
        Integer,
        ForeignKey("furnaces.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    heat_no = Column(
        String(30),
        unique=True,
        nullable=False,
        index=True
    )

    furnace_capacity = Column(
        Numeric(12, 2),
        nullable=False
    )

    status = Column(
        String(30),
        nullable=False,
        default="Running",
        server_default="Running"
    )

    active_stage = Column(
        String(50),
        nullable=False,
        default="Started",
        server_default="Started"
    )

    shift = Column(Integer, nullable=True)

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
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

    furnace = relationship("Furnace", lazy="joined")

    order = relationship("Order", lazy="joined")

    stages = relationship(
        "FurnaceCycleStage",
        back_populates="furnace_cycle",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="FurnaceCycleStage.id"
    )

    __table_args__ = (
        Index(
            "uq_one_running_cycle_per_furnace",
            "furnace_id",
            unique=True,
            postgresql_where=text("status = 'Running'")
        ),
    )


class FurnaceCycleStage(Base):
    __tablename__ = "furnace_cycle_stages"

    id = Column(Integer, primary_key=True, index=True)

    furnace_cycle_id = Column(
        Integer,
        ForeignKey("furnace_cycles.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    stage_name = Column(
        String(50),
        nullable=False
    )

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    furnace_cycle = relationship(
        "FurnaceCycle",
        back_populates="stages"
    )
