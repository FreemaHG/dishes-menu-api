import json
import uuid
from http import HTTPStatus

import pytest
from httpx import AsyncClient

from src.main import app
from src.models.dish import Dish
from src.models.menu import Menu
from src.models.submenu import Submenu
from src.schemas.dish import DishInSchema, DishOutSchema
from src.schemas.response import ResponseForDeleteSchema, ResponseSchema


@pytest.mark.integration
class TestDishesRoutes:
    """
    Тестирование роутов для создания, вывода, обновления и удаления блюд
    """

    @pytest.fixture(scope='class')
    async def dish_update_data(self) -> dict:
        """
        Данные для частичного обновления блюда
        """
        return {
            'title': 'Update test dish',
            'price': 99
        }

    async def test_create_dish(
            self,
            menu: Menu,
            submenu: Submenu,
            client: AsyncClient,
            dish_schema: DishInSchema
    ) -> None:
        """
        Проверка роута для создания нового блюда
        """
        url = app.url_path_for('create_dish', menu_id=menu.id, submenu_id=submenu.id)
        resp = await client.post(url, json=dish_schema.model_dump())

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert DishOutSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_create_dish_fail(
            self,
            menu: Menu,
            submenu: Submenu,
            client: AsyncClient,
            invalid_data: dict
    ) -> None:
        """
        Проверка ответа при создании блюда при невалидных данных
        """
        url = app.url_path_for('create_dish', menu_id=menu.id, submenu_id=submenu.id)
        resp = await client.post(url, json=json.dumps(invalid_data))

        assert resp
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_get_dish(
            self,
            menu: Menu,
            submenu: Submenu,
            dish: Dish,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для вывода блюда по id
        """
        url = app.url_path_for('get_dish', menu_id=menu.id, submenu_id=submenu.id, dish_id=dish.id)
        resp = await client.get(url)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert DishOutSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_get_dish_not_found(
            self,
            menu: Menu,
            submenu: Submenu,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения, что блюдо не найдено
        """
        url = app.url_path_for('get_dish', menu_id=menu.id, submenu_id=submenu.id, dish_id=uuid.uuid4())
        resp = await client.get(url)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert ResponseSchema.model_validate(resp.json())

    @pytest.mark.usefixtures('dish')
    async def test_get_list_dishes(
            self,
            menu: Menu,
            submenu: Submenu,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для вывода списка блюд
        """
        url = app.url_path_for('get_dishes_list', menu_id=menu.id, submenu_id=submenu.id)
        resp = await client.get(url)
        resp_json = resp.json()

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert DishOutSchema.model_validate(resp_json[0])
        assert isinstance(resp_json, list)

    async def test_update_dish(
            self,
            menu: Menu,
            submenu: Submenu,
            dish: Dish,
            dish_update_data: dict,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для частичного обновления блюда
        """
        url = app.url_path_for('update_dish', menu_id=menu.id, submenu_id=submenu.id, dish_id=dish.id)
        resp = await client.patch(url, content=json.dumps(dish_update_data))

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert DishOutSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_update_dish_not_found(
            self,
            menu: Menu,
            submenu: Submenu,
            dish_update_data: dict,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения, что блюдо не найдено
        """
        url = app.url_path_for('update_dish', menu_id=menu.id, submenu_id=submenu.id, dish_id=uuid.uuid4())
        resp = await client.patch(url, content=json.dumps(dish_update_data))

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert ResponseSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_update_dish_validation_error(
            self,
            menu: Menu,
            submenu: Submenu,
            dish: Dish,
            invalid_data: dict,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения о невалидном URL для вывода блюда
        """
        url = app.url_path_for('update_dish', menu_id=menu.id, submenu_id=submenu.id, dish_id=dish.id)
        resp = await client.patch(url, content=json.dumps(invalid_data))

        assert resp
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_delete_dish(
            self,
            menu: Menu,
            submenu: Submenu,
            dish: Dish,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для удаления блюда
        """
        url = app.url_path_for('update_dish', menu_id=menu.id, submenu_id=submenu.id, dish_id=dish.id)
        resp = await client.delete(url)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert ResponseForDeleteSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_delete_dish_not_found(
            self,
            menu: Menu,
            submenu: Submenu,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения, что удаляемое блюдо не найдено
        """
        url = app.url_path_for('update_dish', menu_id=menu.id, submenu_id=submenu.id, dish_id=uuid.uuid4())
        resp = await client.delete(url)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert ResponseSchema.model_validate(resp.json())
