import json
from http import HTTPStatus

import pytest
from httpx import AsyncClient

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
            submenus_url: str,
            client: AsyncClient,
            submenu_schema: BaseInSchema
    ) -> None:
        """
        Проверка роута для создания нового подменю
        """
        resp = await client.post(submenus_url, json=submenu_schema.model_dump())

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert SubmenuOutSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_create_submenu_fail(
            self,
            submenus_url: str,
            client: AsyncClient,
            invalid_data: dict
    ) -> None:
        """
        Проверка ответа при создании подменю при невалидных данных
        """
        resp = await client.post(submenus_url, json=json.dumps(invalid_data))

        assert resp
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_get_submenu(
            self,
            submenu_url: str,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для вывода подменю по id
        """
        resp = await client.get(submenu_url)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert SubmenuOutSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_get_submenu_not_found(
            self,
            submenu_url_invalid: str,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения, что подменю не найдено
        """
        resp = await client.get(submenu_url_invalid)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert ResponseSchema.model_validate(resp.json())

    @pytest.mark.usefixtures('submenu')
    async def test_get_list_submenu(
            self,
            submenus_url: str,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для вывода списка подменю
        """
        resp = await client.get(submenus_url)
        resp_json = resp.json()

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert SubmenuOutSchema.model_validate(resp_json[0])
        assert isinstance(resp_json, list)

    async def test_update_submenu(
            self,
            submenu_url: str,
            submenu_update_data: dict,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для частичного обновления подменю
        """
        resp = await client.patch(submenu_url, content=json.dumps(submenu_update_data))

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert SubmenuOutSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_update_submenu_not_found(
            self,
            submenu_url_invalid: str,
            submenu_update_data: dict,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения, что подменю не найдено
        """
        resp = await client.patch(submenu_url_invalid, content=json.dumps(submenu_update_data))

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert ResponseSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_update_submenu_validation_error(
            self,
            submenu_url: str,
            invalid_data: dict,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения о невалидном URL для вывода меню
        """
        resp = await client.patch(submenu_url, content=json.dumps(invalid_data))

        assert resp
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_delete_submenu(
            self,
            submenu_url: str,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для удаления подменю
        """
        resp = await client.delete(submenu_url)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert ResponseForDeleteSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_delete_submenu_not_found(
            self,
            submenu_url_invalid: str,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения, что удаляемое подменю не найдено
        """
        resp = await client.delete(submenu_url_invalid)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert ResponseSchema.model_validate(resp.json())
