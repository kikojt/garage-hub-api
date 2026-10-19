from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.repair_order import RepairOrder
from app.models.repair_part import RepairPart
from app.models.repair_status import RepairStatus
from app.models.part import Part
from app.models.employee import Employee


class DashboardService:

    @staticmethod
    def get_dashboard(db: Session):

        pending = DashboardService.get_pending_repairs(db)

        in_progress = DashboardService.get_in_progress_repairs(db)

        completed = DashboardService.get_completed_repairs(db)

        low_stock = DashboardService.get_low_stock_parts(db)

        revenue = DashboardService.get_total_revenue(db)

        top_mechanic = DashboardService.get_top_mechanic(db)

        return {
            "pending_repairs": pending,
            "in_progress_repairs": in_progress,
            "completed_repairs": completed,
            "low_stock_parts": low_stock,
            "total_revenue": revenue,
            "top_mechanic": top_mechanic
        }

    @staticmethod
    def get_pending_repairs(db: Session):

        return (
            db.query(RepairOrder)
            .join(RepairStatus)
            .filter(
                RepairStatus.name == "Pending"
            )
            .count()
        )

    @staticmethod
    def get_in_progress_repairs(db: Session):

        return (
            db.query(RepairOrder)
            .join(RepairStatus)
            .filter(
                RepairStatus.name == "In Progress"
            )
            .count()
        )

    @staticmethod
    def get_completed_repairs(db: Session):

        return (
            db.query(RepairOrder)
            .join(RepairStatus)
            .filter(
                RepairStatus.name == "Completed"
            )
            .count()
        )

    @staticmethod
    def get_low_stock_parts(db: Session):

        return (
            db.query(Part)
            .filter(
                Part.stock_quantity <= 5
            )
            .count()
        )

    @staticmethod
    def get_total_revenue(db: Session):

        labour_total = (
            db.query(
                func.sum(
                    RepairOrder.labour_cost
                )
            )
            .scalar()
        )

        parts_total = (
            db.query(
                func.sum(
                    RepairPart.quantity * Part.unit_price
                )
            )
            .join(
                Part,
                RepairPart.part_id == Part.id
            )
            .scalar()
        )

        return (
            (labour_total or 0)
            +
            (parts_total or 0)
        )

    @staticmethod
    def get_top_mechanic(db: Session):

        result = (
            db.query(
                Employee.id,
                Employee.first_name,
                Employee.last_name,
                func.count(RepairOrder.id).label("total_repairs")
            )
            .join(
                RepairOrder,
                RepairOrder.employee_id == Employee.id
            )
            .group_by(
                Employee.id,
                Employee.first_name,
                Employee.last_name
            )
            .order_by(
                func.count(RepairOrder.id).desc()
            )
            .first()
        )

        if result is None:
            return None

        return {
            "employee_id": result.id,
            "name": f"{result.first_name} {result.last_name}",
            "total_repairs": result.total_repairs
        }