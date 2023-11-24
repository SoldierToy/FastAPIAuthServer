from typing import Type

import sqlalchemy
from fastapi import HTTPException

from jwt.generate_jwt import TokenCreator
from repositories.users_repo import UsersRepo
from schemas.users_schema import CreateUserSchema, AuthUserSchema
from utils.hashing import Hasher
from collections import namedtuple

Tokens = namedtuple('Tokens', ['access_token', 'refresh_token'])


class UsersService:
    def __init__(self, repo: Type[UsersRepo]):
        self.repo: UsersRepo = repo()

    async def add_user(self, user: CreateUserSchema):
        """Занесение нового юзера в БД"""
        try:
            user_data = user.model_dump()
            user_pass = user_data.pop('password')
            user_data['hashed_password'] = Hasher.hashing_password(user_pass)
            user_id = await self.repo.add_one(user_data)

            return user_id

        except sqlalchemy.exc.IntegrityError as err:
            if 'duplicate key value violates unique constraint "users_email_key"' in str(err):
                raise HTTPException(status_code=400, detail="Email already registered")
            elif 'duplicate key value violates unique constraint "users_tg_id_key"' in str(err):
                raise HTTPException(status_code=400, detail="tg_id already registered")

    async def check_user_for_email(self, user: CreateUserSchema):
        """"Проверка наличия юзера в БД по Email"""
        user_email = user.email
        res = await self.repo.get_one_from_email(user_email)
        return res

    async def check_user_for_tg_id(self, user: CreateUserSchema):
        """"Проверка наличия юзера в БД по tg_id"""
        user_email = user.email
        res = await self.repo.get_one_from_email(user_email)
        return res

    async def authenticated(self, data: AuthUserSchema):
        user_email = data.email

        try:
            user_data = await self.repo.get_email_and_pass(user_email)
        except sqlalchemy.exc.NoResultFound:
            raise HTTPException(status_code=400, detail="Incorrect password or email")

        user_password = data.password
        hashed_user_password = user_data.hashed_password

        if Hasher.verify_password(user_password, hashed_user_password):
            user_data_to_jwt = {
                'name': user_data.name,
                'email': user_data.email,
                'uuid': str(user_data.id),
                'role': user_data.role
            }

            Tokens.access_token = TokenCreator.create_access_token(user_data_to_jwt)
            Tokens.refresh_token = TokenCreator.create_refresh_token(user_data_to_jwt)

            await self.repo.add_refresh_token_for_user(user_data.id, Tokens.refresh_token)

            return Tokens
        else:
            raise HTTPException(status_code=400, detail="Incorrect password or email")
