from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse
from app.services.vehicle import VehicleService

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)

@router.get("/", response_model=list[VehicleResponse])
def get_all_vehicles(db: Session = Depends(get_db)):
    return VehicleService.get_all_vehicles(db)

@router.get("/search", response_model=list[VehicleResponse])
def search_vehicles(
    registration_plate: str | None = None,
    vin: str | None = None,
    customer_id: int | None = None,
    db: Session = Depends(get_db)
):
    return VehicleService.search_vehicles(
        db,
        registration_plate,
        vin,
        customer_id
    )

@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle( vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = VehicleService.get_vehicle_by_id(db, vehicle_id)

    if vehicle is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found."
        )
    
    return vehicle

@router.get("/customers/{customer_id}/vehicles", response_model=list[VehicleResponse])
def get_customer_vehicles(customer_id: int, db: Session = Depends(get_db)):
    vehicles = VehicleService.get_vehicles_by_customer(db, customer_id)

    if vehicles is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    return vehicles

@router.post("/", response_model=VehicleResponse)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    try:
        return VehicleService.create_vehicle(db, vehicle)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

## Falta o PUT


@router.delete("/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    deleted = VehicleService.delete_vehicle(db, vehicle_id)

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found."
        )

    return {
        "message": "Vehicle deleted successfully."
    }
