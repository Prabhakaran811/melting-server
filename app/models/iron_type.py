from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey,
    Table, func
)
from sqlalchemy.orm import relationship

from app.db.base import Base


iron_type_elements = Table(
    "iron_type_elements",
    Base.metadata,

    Column(
        "iron_type_id",
        Integer,
        ForeignKey("iron_types.id", ondelete="CASCADE"),
        primary_key=True
    ),

    Column(
        "element_id",
        Integer,
        ForeignKey("elements.id", ondelete="RESTRICT"),
        primary_key=True
    )
)


class IronType(Base):
    __tablename__ = "iron_types"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(150),
        nullable=False,
        unique=True,
        index=True
    )

    elements = relationship(
        "Element",
        secondary=iron_type_elements,
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