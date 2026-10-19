from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Integer,
    ForeignKey,
    TIMESTAMP
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Vehicle(Base):

    __tablename__ = "vehicles"

    __table_args__ = {
        "schema": "public"
    }

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        BigInteger,
        ForeignKey("public.customers.id"),
        nullable=False
    )

    registration_plate = Column(
        String(20),
        nullable=False,
        unique=True
    )

    brand = Column(
        String(100),
        nullable=False
    )

    model = Column(
        String(100),
        nullable=False
    )

    manufacture_year = Column(
        Integer,
        nullable=True
    )

    fuel_type = Column(
        String(50),
        nullable=True
    )

    vin = Column(
        String(17),
        nullable=True,
        unique=True
    )

    mileage = Column(
        Integer,
        nullable=True
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

    customer = relationship(
        "Customer",
        back_populates="vehicles"
    )

    repair_orders = relationship(
        "RepairOrder",
        back_populates="vehicle"
    )