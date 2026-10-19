from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Date,
    ForeignKey,
    TIMESTAMP
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Employee(Base):

    __tablename__ = "employees"

    __table_args__ = {
        "schema": "public"
    }

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("public.users.id"),
        nullable=False,
        unique=True
    )

    first_name = Column(
        String(100),
        nullable=False
    )

    last_name = Column(
        String(100),
        nullable=False
    )

    phone = Column(
        String(20),
        nullable=True
    )

    hire_date = Column(
        Date,
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

    user = relationship(
        "User",
        back_populates="employee"
    )

    repair_orders = relationship(
        "RepairOrder",
        back_populates="employee"
    )