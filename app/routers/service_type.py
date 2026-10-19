from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.service_type import ServiceTypeCreate, ServiceTypeUpdate, ServiceTypeResponse
from app.services.service_type import ServiceTypeService

router = APIRouter(
    prefix="/service-types",
    tags=["Service Types"]
)

@router.get("/", response_model=list[ServiceTypeResponse])
def get_all_service_types(db: Session = Depends(get_db)):
    return ServiceTypeService.get_all_service_types(db)

@router.get("/{service_type_id}", response_model=ServiceTypeResponse)
def get_service_type(service_type_id: int, db: Session = Depends(get_db)):
    service_type = ServiceTypeService.get_service_type_by_id(db, service_type_id)

    if service_type is None:
        raise HTTPException(
            status_code=404,
            detail="Service type not found."
        )

    return service_type

@router.post("/", response_model=ServiceTypeResponse)
def create_service_type(service_type: ServiceTypeCreate, db: Session = Depends(get_db)):
    try:
        return ServiceTypeService.create_service_type(db, service_type)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.delete("/{service_type_id}")
def delete_service_type(service_type_id: int, db: Session = Depends(get_db)):
    deleted = ServiceTypeService.delete_service_type(db, service_type_id)

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Service type not found."
        )

    return {
        "message": "Service type deleted successfully."
    }
