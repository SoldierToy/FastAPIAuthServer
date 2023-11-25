from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from settings import settings

engine = create_async_engine(
    url=settings.get_db_url(),
    echo=True
)

async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False
)


async def get_async_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session
        await session.close()
