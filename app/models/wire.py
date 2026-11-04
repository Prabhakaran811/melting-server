from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Wire(Base):
    __tablename__ = "wires"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(150),
        nullable=False,
        unique=True,
        index=True
    )

    raw_material_id = Column(
        Integer,
        ForeignKey("raw_materials.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    raw_material = relationship(
        "RawMaterial",
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