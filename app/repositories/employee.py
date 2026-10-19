from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.user import User
from app.schemas.employee import EmployeeCreate, EmployeeUpdate

class EmployeeRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Employee).all()
    
    @staticmethod
    def get_by_id(db: Session, employee_id: int):
        return db.query(Employee).filter(Employee.id == employee_id).first()
    
    @staticmethod
    def get_by_user_id(db: Session, user_id: int):
        return db.query(Employee).filter(Employee.user_id == user_id).first()
    
    @staticmethod
    def create(db: Session, employee: EmployeeCreate):
        db_employee = Employee(
            user_id = employee.user_id,
            first_name = employee.first_name,
            last_name = employee.last_name,
            phone = employee.phone,
            hire_date = employee.hire_date,
        )

        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)

        return db_employee
    
    @staticmethod
    def delete(db: Session, db_employee: Employee):
        db.delete(db_employee)
        db.commit()

    
    @staticmethod
    def is_active(employee: Employee) -> bool:
        return employee.user.is_active


    @staticmethod
    def search(
        db: Session,
        name: str | None = None,
        is_active: bool | None = None
    ):

        query = db.query(Employee).join(User)

        if name:
            query = query.filter(
                (
                    Employee.first_name.ilike(f"%{name}%")
                )
                |
                (
                    Employee.last_name.ilike(f"%{name}%")
                )
            )

        if is_active is not None:
            query = query.filter(
                User.is_active == is_active
            )

        return query.all()
