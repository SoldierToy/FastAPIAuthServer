from services.users_service import UsersService
from repositories.users_repo import UsersRepo


def users_service_depends():
    return UsersService(UsersRepo)
