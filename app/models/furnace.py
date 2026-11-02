from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    Numeric,
    String,
    func,
)

from app.db.base import Base


class Furnace(Base):
    __tablename__ = "furnaces"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)
    furnace_no = Column(String(50), nullable=False, unique=True, index=True)
    ref_no = Column(String(50), nullable=False, unique=True, index=True)

    capacity = Column(Numeric(12, 2), nullable=False)

    is_active = Column(Boolean, nullable=False, default=True)

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