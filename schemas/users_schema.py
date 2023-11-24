from uuid import UUID, uuid4

from pydantic import BaseModel
from pydantic import UUID4, EmailStr, Field


class CreateUserSchema(BaseModel):
    tg_id: int = Field(gt=1)
    name: str = Field(max_length=32)
    password: str = Field(max_length=64)
    email: EmailStr
    role: int = Field(gt=0, lt=4, default=0)


class AuthUserSchema(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str
    user_fk: UUID4


class Token(BaseModel):
    access_token: str
    token_type: str
