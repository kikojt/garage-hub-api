from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.part import PartCreate, PartResponse
from app.services.part import PartService

router = APIRouter(
    prefix="/parts",
    tags=["Parts"]
)


@router.get("/", response_model=list[PartResponse])
def get_all_parts(db: Session = Depends(get_db)):
    return PartService.get_all_parts(db)


@router.get("/search", response_model=list[PartResponse])
def search_parts(
    name: str | None = None,
    part_number: str | None = None,
    low_stock: bool | None = None,
    db: Session = Depends(get_db)
):

    return PartService.search_parts(
        db,
        name,
        part_number,
        low_stock
    )


@router.get("/{part_id}", response_model=PartResponse)
def get_part(part_id: int, db: Session = Depends(get_db)):
    part = PartService.get_part_by_id(db, part_id)

    if part is None:
        raise HTTPException(
            status_code=404,
            detail="Part not found."
        )

    return part


@router.post("/", response_model=PartResponse)
def create_part(part: PartCreate, db: Session = Depends(get_db)):
    try:
        return PartService.create_part(db, part)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.delete("/{part_id}")
def delete_part(part_id: int, db: Session = Depends(get_db)):
    deleted = PartService.delete_part(db, part_id)

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Part not found."
        )

    return {
        "message": "Part deleted successfully."
    }
