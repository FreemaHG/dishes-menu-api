import json
import uuid
from http import HTTPStatus

import pytest
from httpx import AsyncClient

from src.main import app
from src.models.menu import Menu
from src.models.submenu import Submenu
from src.schemas.base import BaseInSchema
from src.schemas.response import ResponseForDeleteSchema, ResponseSchema
from src.schemas.submenu import SubmenuOutSchema


@pytest.mark.integration
class TestSubmenusRoutes:
    """
    Тестирование роутов для создания, вывода, обновления и удаления подменю
    """

    async def test_create_submenu(
            self,
            menu: Menu,
            client: AsyncClient,
            submenu_schema: BaseInSchema
    ) -> None:
        """
        Проверка роута для создания нового подменю
        """
        url = app.url_path_for('create_submenu', menu_id=menu.id)
        resp = await client.post(url, json=submenu_schema.model_dump())

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert SubmenuOutSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_create_submenu_fail(
            self,
            menu: Menu,
            client: AsyncClient,
            invalid_data: dict
    ) -> None:
        """
        Проверка ответа при создании подменю при невалидных данных
        """
        url = app.url_path_for('create_submenu', menu_id=menu.id)
        resp = await client.post(url, json=json.dumps(invalid_data))

        assert resp
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_get_submenu(
            self,
            menu: Menu,
            submenu: Submenu,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для вывода подменю по id
        """
        url = app.url_path_for('get_submenu', menu_id=menu.id, submenu_id=submenu.id)
        resp = await client.get(url)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert SubmenuOutSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_get_submenu_not_found(
            self,
            menu: Menu,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения, что подменю не найдено
        """
        url = app.url_path_for('get_submenu', menu_id=menu.id, submenu_id=uuid.uuid4())
        resp = await client.get(url)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert ResponseSchema.model_validate(resp.json())

    @pytest.mark.usefixtures('submenu')
    async def test_get_list_submenu(
            self,
            menu: Menu,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для вывода списка подменю
        """
        url = app.url_path_for('get_submenus_list', menu_id=menu.id)
        resp = await client.get(url)
        resp_json = resp.json()

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert SubmenuOutSchema.model_validate(resp_json[0])
        assert isinstance(resp_json, list)

    async def test_update_submenu(
            self,
            menu: Menu,
            submenu: Submenu,
            submenu_update_data: dict,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для частичного обновления подменю
        """
        url = app.url_path_for('update_submenu', menu_id=menu.id, submenu_id=submenu.id)
        resp = await client.patch(url, content=json.dumps(submenu_update_data))

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert SubmenuOutSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_update_submenu_not_found(
            self,
            menu: Menu,
            submenu: Submenu,
            submenu_update_data: dict,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения, что подменю не найдено
        """
        url = app.url_path_for('update_submenu', menu_id=menu.id, submenu_id=uuid.uuid4())
        resp = await client.patch(url, content=json.dumps(submenu_update_data))

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert ResponseSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_update_submenu_validation_error(
            self,
            menu: Menu,
            submenu: Submenu,
            invalid_data: dict,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения о невалидном URL для вывода меню
        """
        url = app.url_path_for('update_submenu', menu_id=menu.id, submenu_id=submenu.id)
        resp = await client.patch(url, content=json.dumps(invalid_data))

        assert resp
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_delete_submenu(
            self,
            menu: Menu,
            submenu: Submenu,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для удаления подменю
        """
        url = app.url_path_for('delete_submenu', menu_id=menu.id, submenu_id=submenu.id)
        resp = await client.delete(url)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert ResponseForDeleteSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_delete_submenu_not_found(
            self,
            menu: Menu,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения, что удаляемое подменю не найдено
        """
        url = app.url_path_for('delete_submenu', menu_id=menu.id, submenu_id=uuid.uuid4())
        resp = await client.delete(url)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert ResponseSchema.model_validate(resp.json())
