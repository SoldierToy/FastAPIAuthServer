from uuid import UUID, uuid4

from pydantic import BaseModel
from pydantic import UUID4, EmailStr, Field


class CreateUserSchema(BaseModel):
    tg_id: int = Field(gt=1)
    name: str = Field(max_length=32)
    password: str = Field(max_length=64)
    email: EmailStr


class AuthUserSchema(BaseModel):
    email: EmailStr
    password: str
