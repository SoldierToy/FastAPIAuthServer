import asyncio
from asyncio import run

from settings import settings
from src.depends.users_service_depends import users_service_depends
from src.repositories.users_repo import UsersRepo
from src.schemas.users_schemas import CreateUserSchema
from src.services.users_service import UsersService, UserRoles


async def create_super_user():
    name = settings.superuser_name
    password = settings.superuser_password
    email = settings.superuser_email
    tg_id = settings.superuser_tg_id

    user_date = CreateUserSchema(
        name=name,
        password=password,
        email=email,
        tg_id=tg_id)

    await UsersService(UsersRepo).add_user(user_date, user_role=UserRoles.ROLE_SUPERADMIN)


print()
print('SUPERADMIN CREATED')


async def main():
    await create_super_user()


asyncio.run(main())
