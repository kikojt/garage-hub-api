from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class RepairOrderBase(BaseModel):
    vehicle_id: int
    employee_id: int
    status_id: int
    service_type_id: int
    customer_notes: str | None = None
    mechanic_notes: str | None = None
    labour_cost: Decimal = Field(..., ge=0)
    entry_date: date
    expected_completion_date: date | None = None
    completion_date: date | None = None


class RepairOrderCreate(RepairOrderBase):
    pass


class RepairOrderUpdate(BaseModel):
    vehicle_id: int | None = None
    employee_id: int | None = None
    status_id: int | None = None
    service_type_id: int | None = None
    customer_notes: str | None = None
    mechanic_notes: str | None = None
    labour_cost: Decimal | None = Field(None, ge=0)
    entry_date: date | None = None
    expected_completion_date: date | None = None
    completion_date: date | None = None


class RepairOrderResponse(RepairOrderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)