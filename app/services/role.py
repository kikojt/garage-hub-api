from sqlalchemy.orm import Session

from app.repositories.role import RoleRepository
from app.schemas.role import RoleCreate, RoleUpdate


class RoleService:

    @staticmethod
    def get_all_roles(db: Session):
        return RoleRepository.get_all(db)

    @staticmethod
    def get_role_by_id(db: Session, role_id: int):
        return RoleRepository.get_by_id(db, role_id)

    @staticmethod
    def create_role(db: Session, role: RoleCreate):
        return RoleRepository.create(db, role)

    @staticmethod
    def update_role(db: Session, role_id: int, role: RoleUpdate):
        db_role = RoleRepository.get_by_id(db, role_id)
        
        if db_role is None:
            return None

        return RoleRepository.update(db, db_role, role)

    @staticmethod
    def delete_role(db: Session, role_id: int):
        db_role = RoleRepository.get_by_id(db, role_id)
        
        if db_role is None:
            return None

        RoleRepository.delete(db, db_role)

        return True