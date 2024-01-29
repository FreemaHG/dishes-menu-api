import json
from http import HTTPStatus
from typing import Dict
import pytest
from httpx import AsyncClient

from src.schemas.base import BaseInSchema
from src.schemas.menu import MenuOutSchema
from src.schemas.response import ResponseSchema, ResponseForDeleteSchema


@pytest.mark.integration
class TestMenusRoutes:
    """
    Тестирование роутов для создания, вывода, обновления и удаления меню
    """

    async def test_create_menu(
            self,
            menus_url: str,
            client: AsyncClient,
            menu_schema: BaseInSchema
    ) -> None:
        """
        Проверка роута для создания нового меню
        """
        resp = await client.post(menus_url, json=menu_schema.model_dump())

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert MenuOutSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_create_menu_fail(
            self,
            menus_url: str,
            client: AsyncClient,
            invalid_data: Dict
    ) -> None:
        """
        Проверка ответа при создании меню при невалидных данных
        """
        resp = await client.post(menus_url, content=json.dumps(invalid_data))

        assert resp
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_get_menu(
            self,
            menu_url: str,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для вывода меню по id
        """
        resp = await client.get(menu_url)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert MenuOutSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_get_menu_not_found(
            self,
            menu_url_invalid: str,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения, что меню не найдено
        """
        resp = await client.get(menu_url_invalid)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert ResponseSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_get_menu_validation_error(
            self,
            menus_url: str,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения о невалидном URL для вывода меню
        """
        resp = await client.get("/".join([menus_url, "9"]))

        assert resp
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.usefixtures("menu")
    async def test_get_list_menu(
            self,
            menus_url: str,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для вывода списка меню
        """
        resp = await client.get(menus_url)
        resp_json = resp.json()

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert MenuOutSchema.model_validate(resp_json[0])
        assert isinstance(resp_json, list)

    async def test_update_menu(
            self,
            menu_url: str,
            menu_update_data: Dict,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для частичного обновления меню
        """
        resp = await client.patch(menu_url, content=json.dumps(menu_update_data))

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert MenuOutSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_update_menu_not_found(
            self,
            menu_url_invalid: str,
            menu_update_data: Dict,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения, что меню не найдено
        """
        resp = await client.patch(menu_url_invalid, content=json.dumps(menu_update_data))

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert ResponseSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_update_menu_validation_error(
            self,
            menu_url: str,
            invalid_data: Dict,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения о невалидном URL для вывода меню
        """
        resp = await client.patch(menu_url, content=json.dumps(invalid_data))

        assert resp
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_delete_menu(
            self,
            menu_url: str,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для удаления меню
        """
        resp = await client.delete(menu_url)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert ResponseForDeleteSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_delete_menu_not_found(
            self,
            menu_url_invalid: str,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения, что удаляемое меню не найдено
        """
        resp = await client.delete(menu_url_invalid)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert ResponseSchema.model_validate(resp.json())
