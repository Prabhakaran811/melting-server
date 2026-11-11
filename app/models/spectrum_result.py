
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Numeric,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class SpectrumResult(Base):
    __tablename__ = "spectrum_results"

    id = Column(Integer, primary_key=True, index=True)

    furnace_cycle_id = Column(
        Integer,
        ForeignKey("furnace_cycles.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    test_number = Column(Integer, nullable=False)

    # Assigned later by MES if the machine doesn't send it.
    test_stage = Column(String(50), nullable=True)

    operator_name = Column(String(100), nullable=True)

    result_status = Column(
        String(20),
        nullable=False,
        default="Pending",
        server_default="Pending",
    )

    raw_payload = Column(Text, nullable=False)

    received_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    elements = relationship(
        "SpectrumResultElement",
        back_populates="spectrum_result",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "furnace_cycle_id",
            "test_number",
            name="uq_spectrum_result_cycle_test",
        ),
        CheckConstraint(
            "test_number > 0",
            name="ck_spectrum_result_test_number_positive",
        ),
    )


class SpectrumResultElement(Base):
    __tablename__ = "spectrum_result_elements"

    id = Column(Integer, primary_key=True, index=True)

    spectrum_result_id = Column(
        Integer,
        ForeignKey("spectrum_results.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    element_symbol = Column(String(20), nullable=False)

    element_name = Column(String(100), nullable=True)

    percentage = Column(
        Numeric(12, 6),
        nullable=False,
    )

    spectrum_result = relationship(
        "SpectrumResult",
        back_populates="elements",
    )

    __table_args__ = (
        UniqueConstraint(
            "spectrum_result_id",
            "element_symbol",
            name="uq_spectrum_result_element",
        ),
    )
