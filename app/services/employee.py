from sqlalchemy.orm import Session

from app.repositories.employee import EmployeeRepository
from app.repositories.user import UserRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate

class EmployeeService:

    @staticmethod
    def get_all_employees(db: Session):
        return EmployeeRepository.get_all(db)
    
    @staticmethod
    def get_employee_by_id(db: Session, employee_id: int):
        return EmployeeRepository.get_by_id(db, employee_id)
    
    @staticmethod
    def create_employee(db: Session, employee: EmployeeCreate):
        existing_user = UserRepository.get_by_id(db, employee.user_id)

        if existing_user is None:
            raise ValueError("User not found.")

        existing_employee = EmployeeRepository.get_by_user_id(db, employee.user_id)

        if existing_employee:
            raise ValueError("This user is already assigned to an employee.")

        return EmployeeRepository.create(db, employee)
    
    @staticmethod
    def delete_employee(db: Session, employee_id: int):
        db_employee = EmployeeRepository.get_by_id(db, employee_id)

        if db_employee is None:
            return None

        EmployeeRepository.delete(db, db_employee)

        return True

    @staticmethod
    def search_employees(
        db: Session,
        name: str | None = None,
        is_active: bool | None = None
    ):
        return EmployeeRepository.search(
            db,
            name,
            is_active
        )
