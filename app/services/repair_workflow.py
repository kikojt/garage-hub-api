from sqlalchemy.orm import Session

from app.core.repair_status_rules import can_change_status
from app.repositories.repair_order import RepairOrderRepository
from app.repositories.repair_status import RepairStatusRepository
from app.repositories.part import PartRepository
from app.repositories.repair_part import RepairPartRepository

from app.repositories.employee import EmployeeRepository
from app.core.repair_status_rules import is_final_status


class RepairWorkflowService:
    pass

    @staticmethod
    def change_status(db: Session, repair_order_id: int, new_status_id: int):
        repair_order = RepairOrderRepository.get_by_id(db, repair_order_id)

        if repair_order is None:
            raise ValueError("Repair order not found.")
        
        new_status = RepairStatusRepository.get_by_id(db, new_status_id)

        if new_status is None:
            raise ValueError("Repair status not found.")
        
        current_status = RepairStatusRepository.get_by_id(
            db,
            repair_order.status_id
        )

        current_status_name = current_status.name
        new_status_name = new_status.name

        # Validar a transição do estado
        if not can_change_status(current_status_name, new_status_name):
            raise ValueError(
                f"Cannot change status from '{current_status_name}' to '{new_status_name}'."
            )

        repair_order.status_id = new_status.id

        return RepairOrderRepository.update_status(db, repair_order, new_status.id)


    @staticmethod
    def assign_employee(db: Session, repair_order_id: int, employee_id: int):
        repair_order = RepairOrderRepository.get_by_id(db, repair_order_id)

        if repair_order is None:
            raise ValueError("Repair order not found.")

        employee = EmployeeRepository.get_by_id(db, employee_id)

        if employee is None:
            raise ValueError("Employee not found.")

        if not EmployeeRepository.is_active(employee):
            raise ValueError("Employee user is inactive.")

        current_status = RepairStatusRepository.get_by_id(db, repair_order.status_id)

        if is_final_status(current_status.name):
            raise ValueError(
                "Cannot assign an employee to a closed repair order."
            )
        if repair_order.employee_id == employee_id:
            return repair_order

        return RepairOrderRepository.assign_employee(db, repair_order, employee_id)
    
    @staticmethod
    def add_part(db: Session, repair_order_id: int, part_id: int, quantity: int):
        repair_order = RepairOrderRepository.get_by_id(db, repair_order_id)

        if repair_order is None:
            raise ValueError("Repair order not found.")

        current_status = RepairStatusRepository.get_by_id(db, repair_order.status_id)

        if is_final_status(current_status.name):
            raise ValueError("Cannot add part to a closed repair order.")

        part = PartRepository.get_by_id(db, part_id)

        if part is None:
            raise ValueError("Part not found.")

        if part.stock_quantity < quantity:
            raise ValueError("Insufficient stock.")

        repair_part = RepairPartRepository.get_by_repair_order_and_part(db, repair_order_id, part_id)

        if repair_part:
            repair_part = RepairPartRepository.update(db, repair_part, repair_part.quantity + quantity)
        else:
            repair_part = RepairPartRepository.create(db, repair_order_id, part_id, quantity, part.unit_price)

        PartRepository.decrease_stock(db, part, quantity)

        return repair_part
    
    @staticmethod
    def remove_part(
        db: Session,
        repair_order_id: int,
        part_id: int
    ):
        repair_order = RepairOrderRepository.get_by_id(
            db,
            repair_order_id
        )

        if repair_order is None:
            raise ValueError("Repair order not found.")

        current_status = RepairStatusRepository.get_by_id(
            db,
            repair_order.status_id
        )

        if is_final_status(current_status.name):
            raise ValueError(
                "Cannot remove parts from a closed repair order."
            )

        repair_part = RepairPartRepository.get_by_repair_order_and_part(
            db,
            repair_order_id,
            part_id
        )

        if repair_part is None:
            raise ValueError(
                "Part is not assigned to this repair order."
            )

        part = PartRepository.get_by_id(
            db,
            part_id
        )

        if part is None:
            raise ValueError("Part not found.")

        PartRepository.increase_stock(
            db,
            part,
            repair_part.quantity
        )

        RepairPartRepository.delete(
            db,
            repair_part
        )

        return True


    @staticmethod
    def update_part_quantity(
        db: Session,
        repair_order_id: int,
        part_id: int,
        new_quantity: int
    ):
        repair_order = RepairOrderRepository.get_by_id(
            db,
            repair_order_id
        )

        if repair_order is None:
            raise ValueError("Repair order not found.")

        current_status = RepairStatusRepository.get_by_id(
            db,
            repair_order.status_id
        )

        if is_final_status(current_status.name):
            raise ValueError(
                "Cannot update parts in a closed repair order."
            )

        repair_part = RepairPartRepository.get_by_repair_order_and_part(
            db,
            repair_order_id,
            part_id
        )

        if repair_part is None:
            raise ValueError(
                "Part is not assigned to this repair order."
            )

        part = PartRepository.get_by_id(
            db,
            part_id
        )

        if part is None:
            raise ValueError("Part not found.")

        # Calcula a diferença entre a nova quantidade e a atual
        difference = new_quantity - repair_part.quantity

        # A quantidade mantém-se igual
        if difference == 0:
            return repair_part

        # Aumentar quantidade
        if difference > 0:

            if part.stock_quantity < difference:
                raise ValueError("Insufficient stock.")

            PartRepository.decrease_stock(
                db,
                part,
                difference
            )

        # Diminuir quantidade
        else:

            PartRepository.increase_stock(
                db,
                part,
                abs(difference)
            )

        repair_part = RepairPartRepository.update(
            db,
            repair_part,
            new_quantity
        )

        return repair_part
    
    
    @staticmethod
    def complete_repair(
        db: Session,
        repair_order_id: int
    ):
        repair_order = RepairOrderRepository.get_by_id(
            db,
            repair_order_id
        )

        if repair_order is None:
            raise ValueError("Repair order not found.")

        if repair_order.employee_id is None:
            raise ValueError(
                "Repair order has no assigned employee."
            )

        completed_status = RepairStatusRepository.get_by_name(
            db,
            "Completed"
        )

        if completed_status is None:
            raise ValueError(
                "Completed status not found."
            )

        return RepairWorkflowService.change_status(
            db,
            repair_order_id,
            completed_status.id
        )
        
        
    @staticmethod
    def cancel_repair(
        db: Session,
        repair_order_id: int
    ):
        repair_order = RepairOrderRepository.get_by_id(
            db,
            repair_order_id
        )

        if repair_order is None:
            raise ValueError("Repair order not found.")

        cancelled_status = RepairStatusRepository.get_by_name(
            db,
            "Cancelled"
        )

        if cancelled_status is None:
            raise ValueError(
                "Cancelled status not found."
            )

        repair_parts = RepairPartRepository.get_by_repair_order(
            db,
            repair_order_id
        )

        for repair_part in repair_parts:

            part = PartRepository.get_by_id(
                db,
                repair_part.part_id
            )

            if part:
                PartRepository.increase_stock(
                    db,
                    part,
                    repair_part.quantity
                )

            RepairPartRepository.delete(
                db,
                repair_part
            )

        return RepairWorkflowService.change_status(
            db,
            repair_order_id,
            cancelled_status.id
        )
        