from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RepairPartBase(BaseModel):
    repair_order_id: int
    part_id: int
    quantity: int = Field(..., ge=1)


class RepairPartCreate(RepairPartBase):
    pass


class RepairPartUpdate(BaseModel):
    repair_order_id: int | None = None
    part_id: int | None = None
    quantity: int | None = Field(None, ge=1)


class RepairPartResponse(RepairPartBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)