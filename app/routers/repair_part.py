from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.repair_part import RepairPartCreate, RepairPartResponse
from app.services.repair_part import RepairPartService

router = APIRouter(
    prefix="/repair-parts",
    tags=["Repair Parts"]
)

@router.get("/", response_model=list[RepairPartResponse])
def get_all_repair_parts(db: Session = Depends(get_db)):
    return RepairPartService.get_all_repair_parts(db)

@router.get("/{repair_part_id}", response_model=RepairPartResponse)
def get_repair_part(repair_part_id: int, db: Session = Depends(get_db)):
    repair_part = RepairPartService.get_repair_part_by_id(
        db,
        repair_part_id
    )

    if repair_part is None:
        raise HTTPException(
            status_code=404,
            detail="Repair part not found."
        )

    return repair_part

@router.post("/", response_model=RepairPartResponse)
def create_repair_part(
    repair_part: RepairPartCreate,
    db: Session = Depends(get_db)
):
    try:
        return RepairPartService.create_repair_part(
            db,
            repair_part
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.delete("/{repair_part_id}")
def delete_repair_part(
    repair_part_id: int,
    db: Session = Depends(get_db)
):
    deleted = RepairPartService.delete_repair_part(
        db,
        repair_part_id
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Repair part not found."
        )

    return {
        "message": "Repair part deleted successfully."
    }
