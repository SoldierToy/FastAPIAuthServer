from src.db.connection import async_session_factory
from src.models import Users, RefreshTokens
from sqlalchemy import insert, select, update, delete


class UsersRepo:
    model_user = Users
    model_refresh_tokens = RefreshTokens

    async def add_one(self, data: dict):
        async with async_session_factory() as session:
            stmt = insert(self.model_user).values(**data).returning(self.model_user.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def get_one_from_email(self, email: str):
        async with async_session_factory() as session:
            stmt = select(self.model_user).filter_by(email=email)
            res = await session.execute(stmt)
            return res.scalar_one()

    async def get_one_from_id(self, user_id: str):
        async with async_session_factory() as session:
            stmt = select(self.model_user).filter_by(id=user_id)
            res = await session.execute(stmt)
            return res.scalar_one()

    async def get_one_from_tg_id(self, tg_id: str):
        async with async_session_factory() as session:
            stmt = select(self.model_user).filter_by(tg_id=tg_id)
            res = await session.execute(stmt)
            return res.scalar_one()

    async def get_email_and_pass(self, email):
        async with async_session_factory() as session:
            stmt = select(self.model_user).filter_by(email=email)
            res = await session.execute(stmt)
            return res.scalar_one()

    async def add_refresh_token_for_user(self, user_id: int, refresh_token: str):
        async with async_session_factory() as session:
            stmt = insert(self.model_refresh_tokens).values(user_id=user_id, refresh_token=refresh_token)
            await session.execute(stmt)
            await session.commit()

    async def update_user_data(self, data: dict):
        async with async_session_factory() as session:
            user_id = data.get('id')
            stmt = update(self.model_user).filter_by(id=user_id).values(**data)
            await session.execute(stmt)
            await session.commit()

    async def delete_refresh_token_for_user(self, refresh_token):
        async with async_session_factory() as session:
            stmt = delete(self.model_refresh_tokens).filter_by(refresh_token=refresh_token)
            await session.execute(stmt)
            await session.commit()
