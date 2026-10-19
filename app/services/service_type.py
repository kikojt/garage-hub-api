from sqlalchemy.orm import Session

from app.repositories.service_type import ServiceTypeRepository
from app.schemas.service_type import ServiceTypeCreate, ServiceTypeUpdate

class ServiceTypeService:

    @staticmethod
    def get_all_service_types(db: Session):
        return ServiceTypeRepository.get_all(db)
    
    @staticmethod
    def get_service_type_by_id(db: Session, service_type_id: int):
        return ServiceTypeRepository.get_by_id(db, service_type_id)

    @staticmethod
    def create_service_type(db: Session, service_type: ServiceTypeCreate):
        existing_service_type = ServiceTypeRepository.get_by_name(db, service_type.name)

        if existing_service_type:
            raise ValueError(
                "Service type already exists."
            )

        return ServiceTypeRepository.create(db, service_type)
    
    @staticmethod
    def delete_service_type(db: Session, service_type_id: int):
        db_service_type = ServiceTypeRepository.get_by_id(db, service_type_id)

        if db_service_type is None:
            return None

        ServiceTypeRepository.delete(db, db_service_type)

        return True
    

    
