from src.services.users_service import UsersService
from src.repositories.users_repo import UsersRepo


def users_service_depends():
    return UsersService(UsersRepo)
