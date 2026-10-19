from sqlalchemy.orm import Session

from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate


class RoleRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Role).all()

    @staticmethod
    def get_by_id(db: Session, role_id: int):
        return db.query(Role).filter(Role.id == role_id).first()

    @staticmethod
    def create(db: Session, role: RoleCreate):
        db_role = Role(
            name = role.name,
            description = role.description
        )

        db.add(db_role)
        db.commit()
        db.refresh(db_role)

        return db_role

    @staticmethod
    def update(db: Session, db_role: Role, role: RoleUpdate):
        db_role.name = role.name
        db_role.description = role.description

        db.commit()
        db.refresh(db_role)

        return db_role

    @staticmethod
    def delete(db: Session, db_role: Role):
        db.delete(db_role)
        db.commit()
