from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.services.employee import EmployeeService

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)

@router.get("/", response_model=list[EmployeeResponse])
def get_all_employees(db: Session = Depends(get_db)):
    return EmployeeService.get_all_employees(db)

@router.get("/search", response_model=list[EmployeeResponse])
def search_employees(
    name: str | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db)
):
    return EmployeeService.search_employees(
        db,
        name,
        is_active
    )

@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = EmployeeService.get_employee_by_id(db, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found."
        )
    
    return employee

@router.post("/", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    try:
        return EmployeeService.create_employee(db, employee)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    deleted = EmployeeService.delete_employee(db, employee_id)

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found."
        )

    return {
        "message": "Employee deleted successfully."
    }