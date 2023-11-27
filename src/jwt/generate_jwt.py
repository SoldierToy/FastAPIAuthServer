from datetime import datetime
from datetime import timedelta
from random import randint
from jose import jwt
import settings


class TokenCreator:
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()

        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) + timedelta(
            seconds=randint(1, 10000))

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict):
        to_encode = data.copy()

        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS) + timedelta(
            seconds=randint(1, 10000))

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        return encoded_jwt

    @staticmethod
    def decode_tokens(token):
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
