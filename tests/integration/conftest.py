from typing import Dict
from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.menu import Menu
from src.schemas.base import BaseInSchema


@pytest.fixture(scope="session")
async def menu_schema(menu_data: Dict) -> BaseInSchema:
    """
    Объект схемы для передачи данных для создания нового меню
    """
    menu = BaseInSchema(**menu_data)

    return menu


@pytest.fixture(scope="class")
async def menu(session: AsyncSession, menu_data: Dict) -> Menu:
    """
    Тестовая запись с меню для проверки GET-запросов и установки связи для подменю
    """
    menu = Menu(**menu_data)
    session.add(menu)
    await session.commit()

    return menu


@pytest.fixture(scope="class")
async def menu_url(menus_url: str, menu: Menu) -> str:
    """
    URL адрес с id конкретного меню
    """
    return "/".join([menus_url, str(menu.id)])


@pytest.fixture(scope="class")
async def menu_url_invalid(menu_url: str) -> str:
    """
    URL адрес с невалидным id меню (для проверки статуса 404)
    """
    return "/".join([menu_url[:-1], "9"])
