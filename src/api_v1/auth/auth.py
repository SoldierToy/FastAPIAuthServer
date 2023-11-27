from collections import namedtuple

from fastapi import APIRouter, Depends, Response

from src.depends.users_authorization_depends import check_user_auth
from src.schemas.users_schemas import CreateUserSchema, AuthUserSchema, UserAuthTokenSchema
from src.depends.users_service_depends import users_service_depends

router = APIRouter(tags=["auth"])


@router.post('/register')
async def register_user(
        user: CreateUserSchema, user_service=Depends(users_service_depends)):
    res = await user_service.add_user(user)
    return {'uuid': res}


@router.post('/authenticated')
async def authenticated(response: Response, user: AuthUserSchema, user_service=Depends(users_service_depends)):
    tokens: namedtuple = await user_service.authenticated_user(user)
    response.set_cookie('refresh_token', tokens.refresh_token, httponly=True)
    return {'access_token': tokens.access_token}


@router.post('/update_access_token')
async def update_access_token():
    pass


@router.post('/private_endpoint')
async def private(user_token_date: UserAuthTokenSchema = Depends(check_user_auth)):
    print(user_token_date.email)
    return {'post': 'private_endpoint'}
