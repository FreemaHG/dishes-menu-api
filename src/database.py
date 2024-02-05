from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
metadata = MetaData()
engine = create_async_engine(DATABASE_URL)


class Base(DeclarativeBase):
    """
    Базовый класс для декларативного описания моделей
    """

    pass


# Объект асинхронной сессии для запросов к БД
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор, возвращающий объект асинхронной сессии
    """
    async with async_session_maker() as session:
        yield session
