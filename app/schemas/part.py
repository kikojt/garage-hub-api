from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PartBase(BaseModel):
    supplier_id: int
    name: str
    part_number: str
    stock_quantity: int = Field(..., ge=0)
    unit_price: Decimal = Field(..., ge=0)


class PartCreate(PartBase):
    pass


class PartUpdate(BaseModel):
    supplier_id: int | None = None
    name: str | None = None
    part_number: str | None = None
    stock_quantity: int | None = Field(None, ge=0)
    unit_price: Decimal | None = Field(None, ge=0)


class PartResponse(PartBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)