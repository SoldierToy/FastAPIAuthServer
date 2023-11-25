from pydantic import BaseModel, UUID4


class RefreshTokenSchema(BaseModel):
    refresh_token: str
    user_fk: UUID4


class Token(BaseModel):
    access_token: str
    token_type: str
