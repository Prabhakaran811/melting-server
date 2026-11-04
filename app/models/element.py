from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.base import Base
from sqlalchemy.orm import relationship

class Element(Base):
    __tablename__ = "elements"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False, unique=True, index=True)

    abbreviation = Column(
        String(20),
        nullable=False,
        unique=True,
        index=True
    )

    sequence_order = Column(Integer, nullable=False)

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

    iron_types = relationship(
    "IronType",
    secondary="iron_type_elements",
    viewonly=True,
    lazy="selectin"
)