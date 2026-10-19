from sqlalchemy.orm import Session

from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate

class SupplierRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Supplier).all()
    
    @staticmethod
    def get_by_id(db: Session, supplier_id: int):
        return db.query(Supplier).filter(Supplier.id == supplier_id).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(Supplier).filter(Supplier.email == email).first()
    
    @staticmethod
    def create(db: Session, supplier: SupplierCreate):
        db_supplier = Supplier(
            company_name = supplier.company_name,
            contact_name = supplier.contact_name,
            phone = supplier.phone,
            email = supplier.email,
            address = supplier.address,
            postal_code = supplier.postal_code,
            city = supplier.city
        )

        db.add(db_supplier)
        db.commit()
        db.refresh(db_supplier)

        return db_supplier
    
    @staticmethod
    def update(db: Session, db_supplier: Supplier, supplier: SupplierUpdate):
        db_supplier.company_name = supplier.company_name
        db_supplier.contact_name = supplier.contact_name
        db_supplier.phone = supplier.phone
        db_supplier.email = supplier.email
        db_supplier.address = supplier.address
        db_supplier.postal_code = supplier.postal_code
        db_supplier.city = supplier.city

        db.commit()
        db.refresh(db_supplier)

        return db_supplier

    @staticmethod
    def delete(db: Session, db_supplier: Supplier):
        db.delete(db_supplier)
        db.commit()
