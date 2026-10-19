from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.user import UserResponse


class EmployeeBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    phone: str | None = None
    hire_date: date


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    user_id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    hire_date: date | None = None


class EmployeeResponse(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    user: UserResponse

    model_config = ConfigDict(from_attributes=True)