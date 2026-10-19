from sqlalchemy.orm import Session

from app.repositories.customer import CustomerRepository
from app.repositories.vehicle import VehicleRepository
from app.schemas.vehicle import VehicleCreate, VehicleUpdate

class VehicleService:

    @staticmethod
    def get_all_vehicles(db: Session):
        return VehicleRepository.get_all(db)
    
    @staticmethod
    def get_vehicle_by_id(db: Session, vehicle_id: int):
        return VehicleRepository.get_by_id(db, vehicle_id)
    
    @staticmethod
    def get_vehicles_by_customer(db: Session, customer_id: int):
        customer = CustomerRepository.get_by_id(db, customer_id)

        if customer is None:
            return None

        return VehicleRepository.get_by_customer_id(db, customer_id)
    
    @staticmethod
    def create_vehicle(db: Session, vehicle: VehicleCreate):
        existing_customer = CustomerRepository.get_by_id(db, vehicle.customer_id)

        if existing_customer is None:
            raise ValueError("Customer not found.")
        
        existing_plate = VehicleRepository.get_by_registration_plate(db, vehicle.registration_plate)

        if existing_plate is not None:
            raise ValueError("Registration plate already exists.")
        
        existing_vin = VehicleRepository.get_by_vin(db, vehicle.vin)

        if existing_vin is not None:
            raise ValueError("VIN already exists.")
        
        return VehicleRepository.create(db, vehicle)
    
    # falta editar PUT
    # .... in progress


    @staticmethod
    def delete_vehicle(db: Session, vehicle_id: int):
        db_vehicle = VehicleRepository.get_by_id(db, vehicle_id)

        if db_vehicle is None:
            return None
        
        VehicleRepository.delete(db, db_vehicle)

        return True


    @staticmethod
    def search_vehicles(
        db: Session,
        registration_plate: str | None = None,
        vin: str | None = None,
        customer_id: int | None = None
    ):
        return VehicleRepository.search(
            db,
            registration_plate,
            vin,
            customer_id
        )
