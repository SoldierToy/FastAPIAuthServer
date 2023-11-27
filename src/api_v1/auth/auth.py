from collections import namedtuple

from fastapi import APIRouter, Depends, Response, Request, Cookie

from src.depends.users_authorization_depends import check_user_jwt, check_user_refresh_token
from src.schemas.users_schemas import CreateUserSchema, AuthUserSchema, UserAuthTokenSchema, UpdateUserSchema, \
    UserAuthRefreshTokenSchema
from src.depends.users_service_depends import users_service_depends

router = APIRouter(tags=["auth"])


@router.post('/register')
async def register_user(
        user: CreateUserSchema,
        user_service=Depends(users_service_depends)
):
    res = await user_service.add_user(user)
    return {'uuid': res}


@router.post('/authenticated')
async def authenticated(
        response: Response,
        user: AuthUserSchema,
        user_service=Depends(users_service_depends)
):
    tokens: namedtuple = await user_service.authenticated_user(user)
    response.set_cookie('refresh_token', tokens.refresh_token, httponly=True)
    return {'access_token': tokens.access_token}


@router.post('/update_access_token')
async def update_access_token(
        response: Response,
        refresh_token: UserAuthRefreshTokenSchema = Depends(check_user_refresh_token),
        user_service=Depends(users_service_depends)
):
    tokens = await user_service.tokens_replacement(refresh_token)
    response.delete_cookie('refresh_token')
    response.set_cookie('refresh_token', tokens.refresh_token, httponly=True)
    return {'access_token': tokens.access_token}

@router.post('/update_user_data')
async def update_user_date(
        update_edit_data: UpdateUserSchema,
        current_user_token_data: UserAuthTokenSchema = Depends(check_user_jwt),
        user_service=Depends(users_service_depends)
):
    await user_service.update_user(current_user_data=current_user_token_data, user_edit_data=update_edit_data)
