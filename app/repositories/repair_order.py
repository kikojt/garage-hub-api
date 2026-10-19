from datetime import date

from sqlalchemy.orm import Session

from app.models.repair_order import RepairOrder
from app.models.vehicle import Vehicle
from app.schemas.repair_order import RepairOrderCreate


class RepairOrderRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(RepairOrder).all()

    @staticmethod
    def get_by_id(db: Session, repair_order_id: int):
        return db.query(RepairOrder).filter(RepairOrder.id == repair_order_id).first()

    @staticmethod
    def create(db: Session, repair_order: RepairOrderCreate):
        db_repair_order = RepairOrder(
            vehicle_id = repair_order.vehicle_id,
            employee_id = repair_order.employee_id,
            status_id = repair_order.status_id,
            service_type_id = repair_order.service_type_id,
            customer_notes = repair_order.customer_notes,
            mechanic_notes = repair_order.mechanic_notes,
            labour_cost = repair_order.labour_cost,
            entry_date = repair_order.entry_date,
            expected_completion_date = repair_order.expected_completion_date,
            completion_date = repair_order.completion_date
        )

        db.add(db_repair_order)
        db.commit()
        db.refresh(db_repair_order)

        return db_repair_order

    @staticmethod
    def delete(db: Session, db_repair_order: RepairOrder):
        db.delete(db_repair_order)
        db.commit()


    @staticmethod
    def update_status(db: Session, repair_order: RepairOrder, status_id: int):
        repair_order.status_id = status_id

        db.commit()
        db.refresh(repair_order)

        return repair_order


    @staticmethod
    def assign_employee(db: Session, repair_order: RepairOrder, employee_id: int):
        repair_order.employee_id = employee_id

        db.commit()
        db.refresh(repair_order)

        return repair_order


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

        query = db.query(RepairOrder).join(Vehicle)
    
        if registration_plate:
            query = query.filter(Vehicle.registration_plate == registration_plate)

        if customer_id:
            query = query.filter(Vehicle.customer_id == customer_id)

        if status_id:
            query = query.filter(RepairOrder.status_id == status_id)

        if employee_id:
            query = query.filter(RepairOrder.employee_id == employee_id)

        if start_date:
            query = query.filter(
                RepairOrder.entry_date >= start_date
            )

        if end_date:
            query = query.filter(
                RepairOrder.entry_date <= end_date
            )

        return query.all()

