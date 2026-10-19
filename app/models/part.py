from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Integer,
    Numeric,
    ForeignKey,
    TIMESTAMP
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Part(Base):

    __tablename__ = "parts"

    __table_args__ = {
        "schema": "public"
    }

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    supplier_id = Column(
        BigInteger,
        ForeignKey("public.suppliers.id"),
        nullable=False
    )

    name = Column(
        String(150),
        nullable=False
    )

    part_number = Column(
        String(100),
        nullable=False,
        unique=True
    )

    stock_quantity = Column(
        Integer,
        nullable=False,
        default=0
    )

    unit_price = Column(
        Numeric(10, 2),
        nullable=False
    )

    created_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now()
    )

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    supplier = relationship(
        "Supplier",
        back_populates="parts"
    )

    repair_parts = relationship(
        "RepairPart",
        back_populates="part"
    )