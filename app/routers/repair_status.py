from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.repair_status import (
    RepairStatusCreate,
    RepairStatusUpdate,
    RepairStatusResponse
)
from app.services.repair_status import RepairStatusService

router = APIRouter(
    prefix="/repair-status",
    tags=["Repair Status"]
)

@router.get("/", response_model=list[RepairStatusResponse])
def get_all_repair_statuses(db: Session = Depends(get_db)):
    return RepairStatusService.get_all_repair_statuses(db)

@router.get("/{repair_status_id}", response_model=RepairStatusResponse)
def get_repair_status(repair_status_id: int, db: Session = Depends(get_db)):
    repair_status = RepairStatusService.get_repair_status_by_id(db, repair_status_id)

    if repair_status is None:
        raise HTTPException(
            status_code=404,
            detail="Repair status not found."
        )

    return repair_status

@router.post("/", response_model=RepairStatusResponse)
def create_repair_status(repair_status: RepairStatusCreate, db: Session = Depends(get_db)):
    try:
        return RepairStatusService.create_repair_status(db, repair_status)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.delete("/{repair_status_id}")
def delete_repair_status(repair_status_id: int, db: Session = Depends(get_db)):
    deleted = RepairStatusService.delete_repair_status(db, repair_status_id)

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Repair status not found."
        )

    return {
        "message": "Repair status deleted successfully."
    }
