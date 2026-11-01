from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    address = Column(String(500), nullable=False)
    phone_number = Column(String(20), nullable=False)