from sqlalchemy.orm import Session

from app.repositories.repair_status import RepairStatusRepository
from app.schemas.repair_status import RepairStatusCreate, RepairStatusUpdate

class RepairStatusService:

    @staticmethod
    def get_all_repair_statuses(db: Session):
        return RepairStatusRepository.get_all(db)
    
    @staticmethod
    def get_repair_status_by_id(db: Session, repair_status_id: int):
        return RepairStatusRepository.get_by_id(db, repair_status_id)
    
    @staticmethod
    def get_repair_status_by_name(db: Session, repair_status_name: str):
        return RepairStatusRepository.get_by_name(db, repair_status_name)
    
    @staticmethod
    def create_repair_status(db: Session, repair_status: RepairStatusCreate):
        existing_status = RepairStatusRepository.get_by_name(db, repair_status.name)

        if existing_status:
            raise ValueError(
                "Repair status already exists."
            )

        return RepairStatusRepository.create(db, repair_status)


    @staticmethod
    def delete_repair_status(db: Session, repair_status_id: int):
        db_repair_status = RepairStatusRepository.get_by_id(db, repair_status_id)

        if db_repair_status is None:
            return None

        RepairStatusRepository.delete(db, db_repair_status)

        return True