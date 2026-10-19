from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ServiceTypeBase(BaseModel):
    name: str
    description: str | None = None


class ServiceTypeCreate(ServiceTypeBase):
    pass


class ServiceTypeUpdate(ServiceTypeBase):
    pass


class ServiceTypeResponse(ServiceTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)