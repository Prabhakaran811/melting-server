from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Table,
    func
)
from sqlalchemy.orm import relationship

from app.db.base import Base


raw_material_elements = Table(
    "raw_material_elements",
    Base.metadata,

    Column(
        "raw_material_id",
        Integer,
        ForeignKey("raw_materials.id", ondelete="CASCADE"),
        primary_key=True
    ),

    Column(
        "element_id",
        Integer,
        ForeignKey("elements.id", ondelete="RESTRICT"),
        primary_key=True
    )
)


class RawMaterial(Base):

    __tablename__ = "raw_materials"

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

    elements = relationship(
        "Element",
        secondary=raw_material_elements,
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