from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.repositories.role import RoleRepository
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate

class UserService:

    @staticmethod
    def get_all_users(db: Session):
        return UserRepository.get_all(db)

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return UserRepository.get_by_id(db, user_id)
    
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        existing_username = UserRepository.get_by_username(db, user.username)

        if existing_username:
            raise ValueError("Username already exists.")
        
        existing_email = UserRepository.get_by_email(db, user.email)

        if existing_email:
            raise ValueError("Email already exists.")
        
        existing_role = RoleRepository.get_by_id(db, user.role_id)

        if existing_role is None:
            raise ValueError("Role not found.")
        
        password_hash = hash_password(user.password)

        return UserRepository.create(db, user, password_hash)
