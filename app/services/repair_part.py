from sqlalchemy.orm import Session

from app.repositories.part import PartRepository
#from app.repositories.repair_order import RepairOrderRepository
from app.repositories.repair_part import RepairPartRepository
from app.schemas.repair_part import RepairPartCreate


class RepairPartService:

    @staticmethod
    def get_all_repair_parts(db: Session):
        return RepairPartRepository.get_all(db)

    @staticmethod
    def get_repair_part_by_id(db: Session, repair_part_id: int):
        return RepairPartRepository.get_by_id(db, repair_part_id)

    @staticmethod
    def create_repair_part(db: Session, repair_part: RepairPartCreate):

        #existing_repair_order = RepairOrderRepository.get_by_id(
        #    db,
        #    repair_part.repair_order_id
        #)

        #if existing_repair_order is None:
            #raise ValueError("Repair order not found.")

        existing_part = PartRepository.get_by_id(db, repair_part.part_id)

        if existing_part is None:
            raise ValueError("Part not found.")

        #existing_repair_part = RepairPartRepository.get_by_repair_order_and_part(
        #    db,
        #    repair_part.repair_order_id,
        #    repair_part.part_id
        #)

        #if existing_repair_part:
        #    raise ValueError(
        #        "This part is already assigned to this repair order."
        #    )

        return RepairPartRepository.create(
            db,
            repair_part,
            existing_part.unit_price
        )

    @staticmethod
    def delete_repair_part(db: Session, repair_part_id: int):

        db_repair_part = RepairPartRepository.get_by_id(
            db,
            repair_part_id
        )

        if db_repair_part is None:
            return None

        RepairPartRepository.delete(db, db_repair_part)

        return True