from sqlalchemy import (
    Column,
    BigInteger,
    String,
    TIMESTAMP
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Customer(Base):

    __tablename__ = "customers"

    __table_args__ = {
        "schema": "public"
    }

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    first_name = Column(
        String(100),
        nullable=False
    )

    last_name = Column(
        String(100),
        nullable=False
    )

    nif = Column(
        String(20),
        nullable=False,
        unique=True
    )

    phone = Column(
        String(20),
        nullable=True
    )

    email = Column(
        String(255),
        nullable=True
    )

    address = Column(
        String(255),
        nullable=True
    )

    postal_code = Column(
        String(20),
        nullable=True
    )

    city = Column(
        String(100),
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

    vehicles = relationship(
        "Vehicle",
        back_populates="customer"
    )