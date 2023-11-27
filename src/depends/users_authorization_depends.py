import jose
from src.jwt.generate_jwt import TokenCreator
from fastapi import Header, HTTPException
from src.schemas.users_schemas import UserAuthTokenSchema


class CheckUserAuth:

    @staticmethod
    def parse_jwt(token, parser=TokenCreator.decode_tokens):
        return parser(token)

    def __call__(self, token=Header(alias='x-authorization', default=None)):
        if token is None:
            raise HTTPException(status_code=401, detail='invalid token')
        try:
            user_token_date = UserAuthTokenSchema(**CheckUserAuth.parse_jwt(token))
        except jose.exceptions.JWTError:
            raise HTTPException(status_code=401, detail='invalid token')
        return user_token_date


check_user_auth = CheckUserAuth()
