from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.repair_order import RepairOrderCreate, RepairOrderResponse
from app.services.repair_order import RepairOrderService

router = APIRouter(
    prefix="/repair-orders",
    tags=["Repair Orders"]
)

@router.get("/", response_model=list[RepairOrderResponse])
def get_all_repair_orders(db: Session = Depends(get_db)):
    return RepairOrderService.get_all_repair_orders(db)

@router.get("/search", response_model=list[RepairOrderResponse])
def search(
    db: Session = Depends(get_db),
    registration_plate: str | None = None,
    customer_id: int | None = None,
    status_id: int | None = None,
    employee_id: int | None = None,
    start_date: date | None = None,
    end_date: date | None = None
):
    return RepairOrderService.search(
        db=db,
        registration_plate=registration_plate,
        customer_id=customer_id,
        status_id=status_id,
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date
    )

@router.get("/{repair_order_id}", response_model=RepairOrderResponse)
def get_repair_order(repair_order_id: int, db: Session = Depends(get_db)):
    repair_order = RepairOrderService.get_repair_order_by_id(
        db,
        repair_order_id
    )

    if repair_order is None:
        raise HTTPException(
            status_code=404,
            detail="Repair order not found."
        )

    return repair_order

@router.post("/", response_model=RepairOrderResponse)
def create_repair_order(
    repair_order: RepairOrderCreate,
    db: Session = Depends(get_db)
):
    try:
        return RepairOrderService.create_repair_order(
            db,
            repair_order
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.delete("/{repair_order_id}")
def delete_repair_order(
    repair_order_id: int,
    db: Session = Depends(get_db)
):
    deleted = RepairOrderService.delete_repair_order(
        db,
        repair_order_id
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Repair order not found."
        )

    return {
        "message": "Repair order deleted successfully."
    }


