from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.base import Base


class FeSiGranule(Base):
    __tablename__ = "fesi_granules"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False, unique=True, index=True)

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