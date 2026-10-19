from sqlalchemy import (
    Column,
    BigInteger,
    String,
    TIMESTAMP
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class RepairStatus(Base):

    __tablename__ = "repair_status"

    __table_args__ = {
        "schema": "public"
    }

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    name = Column(
        String(50),
        nullable=False,
        unique=True
    )

    description = Column(
        String(255),
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

    repair_orders = relationship(
        "RepairOrder",
        back_populates="repair_status"
    )