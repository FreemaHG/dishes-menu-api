import pytest
from typing import AsyncGenerator, Dict
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.main import app
from tests.database import engine_test, async_session_maker, Base


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    """
    Создание и удаление БД перед тестами
    """
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def session() -> AsyncGenerator[AsyncSession, None]:
    """
    Объект асинхронной сессии для выполнения запросов к БД
    """
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Асинхронный клиент для выполнения запросов
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def menus_url() -> str:
    return "/api/v1/menus"


@pytest.fixture(scope="session")
async def menu_data() -> Dict:
    """
    Данные для создания нового меню
    """
    return {"title": "Test menu", "description": "Description for test menu"}
