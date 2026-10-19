from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Numeric,
    Date,
    ForeignKey,
    TIMESTAMP,
    Text
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class RepairOrder(Base):

    __tablename__ = "repair_orders"

    __table_args__ = {
        "schema": "public"
    }

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    vehicle_id = Column(
        BigInteger,
        ForeignKey("public.vehicles.id"),
        nullable=False
    )

    employee_id = Column(
        BigInteger,
        ForeignKey("public.employees.id"),
        nullable=True
    )

    status_id = Column(
        BigInteger,
        ForeignKey("public.repair_status.id"),
        nullable=False
    )

    service_type_id = Column(
        BigInteger,
        ForeignKey("public.service_types.id"),
        nullable=False
    )

    customer_notes = Column(
        Text,
        nullable=True
    )

    mechanic_notes = Column(
        Text,
        nullable=True
    )

    labour_cost = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    entry_date = Column(
        Date,
        nullable=False
    )

    expected_completion_date = Column(
        Date,
        nullable=True
    )

    completion_date = Column(
        Date,
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

    vehicle = relationship(
        "Vehicle",
        back_populates="repair_orders"
    )

    employee = relationship(
        "Employee",
        back_populates="repair_orders"
    )

    repair_status = relationship(
        "RepairStatus",
        back_populates="repair_orders"
    )

    service_type = relationship(
        "ServiceType",
        back_populates="repair_orders"
    )

    repair_parts = relationship(
        "RepairPart",
        back_populates="repair_order"
    )