from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.supplier import SupplierCreate, SupplierUpdate, SupplierResponse
from app.services.supplier import SupplierService

router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"]
)

@router.get("/", response_model=list[SupplierResponse])
def get_all_suppliers(db: Session = Depends(get_db)):
    return SupplierService.get_all_suppliers(db)

@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = SupplierService.get_supplier_by_id(db, supplier_id)

    if supplier is None:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found."
        )

    return supplier

@router.post("/", response_model=SupplierResponse)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    try:
        return SupplierService.create_supplier(db, supplier)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.delete("/{supplier_id}")
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    delete_supplier = SupplierService.delete_supplier(db, supplier_id)

    if delete_supplier is None:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found."
        )

    return {
        "message": "Supplier deleted successfully."
    }