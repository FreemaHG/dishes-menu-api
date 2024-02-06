import json
import uuid
from http import HTTPStatus

import pytest
from httpx import AsyncClient

from src.main import app
from src.models.menu import Menu
from src.schemas.base import BaseInSchema
from src.schemas.menu import MenuOutSchema
from src.schemas.response import ResponseForDeleteSchema, ResponseSchema


@pytest.mark.integration
class TestMenusRoutes:
    """
    Тестирование роутов для создания, вывода, обновления и удаления меню
    """

    async def test_create_menu(
            self,
            client: AsyncClient,
            menu_schema: BaseInSchema
    ) -> None:
        """
        Проверка роута для создания нового меню
        """
        url = app.url_path_for('create_menu')
        resp = await client.post(url, json=menu_schema.model_dump())

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert MenuOutSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_create_menu_fail(
            self,
            client: AsyncClient,
            invalid_data: dict
    ) -> None:
        """
        Проверка ответа при создании меню при невалидных данных
        """
        url = app.url_path_for('create_menu')
        resp = await client.post(url, content=json.dumps(invalid_data))

        assert resp
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_get_menu(
            self,
            menu: Menu,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для вывода меню по id (через reverse())
        """
        url = app.url_path_for('get_menu', menu_id=menu.id)
        resp = await client.get(url)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert MenuOutSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_get_menu_not_found(
            self,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения, что меню не найдено
        """
        url = app.url_path_for('get_menu', menu_id=uuid.uuid4())
        resp = await client.get(url)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert ResponseSchema.model_validate(resp.json())

    @pytest.mark.usefixtures('menu')
    async def test_get_list_menu(
            self,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для вывода списка меню
        """
        url = app.url_path_for('get_menu_list')
        resp = await client.get(url)
        resp_json = resp.json()

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert MenuOutSchema.model_validate(resp_json[0])
        assert isinstance(resp_json, list)

    async def test_update_menu(
            self,
            menu: Menu,
            menu_update_data: dict,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для частичного обновления меню
        """
        url = app.url_path_for('update_menu', menu_id=menu.id)
        resp = await client.patch(url, content=json.dumps(menu_update_data))

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert MenuOutSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_update_menu_not_found(
            self,
            menu_update_data: dict,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения, что меню не найдено
        """
        url = app.url_path_for('update_menu', menu_id=uuid.uuid4())
        resp = await client.patch(url, content=json.dumps(menu_update_data))

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert ResponseSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_update_menu_validation_error(
            self,
            menu: Menu,
            invalid_data: dict,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения о невалидном URL для вывода меню
        """
        url = app.url_path_for('update_menu', menu_id=menu.id)
        resp = await client.patch(url, content=json.dumps(invalid_data))

        assert resp
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_delete_menu(
            self,
            menu: Menu,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для удаления меню
        """
        url = app.url_path_for('delete_menu', menu_id=menu.id)
        resp = await client.delete(url)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert ResponseForDeleteSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_delete_menu_not_found(
            self,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения, что удаляемое меню не найдено
        """
        url = app.url_path_for('delete_menu', menu_id=uuid.uuid4())
        resp = await client.delete(url)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert ResponseSchema.model_validate(resp.json())
