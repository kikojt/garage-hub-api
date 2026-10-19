from sqlalchemy.orm import Session

from app.models.repair_part import RepairPart
from app.schemas.repair_part import RepairPartCreate


class RepairPartRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(RepairPart).all()

    @staticmethod
    def get_by_id(db: Session, repair_part_id: int):
        return db.query(RepairPart).filter(RepairPart.id == repair_part_id).first()
    '''
    @staticmethod
    def create(db: Session, repair_part: RepairPartCreate, unit_price):
        db_repair_part = RepairPart(
            repair_order_id = repair_part.repair_order_id,
            part_id = repair_part.part_id,
            quantity = repair_part.quantity,
            unit_price = unit_price
        )

        db.add(db_repair_part)
        db.commit()
        db.refresh(db_repair_part)

        return db_repair_part
    '''

    @staticmethod
    def create(db: Session, repair_order_id: int, part_id: int, quantity: int, unit_price
    ):
        db_repair_part = RepairPart(
            repair_order_id = repair_order_id,
            part_id = part_id,
            quantity = quantity,
            unit_price = unit_price
        )

        db.add(db_repair_part)
        db.commit()
        db.refresh(db_repair_part)

        return db_repair_part

    @staticmethod
    def update(db: Session, repair_part: RepairPart, quantity: int):
        repair_part.quantity = quantity

        db.commit()
        db.refresh(repair_part)

        return repair_part

    @staticmethod
    def delete(db: Session, db_repair_part: RepairPart):
        db.delete(db_repair_part)
        db.commit()


    @staticmethod
    def get_by_repair_order_and_part(db: Session, repair_order_id: int, part_id: int):
        return db.query(RepairPart).filter(RepairPart.repair_order_id == repair_order_id, RepairPart.part_id == part_id).first()

    
    @staticmethod
    def get_by_repair_order(
        db: Session,
        repair_order_id: int
    ):
        return (
            db.query(RepairPart)
            .filter(
                RepairPart.repair_order_id == repair_order_id
            )
            .all()
        )