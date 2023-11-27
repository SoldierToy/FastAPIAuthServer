from pydantic import BaseModel, UUID4
from pydantic import EmailStr, Field


class CreateUserSchema(BaseModel):
    tg_id: int = Field(gt=1)
    name: str = Field(max_length=32)
    password: str = Field(max_length=64)
    email: EmailStr


class UpdateUserSchema(BaseModel):
    id: str
    tg_id: int | None = Field(gt=1, default=None)
    name: str | None = Field(max_length=32, default=None)
    password: str | None = Field(max_length=64, default=None)
    email: EmailStr | None = Field(default=None)
    role: str = Field(default=None)


class AuthUserSchema(BaseModel):
    email: EmailStr
    password: str


class UserAuthTokenSchema(BaseModel):
    id: str
    name: str = Field(default=None)
    email: str = Field(default=None)
    role: str = Field(default=None)
    exp: int = Field(default=None)


class UserAuthRefreshTokenSchema(UserAuthTokenSchema):
    token: str
