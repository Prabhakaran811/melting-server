from sqlalchemy import Column, Integer, String, DateTime, func

from app.db.base import Base


class Hardness(Base):
    __tablename__ = "hardnesses"

    id = Column(Integer, primary_key=True, index=True)

    hardness_name = Column(
        String(150),
        nullable=False,
        unique=True,
        index=True
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