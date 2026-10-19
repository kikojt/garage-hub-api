from sqlalchemy.orm import Session

from app.models.repair_status import RepairStatus
from app.schemas.repair_status import RepairStatusCreate, RepairStatusUpdate

class RepairStatusRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(RepairStatus).all()

    @staticmethod
    def get_by_id(db: Session, repair_status_id: int):
        return db.query(RepairStatus).filter(RepairStatus.id == repair_status_id).first()

    @staticmethod
    def get_by_name(db: Session, name: str):
        return db.query(RepairStatus).filter(RepairStatus.name == name).first()

    @staticmethod
    def create(db: Session, repair_status: RepairStatusCreate):
        db_repair_status = RepairStatus(
            name = repair_status.name,
            description = repair_status.description
        )
        
        db.add(db_repair_status)
        db.commit()
        db.refresh(db_repair_status)

        return db_repair_status

    @staticmethod
    def delete(db: Session, db_repair_status: RepairStatus):
        db.delete(db_repair_status)
        db.commit()

