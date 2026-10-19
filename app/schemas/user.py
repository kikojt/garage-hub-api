from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role_id: int
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(
        min_length=8,
        max_length=128
    )


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    role_id: int | None = None
    is_active: bool | None = None
    password: str | None = None


class UserResponse(UserBase):
    id: int
    last_login: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)