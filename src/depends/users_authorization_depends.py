from datetime import datetime

import jose
from src.jwt.generate_jwt import TokenCreator
from fastapi import Header, HTTPException
from src.schemas.users_schemas import UserAuthTokenSchema

token_exception = HTTPException(status_code=401, detail='invalid token')


class CheckUserAuth:

    @staticmethod
    def parse_jwt(token, parser=TokenCreator.decode_tokens):
        return parser(token)

    @staticmethod
    def check_expire_token(token_expire):
        time_now = int(datetime.utcnow().timestamp())

        if time_now > token_expire:
            raise token_exception

    def __call__(self, token=Header(alias='x-authorization', default=None)):
        if token is None:
            raise token_exception
        try:
            print(CheckUserAuth.parse_jwt(token))
            user_token_date = UserAuthTokenSchema(**CheckUserAuth.parse_jwt(token))
            CheckUserAuth.check_expire_token(user_token_date.exp)
        except jose.exceptions.JWTError:
            raise token_exception
        return user_token_date


check_user_auth = CheckUserAuth()
