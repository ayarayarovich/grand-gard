from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)
create_session = async_sessionmaker(engine, expire_on_commit=False, future=True)


async def get_db_session() -> AsyncSession:
    try:
        session = create_session()
        yield session
    finally:
        await session.close()
