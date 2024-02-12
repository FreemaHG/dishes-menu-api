import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.dish import Dish
from src.models.menu import Menu
from src.models.submenu import Submenu
from src.schemas.base import BaseInOptionalSchema, BaseInSchema
from src.schemas.dish import DishInOptionalSchema, DishInSchema
from tests.database import Base, app, async_session_maker, engine_test


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


# Пример рекомендуемого кода из документации по асинхронному тестированию FastApi
@pytest.fixture(autouse=True, scope='session')
def event_loop(request):
    """
    Create an instance of the default event loop for each test case.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def session() -> AsyncGenerator[AsyncSession, None]:
    """
    Объект асинхронной сессии для выполнения запросов к БД
    """
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Асинхронный клиент для выполнения запросов
    """
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='class')
async def menu_data() -> dict:
    """
    Данные для создания нового меню
    """
    return {'title': 'Test menu', 'description': 'Description for test menu'}


@pytest.fixture(scope='class')
async def menu_update_data() -> dict:
    """
    Данные для частичного обновления меню
    """
    return {'title': 'Update test menu'}


@pytest.fixture(scope='class')
async def menu_update_schema(menu_update_data: dict) -> BaseInOptionalSchema:
    """
    Схема с данными для частичного обновления меню
    """
    return BaseInOptionalSchema(**menu_update_data)


@pytest.fixture(scope='class')
async def submenu_update_data() -> dict:
    """
    Данные для частичного обновления подменю
    """
    return {'title': 'Update test submenu'}


@pytest.fixture(scope='class')
async def submenu_update_schema(submenu_update_data: dict) -> BaseInOptionalSchema:
    """
    Схема с данными для частичного обновления подменю
    """
    return BaseInOptionalSchema(**submenu_update_data)


@pytest.fixture(scope='class')
async def dish_update_data() -> dict:
    """
    Данные для частичного обновления блюда
    """
    return {'title': 'Update test dish'}


@pytest.fixture(scope='class')
async def dish_update_schema(dish_update_data: dict) -> DishInOptionalSchema:
    """
    Схема с данными для частичного обновления блюда
    """
    return DishInOptionalSchema(**dish_update_data)


@pytest.fixture(scope='class')
async def submenu_data(menu: Menu) -> dict:
    """
    Данные для создания нового подменю
    """
    return {'menu_id': menu.id, 'title': 'Test submenu', 'description': 'Description for test submenu'}


@pytest.fixture(scope='class')
async def dish_data(submenu: Submenu) -> dict:
    """
    Данные для создания нового блюда
    """
    return {
        'submenu_id': submenu.id,
        'title': 'Test dish',
        'description': 'Description for test dish',
        'price': 100
    }


@pytest.fixture(scope='class')
async def menu_schema(menu_data: dict) -> BaseInSchema:
    """
    Объект схемы для передачи данных для создания нового меню
    """
    menu = BaseInSchema(**menu_data)

    return menu


@pytest.fixture(scope='class')
async def submenu_schema(submenu_data: dict) -> BaseInSchema:
    """
    Объект схемы для передачи данных для создания нового подменю
    """
    submenu = BaseInSchema(**submenu_data)

    return submenu


@pytest.fixture(scope='class')
async def dish_schema(dish_data: dict) -> BaseInSchema:
    """
    Объект схемы для передачи данных для создания нового блюда
    """
    dish = DishInSchema(**dish_data)

    return dish


@pytest.fixture(scope='class')
async def menu(session: AsyncSession, menu_data: dict) -> Menu:
    """
    Тестовая запись с меню для проверки GET-запросов и установки связи для подменю
    """
    menu = Menu(**menu_data)
    session.add(menu)
    await session.commit()

    return menu


@pytest.fixture(scope='class')
async def submenu(session: AsyncSession, submenu_data: dict) -> Submenu:
    """
    Тестовая запись с подменю для проверки GET-запросов и установки связи для блюд
    """
    submenu = Submenu(**submenu_data)
    session.add(submenu)
    await session.commit()

    return submenu


@pytest.fixture(scope='class')
async def dish(session: AsyncSession, dish_data: dict) -> Dish:
    """
    Тестовая запись с блюдом для проверки GET-запросов
    """
    dish = Dish(**dish_data)
    session.add(dish)
    await session.commit()

    return dish
