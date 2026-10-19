from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RepairStatusBase(BaseModel):
    name: str
    description: str | None = None


class RepairStatusCreate(RepairStatusBase):
    pass


class RepairStatusUpdate(RepairStatusBase):
    pass


class RepairStatusResponse(RepairStatusBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)