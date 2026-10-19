from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    Numeric,
    ForeignKey,
    TIMESTAMP
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class RepairPart(Base):

    __tablename__ = "repair_parts"

    __table_args__ = {
        "schema": "public"
    }

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    repair_order_id = Column(
        BigInteger,
        ForeignKey("public.repair_orders.id"),
        nullable=False
    )

    part_id = Column(
        BigInteger,
        ForeignKey("public.parts.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=1
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

    repair_order = relationship(
        "RepairOrder",
        back_populates="repair_parts"
    )

    part = relationship(
        "Part",
        back_populates="repair_parts"
    )