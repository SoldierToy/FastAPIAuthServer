from collections import namedtuple

from fastapi import APIRouter, Depends, Response
from schemas.users_schema import CreateUserSchema, RefreshTokenSchema, AuthUserSchema
from depends.users_service_depends import users_service_depends

router = APIRouter(tags=["auth"])


@router.post('/register')
async def register_user(
        user: CreateUserSchema, user_service=Depends(users_service_depends)):
    res = await user_service.add_user(user)
    return {'uuid': res}


@router.post('/authenticated')
async def authenticated(response: Response, user: AuthUserSchema, user_service=Depends(users_service_depends)):
    tokens: namedtuple = await user_service.authenticated(user)
    response.set_cookie('auth_token', tokens.refresh_token, httponly=True)
    return {'access_token': tokens.access_token}


@router.post('/update_access_token')
async def update_access_token():
    pass
