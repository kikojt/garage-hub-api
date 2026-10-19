from sqlalchemy.orm import Session

from app.models.part import Part
from app.schemas.part import PartCreate


class PartRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Part).all()

    @staticmethod
    def get_by_id(db: Session, part_id: int):
        return db.query(Part).filter(Part.id == part_id).first()

    @staticmethod
    def get_by_part_number(db: Session, part_number: str):
        return db.query(Part).filter(Part.part_number == part_number).first()

    @staticmethod
    def create(db: Session, part: PartCreate):
        db_part = Part(
            supplier_id = part.supplier_id,
            name = part.name,
            part_number = part.part_number,
            stock_quantity = part.stock_quantity,
            unit_price = part.unit_price
        )

        db.add(db_part)
        db.commit()
        db.refresh(db_part)

        return db_part

    @staticmethod
    def delete(db: Session, db_part: Part):
        db.delete(db_part)
        db.commit()


    @staticmethod
    def decrease_stock(db: Session, part: Part, quantity: int):
        part.stock_quantity -= quantity

        db.commit()
        db.refresh(part)

        return part

    @staticmethod
    def increase_stock(db: Session, part: Part, quantity: int):
            part.stock_quantity += quantity
    
            db.commit()
            db.refresh(part)
    
            return part

    @staticmethod
    def search(
        db: Session,
        name: str | None = None,
        part_number: str | None = None,
        low_stock: bool | None = None
    ):

        query = db.query(Part)

        if name:
            query = query.filter(
                Part.name.ilike(f"%{name}%")
            )

        if part_number:
            query = query.filter(
                Part.part_number.ilike(f"%{part_number}%")
            )

        if low_stock is True:
            query = query.filter(
                Part.stock_quantity <= 5
            )

        return query.all()
    
