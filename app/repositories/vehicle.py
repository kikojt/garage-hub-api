from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate

class VehicleRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Vehicle).all()
    
    @staticmethod
    def get_by_id(db: Session, vehicle_id: int):
        return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    
    @staticmethod
    def get_by_registration_plate(db: Session, registration_plate: str):
        return db.query(Vehicle).filter(Vehicle.registration_plate == registration_plate).first()
    
    @staticmethod
    def get_by_vin(db: Session, vin: str):
        return db.query(Vehicle).filter(Vehicle.vin == vin).first()
    
    @staticmethod
    def get_by_customer_id(db: Session, customer_id: int):
        return db.query(Vehicle).filter(Vehicle.customer_id == customer_id).all()
    
    @staticmethod
    def create(db: Session, vehicle: VehicleCreate):
        db_vehicle = Vehicle(
            customer_id = vehicle.customer_id,
            registration_plate = vehicle.registration_plate,
            brand = vehicle.brand,
            model = vehicle.model,
            manufacture_year = vehicle.manufacture_year,
            fuel_type = vehicle.fuel_type,
            vin = vehicle.vin,
            mileage = vehicle.mileage
        )

        db.add(db_vehicle)
        db.commit()
        db.refresh(db_vehicle)

        return db_vehicle
    
    @staticmethod
    def update(db: Session, db_vehicle: Vehicle, vehicle: VehicleUpdate):
        db_vehicle.customer_id = vehicle.customer_id
        db_vehicle.registration_plate = vehicle.registration_plate
        db_vehicle.brand = vehicle.brand
        db_vehicle.model = vehicle.model
        db_vehicle.manufacture_year = vehicle.manufacture_year
        db_vehicle.fuel_type = vehicle.fuel_type
        db_vehicle.vin = vehicle.vin
        db_vehicle.mileage = vehicle.mileage

        db.commit()
        db.refresh(db_vehicle)

        return db_vehicle
    
    @staticmethod
    def delete(db: Session, db_vehicle: Vehicle):
        db.delete(db_vehicle)
        db.commit()


    @staticmethod
    def search(
        db: Session,
        registration_plate: str | None = None,
        vin: str | None = None,
        customer_id: int | None = None
    ):

        query = db.query(Vehicle)

        if registration_plate:
            query = query.filter(
                Vehicle.registration_plate == registration_plate
            )

        if vin:
            query = query.filter(
                Vehicle.vin == vin
            )

        if customer_id:
            query = query.filter(
                Vehicle.customer_id == customer_id
            )

        return query.all()