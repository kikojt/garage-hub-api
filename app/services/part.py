from sqlalchemy.orm import Session

from app.repositories.part import PartRepository
from app.repositories.supplier import SupplierRepository
from app.schemas.part import PartCreate


class PartService:

    @staticmethod
    def get_all_parts(db: Session):
        return PartRepository.get_all(db)

    @staticmethod
    def get_part_by_id(db: Session, part_id: int):
        return PartRepository.get_by_id(db, part_id)

    @staticmethod
    def create_part(db: Session, part: PartCreate):

        existing_supplier = SupplierRepository.get_by_id(db, part.supplier_id)

        if existing_supplier is None:
            raise ValueError("Supplier not found.")

        existing_part = PartRepository.get_by_part_number(db, part.part_number)

        if existing_part:
            raise ValueError("Part number already exists.")

        return PartRepository.create(db, part)

    @staticmethod
    def delete_part(db: Session, part_id: int):
        db_part = PartRepository.get_by_id(db, part_id)

        if db_part is None:
            return None

        PartRepository.delete(db, db_part)

        return True

    @staticmethod
    def search_parts(
        db: Session,
        name: str | None = None,
        part_number: str | None = None,
        low_stock: bool | None = None
    ):
        return PartRepository.search(
            db,
            name,
            part_number,
            low_stock
        )