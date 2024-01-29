from typing import Dict

import pytest

from src.models.dish import Dish
from src.models.menu import Menu
from src.models.submenu import Submenu


@pytest.fixture(scope="class")
async def menus_url() -> str:
    """
    Базовый URL для вывода списка меню
    """
    return "/api/v1/menus"


@pytest.fixture(scope="class")
async def menu_url(menus_url: str, menu: Menu) -> str:
    """
    URL адрес с id конкретного меню
    """
    return "/".join([menus_url, str(menu.id)])


@pytest.fixture(scope="class")
async def submenus_url(menu_url: str) -> str:
    """
    Базовый URL для вывода списка подменю
    """
    return "/".join([menu_url, "submenus"])


@pytest.fixture(scope="class")
async def submenu_url(submenus_url: str, submenu: Submenu) -> str:
    """
    URL адрес с id конкретного подменю
    """
    return "/".join([submenus_url, str(submenu.id)])


@pytest.fixture(scope="class")
async def dishes_url(submenu_url: str) -> str:
    """
    Базовый URL для вывода списка блюд
    """
    return "/".join([submenu_url, "dishes"])


@pytest.fixture(scope="class")
async def dish_url(dishes_url: str, dish: Dish) -> str:
    """
    URL адрес с id конкретного блюда
    """
    return "/".join([dishes_url, str(dish.id)])


@pytest.fixture(scope="class")
async def menu_url_invalid(menu_url: str) -> str:
    """
    URL адрес с невалидным id меню (для проверки статуса 404)
    """
    return "/".join([menu_url[:-1], "9"])


@pytest.fixture(scope="class")
async def submenu_url_invalid(submenu_url: str) -> str:
    """
    URL адрес с невалидным id подменю (для проверки статуса 404)
    """
    return "/".join([submenu_url[:-1], "9"])


@pytest.fixture(scope="class")
async def dish_url_invalid(dish_url: str) -> str:
    """
    URL адрес с невалидным id блюда (для проверки статуса 404)
    """
    return "/".join([dish_url[:-1], "9"])


@pytest.fixture(scope="class")
async def invalid_data() -> Dict:
    """
    Невалидные данные для добавления нового меню / подменю
    """
    return {"title": 123, "description": 456}
