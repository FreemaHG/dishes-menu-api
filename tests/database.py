from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from src.config import (
    DB_HOST_TEST,
    DB_NAME_TEST,
    DB_PASS_TEST,
    DB_PORT_TEST,
    DB_USER_TEST,
)
from src.database import Base, get_async_session
from src.main import app

DATABASE_URL_TEST = (
    f'postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'
)

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)

async_session_maker = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)

# Связываем с объектом методанных тестовый движок, чтобы таблицы создавались именно в тестовой БД
Base.metadata.bind = engine_test

# Переписываем зависимость приложения (функцию), возвращающую объект сессии для работы с БД


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

# Переопределяем в приложении зависимость возврата сессии на только что объявленную выше
app.dependency_overrides[get_async_session] = override_get_async_session
