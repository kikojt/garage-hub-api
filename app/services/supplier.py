from sqlalchemy.orm import Session

from app.repositories.supplier import SupplierRepository
from app.schemas.supplier import SupplierCreate, SupplierUpdate

class SupplierService:

    @staticmethod
    def get_all_suppliers(db:Session):
        return SupplierRepository.get_all(db)
    
    @staticmethod
    def get_supplier_by_id(db: Session, supplier_id: int):
        return SupplierRepository.get_by_id(db, supplier_id)
    
    @staticmethod
    def create_supplier(db: Session, supplier: SupplierCreate):
        existing_email = SupplierRepository.get_by_email(db, supplier.email)

        if existing_email:
            raise ValueError("Email already exists.")
        
        return SupplierRepository.create(db, supplier)
    
    @staticmethod
    def delete_supplier(db: Session, supplier_id: int):
        db_supplier = SupplierRepository.get_by_id(db, supplier_id)

        if db_supplier is None:
            return None
        
        SupplierRepository.delete(db, db_supplier)

        return True
