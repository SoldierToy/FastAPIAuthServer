from enum import Enum
from typing import Type, Union

import sqlalchemy
from fastapi import HTTPException

from src.jwt.generate_jwt import TokenCreator
from src.repositories.users_repo import UsersRepo
from src.schemas.users_schemas import CreateUserSchema, AuthUserSchema, UpdateUserSchema, UserAuthTokenSchema
from src.utils.hashing import Hasher
from collections import namedtuple

Tokens = namedtuple('Tokens', ['access_token', 'refresh_token'])


class UserRoles(str, Enum):
    ROLE_USER = "USER"
    ROLE_ADMIN = "ADMIN"
    ROLE_SUPERADMIN = "SUPERADMIN"


class UsersService:
    def __init__(self, repo: Type[UsersRepo]):
        self.repo: UsersRepo = repo()

    async def add_user(self, user: CreateUserSchema, user_role=UserRoles.ROLE_USER):
        """Занесение нового юзера в БД"""
        try:
            user_data = user.model_dump()
            user_data['role'] = user_role
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

    async def authenticated_user(self, data: AuthUserSchema):
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
                'id': str(user_data.id),
                'role': user_data.role
            }

            Tokens.access_token = TokenCreator.create_access_token(user_data_to_jwt)
            Tokens.refresh_token = TokenCreator.create_refresh_token(user_data_to_jwt)

            await self.repo.add_refresh_token_for_user(user_data.id, Tokens.refresh_token)

            return Tokens
        else:
            raise HTTPException(status_code=400, detail="Incorrect password or email")

    @staticmethod
    def self_editing(id_current_user: str, id_user_edit: str) -> bool:
        if id_user_edit == id_current_user:
            return True

    async def check_roles(self, role_current_user, id_user_edit) -> bool:
        user = await self.repo.get_one_from_id(user_id=id_user_edit)
        user_edit_role = user.role

        if role_current_user == UserRoles.ROLE_SUPERADMIN and user_edit_role in (
                UserRoles.ROLE_ADMIN, UserRoles.ROLE_USER):
            return True
        elif role_current_user == UserRoles.ROLE_ADMIN and user_edit_role in (UserRoles.ROLE_USER):
            return True

    async def update_user(self, current_user_data: UserAuthTokenSchema, user_edit_data: UpdateUserSchema):
        edit_data_dict = user_edit_data.model_dump(exclude_none=True)
        if UsersService.self_editing(id_current_user=current_user_data.id, id_user_edit=user_edit_data.id):
            await self.repo.update_user_data(edit_data_dict)
        elif await self.check_roles(current_user_data.role, user_edit_data.id):
            await self.repo.update_user_data(edit_data_dict)
        else:
            raise HTTPException(status_code=403)
