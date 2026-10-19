from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class UserRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(User).all()
    
    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first() 
    
    @staticmethod
    def get_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def create(db: Session, user: UserCreate, password: str):
        db_user = User(
            username = user.username,
            email = user.email,
            password = password,
            role_id = user.role_id,
            is_active = user.is_active
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user
    
    @staticmethod
    def delete(db: Session, db_user: User):
        db.delete(db_user)
        db.commit()

    @staticmethod
    def get_by_username(
        db: Session,
        username: str
    ):
        return (
            db.query(User)
            .filter(User.username == username)
            .first()
        )
