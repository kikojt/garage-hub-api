from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.repair_order import RepairOrderResponse
from app.services.repair_workflow import RepairWorkflowService
from app.schemas.repair_part import RepairPartResponse
from app.schemas.repair_workflow import ChangeStatusRequest, AssignEmployeeRequest, AddPartRequest, UpdatePartQuantityRequest

router = APIRouter(
    prefix="/repair-workflow",
    tags=["Repair Workflow"]
)

@router.patch("/repair-orders/{repair_order_id}/status", response_model=RepairOrderResponse)
def change_repair_order_status(
    repair_order_id: int,
    payload: ChangeStatusRequest,
    db: Session = Depends(get_db)
):
    try:
        return RepairWorkflowService.change_status(
            db,
            repair_order_id,
            payload.repair_status_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.patch(
    "/repair-orders/{repair_order_id}/assign-employee",
    response_model=RepairOrderResponse
)
def assign_employee(
    repair_order_id: int,
    request: AssignEmployeeRequest,
    db: Session = Depends(get_db)
):
    try:
        return RepairWorkflowService.assign_employee(
            db,
            repair_order_id,
            request.employee_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
        
@router.post("/repair-orders/{repair_order_id}/parts",
    response_model=RepairPartResponse
)
def add_part(
    repair_order_id: int,
    request: AddPartRequest,
    db: Session = Depends(get_db)
):
    try:
        return RepairWorkflowService.add_part(
            db,
            repair_order_id,
            request.part_id,
            request.quantity
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
        
@router.patch("/repair-orders/{repair_order_id}/parts/{part_id}",
    response_model=RepairPartResponse
)
def update_part_quantity(
    repair_order_id: int,
    part_id: int,
    request: UpdatePartQuantityRequest,
    db: Session = Depends(get_db)
):
    try:
        return RepairWorkflowService.update_part_quantity(
            db,
            repair_order_id,
            part_id,
            request.quantity
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
        
@router.delete("/repair-orders/{repair_order_id}/parts/{part_id}")
def remove_part(
    repair_order_id: int,
    part_id: int,
    db: Session = Depends(get_db)
):
    try:
        RepairWorkflowService.remove_part(
            db,
            repair_order_id,
            part_id
        )

        return {
            "message": "Part removed successfully."
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
        
@router.patch(
    "/repair-orders/{repair_order_id}/complete",
    response_model=RepairOrderResponse
)
def complete_repair(
    repair_order_id: int,
    db: Session = Depends(get_db)
):
    try:
        return RepairWorkflowService.complete_repair(
            db,
            repair_order_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
@router.patch(
    "/repair-orders/{repair_order_id}/cancel",
    response_model=RepairOrderResponse
)
def cancel_repair(
    repair_order_id: int,
    db: Session = Depends(get_db)
):
    try:
        return RepairWorkflowService.cancel_repair(
            db,
            repair_order_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )