from datetime import datetime
from collections import namedtuple
import jose
from src.jwt.generate_jwt import TokenCreator
from fastapi import Header, HTTPException, Cookie
from src.schemas.users_schemas import UserAuthTokenSchema, UserAuthRefreshTokenSchema

token_exception = HTTPException(status_code=401, detail='invalid token')

RefreshTokenData = namedtuple('RefreshTokenData', ['token_data', 'refresh_token'])


class TokenValidate:
    """Валидация токена. Парсинг и проверка expires"""

    @staticmethod
    def parse_jwt(token, parser=TokenCreator.decode_tokens):
        return parser(token)

    @staticmethod
    def check_expire_token(token_expire):
        time_now = int(datetime.utcnow().timestamp())

        if time_now > token_expire:
            raise token_exception


class CheckUserToken:

    def __call__(self, token=Header(alias='x-authorization', default=None)):
        if token is None:
            raise token_exception
        try:
            user_token_data = UserAuthTokenSchema(**TokenValidate.parse_jwt(token))
            TokenValidate.check_expire_token(user_token_data.exp)
        except jose.exceptions.JWTError:
            raise token_exception
        return user_token_data


check_user_jwt = CheckUserToken()


class RefreshTokenValidate:
    def __call__(self, refresh_token=Cookie(alias='refresh_token', default=None)):
        if refresh_token is None:
            raise token_exception
        try:
            token_dict = TokenValidate.parse_jwt(refresh_token)
            token_dict['token'] = refresh_token

            token_data = UserAuthRefreshTokenSchema(**token_dict)
            TokenValidate.check_expire_token(token_data.exp)
        except jose.exceptions.JWTError:
            raise token_exception

        return token_data


check_user_refresh_token = RefreshTokenValidate()
