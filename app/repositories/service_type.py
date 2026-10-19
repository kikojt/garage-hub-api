from sqlalchemy.orm import Session

from app.models.service_type import ServiceType
from app.schemas.service_type import ServiceTypeCreate, ServiceTypeUpdate

class ServiceTypeRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(ServiceType).all()
    
    @staticmethod
    def get_by_id(db: Session, service_type_id: int):
        return db.query(ServiceType).filter(ServiceType.id == service_type_id).first()
    
    @staticmethod
    def get_by_name(db: Session, service_type_name: str):
        return db.query(ServiceType).filter(ServiceType.name == service_type_name).first()
    
    @staticmethod
    def create(db: Session, service_type: ServiceTypeCreate):
        db_service_type = ServiceType(
            name = service_type.name, 
            description = service_type.description
        )

        db.add(db_service_type)
        db.commit()
        db.refresh(db_service_type)

        return db_service_type
    
    @staticmethod
    def delete(db: Session, db_service_type: ServiceType):
        db.delete(db_service_type)
        db.commit()