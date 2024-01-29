import json
from http import HTTPStatus
from typing import Dict
import pytest
from httpx import AsyncClient

from src.schemas.dish import DishInSchema, DishOutSchema
from src.schemas.response import ResponseSchema, ResponseForDeleteSchema


@pytest.mark.integration
class TestDishesRoutes:
    """
    Тестирование роутов для создания, вывода, обновления и удаления блюд
    """

    @pytest.fixture(scope="class")
    async def dish_update_data(self) -> Dict:
        """
        Данные для частичного обновления блюда
        """
        return {
            "title": "Update test dish",
            "price": 99
        }


    async def test_create_dish(
            self,
            dishes_url: str,
            client: AsyncClient,
            dish_schema: DishInSchema
    ) -> None:
        """
        Проверка роута для создания нового блюда
        """
        resp = await client.post(dishes_url, json=dish_schema.model_dump())

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert DishOutSchema.model_validate(resp.json())


    @pytest.mark.fail
    async def test_create_dish_fail(
            self,
            dishes_url: str,
            client: AsyncClient,
            invalid_data: Dict
    ) -> None:
        """
        Проверка ответа при создании блюда при невалидных данных
        """
        resp = await client.post(dishes_url, json=json.dumps(invalid_data))

        assert resp
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_get_dish(
            self,
            dish_url: str,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для вывода блюда по id
        """
        resp = await client.get(dish_url)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert DishOutSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_get_dish_not_found(
            self,
            dish_url_invalid: str,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения, что блюдо не найдено
        """
        resp = await client.get(dish_url_invalid)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert ResponseSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_get_dish_validation_error(
            self,
            dishes_url: str,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения о невалидном URL для вывода блюда
        """
        resp = await client.get("/".join([dishes_url, "9"]))

        assert resp
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.usefixtures("dish")
    async def test_get_list_dishes(
            self,
            dishes_url: str,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для вывода списка блюд
        """
        resp = await client.get(dishes_url)
        resp_json = resp.json()

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert DishOutSchema.model_validate(resp_json[0])
        assert isinstance(resp_json, list)

    async def test_update_dish(
            self,
            dish_url: str,
            dish_update_data: Dict,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для частичного обновления блюда
        """
        resp = await client.patch(dish_url, content=json.dumps(dish_update_data))

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert DishOutSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_update_dish_not_found(
            self,
            dish_url_invalid: str,
            dish_update_data: Dict,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения, что блюдо не найдено
        """
        resp = await client.patch(dish_url_invalid, content=json.dumps(dish_update_data))

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert ResponseSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_update_dish_validation_error(
            self,
            dish_url: str,
            invalid_data: Dict,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения о невалидном URL для вывода блюда
        """
        resp = await client.patch(dish_url, content=json.dumps(invalid_data))

        assert resp
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_delete_dish(
            self,
            dish_url: str,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для удаления блюда
        """
        resp = await client.delete(dish_url)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert ResponseForDeleteSchema.model_validate(resp.json())

    @pytest.mark.fail
    async def test_delete_dish_not_found(
            self,
            dish_url_invalid: str,
            client: AsyncClient
    ) -> None:
        """
        Проверка вывода сообщения, что удаляемое блюдо не найдено
        """
        resp = await client.delete(dish_url_invalid)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert ResponseSchema.model_validate(resp.json())
