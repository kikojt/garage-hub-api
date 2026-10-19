from datetime import date

from sqlalchemy.orm import Session

from app.repositories.employee import EmployeeRepository
from app.repositories.repair_order import RepairOrderRepository
from app.repositories.repair_status import RepairStatusRepository
from app.repositories.service_type import ServiceTypeRepository
from app.repositories.vehicle import VehicleRepository
from app.schemas.repair_order import RepairOrderCreate


class RepairOrderService:

    @staticmethod
    def get_all_repair_orders(db: Session):
        return RepairOrderRepository.get_all(db)

    @staticmethod
    def get_repair_order_by_id(db: Session, repair_order_id: int):
        return RepairOrderRepository.get_by_id(db, repair_order_id)

    @staticmethod
    def create_repair_order(db: Session, repair_order: RepairOrderCreate):

        existing_vehicle = VehicleRepository.get_by_id(
            db,
            repair_order.vehicle_id
        )

        if existing_vehicle is None:
            raise ValueError("Vehicle not found.")

        existing_employee = EmployeeRepository.get_by_id(
            db,
            repair_order.employee_id
        )

        if existing_employee is None:
            raise ValueError("Employee not found.")

        existing_repair_status = RepairStatusRepository.get_by_id(
            db,
            repair_order.status_id
        )

        if existing_repair_status is None:
            raise ValueError("Repair status not found.")

        existing_service_type = ServiceTypeRepository.get_by_id(
            db,
            repair_order.service_type_id
        )

        if existing_service_type is None:
            raise ValueError("Service type not found.")

        return RepairOrderRepository.create(db, repair_order)

    @staticmethod
    def delete_repair_order(db: Session, repair_order_id: int):

        db_repair_order = RepairOrderRepository.get_by_id(
            db,
            repair_order_id
        )

        if db_repair_order is None:
            return None

        RepairOrderRepository.delete(db, db_repair_order)

        return True

    @staticmethod
    def search(
        db: Session,
        registration_plate: str | None = None,
        customer_id: int | None = None,
        status_id: int | None = None,
        employee_id: int | None = None,
        start_date: date | None = None,
        end_date: date | None = None
    ):

        return RepairOrderRepository.search(
            db,
            registration_plate,
            customer_id,
            status_id,
            employee_id,
            start_date,
            end_date
        )