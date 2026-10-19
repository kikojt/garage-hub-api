from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VehicleBase(BaseModel):
    customer_id: int
    registration_plate: str
    brand: str
    model: str
    manufacture_year: int
    fuel_type: str
    vin: str | None = None
    mileage: int


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    customer_id: int | None = None
    registration_plate: str | None = None
    brand: str | None = None
    model: str | None = None
    manufacture_year: int | None = None
    fuel_type: str | None = None
    vin: str | None = None
    mileage: int | None = None


class VehicleResponse(VehicleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)