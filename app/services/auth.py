from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.repositories.user import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse


class AuthService:

    @staticmethod
    def login(db: Session, credentials: LoginRequest):

        user = UserRepository.get_by_username(db, credentials.username)

        if user is None:
            raise ValueError("Invalid username or password.")

        if not verify_password(credentials.password, user.password):
            raise ValueError("Invalid username or password.")

        if not user.is_active:
            raise ValueError("User account is inactive.")

        access_token = create_access_token(
            {"sub": str(user.id), "role": user.role.name}
        )

        return TokenResponse(access_token=access_token, token_type="bearer")
