from sqlalchemy import (
    Column,
    BigInteger,
    String,
    TIMESTAMP
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Supplier(Base):

    __tablename__ = "suppliers"

    __table_args__ = {
        "schema": "public"
    }

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    company_name = Column(
        String(150),
        nullable=False,
        unique=True
    )

    contact_name = Column(
        String(100),
        nullable=True
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

    parts = relationship(
        "Part",
        back_populates="supplier"
    )