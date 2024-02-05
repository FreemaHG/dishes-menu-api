from http import HTTPStatus

import pytest
from httpx import AsyncClient

from src.models.menu import Menu
from src.models.submenu import Submenu
from src.schemas.dish import DishOutSchema
from src.schemas.menu import MenuOutSchema
from src.schemas.response import ResponseForDeleteSchema
from src.schemas.submenu import SubmenuOutSchema


@pytest.mark.integration
class TestCheckDishesAndSubmenusCount:
    """
    Тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman
    """
    __menu_id = None
    __submenu_id = None
    __first_dish_id = None
    __second_dish_id = None

    @pytest.fixture(scope='class')
    async def new_menu_data(self) -> dict:
        """
        Данные для создания нового меню
        """
        return {
            'title': 'First some menu',
            'description': 'Description for first some menu'
        }

    @pytest.fixture(scope='class')
    async def new_submenu_data(
            self,
            menu: Menu,
    ) -> dict:
        """
        Данные для создания нового подменю
        """
        return {
            'menu_id': TestCheckDishesAndSubmenusCount.__menu_id,
            'title': 'First some submenu',
            'description': 'Description for first some submenu'
        }

    @pytest.fixture(scope='class')
    async def new_first_dish_data(
            self,
            submenu: Submenu
    ) -> dict:
        """
        Данные для создания нового блюда
        """
        return {
            'submenu_id': TestCheckDishesAndSubmenusCount.__submenu_id,
            'title': 'First some dish',
            'description': 'Description for first some dish',
            'price': 123
        }

    @pytest.fixture(scope='class')
    async def new_second_dish_data(
            self,
            submenu: Submenu
    ) -> dict:
        """
        Данные для создания нового блюда
        """
        return {
            'submenu_id': TestCheckDishesAndSubmenusCount.__submenu_id,
            'title': 'Second some dish',
            'description': 'Description for second some dish',
            'price': 68
        }

    async def test_create_menu(
            self,
            client: AsyncClient,
            new_menu_data: dict
    ) -> None:
        """
        Проверка роута для создания нового меню
        """
        resp = await client.post('/api/v1/menus', json=new_menu_data)
        resp_json = resp.json()

        TestCheckDishesAndSubmenusCount.__menu_id = resp_json['id']

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert MenuOutSchema.model_validate(resp_json)

    async def test_create_submenu(
            self,
            client: AsyncClient,
            new_submenu_data: dict
    ) -> None:
        """
        Проверка роута для создания нового подменю
        """
        resp = await client.post(
            f'/api/v1/menus/{TestCheckDishesAndSubmenusCount.__menu_id}/submenus',
            json=new_submenu_data
        )
        resp_json = resp.json()
        TestCheckDishesAndSubmenusCount.__submenu_id = resp_json['id']

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert SubmenuOutSchema.model_validate(resp_json)

    async def test_create_first_dish(
            self,
            client: AsyncClient,
            new_first_dish_data: dict
    ) -> None:
        """
        Проверка роута для создания нового блюда
        """
        resp = await client.post(
            f'/api/v1/menus/{TestCheckDishesAndSubmenusCount.__menu_id}/submenus/'
            f'{TestCheckDishesAndSubmenusCount.__submenu_id}/dishes',
            json=new_first_dish_data
        )
        resp_json = resp.json()
        TestCheckDishesAndSubmenusCount.__first_dish_id = resp_json['id']

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert DishOutSchema.model_validate(resp_json)

    async def test_create_second_dish(
            self,
            client: AsyncClient,
            new_second_dish_data: dict
    ) -> None:
        """
        Проверка роута для создания нового блюда
        """
        resp = await client.post(
            f'/api/v1/menus/{TestCheckDishesAndSubmenusCount.__menu_id}/submenus/'
            f'{TestCheckDishesAndSubmenusCount.__submenu_id}/dishes',
            json=new_second_dish_data
        )
        resp_json = resp.json()
        TestCheckDishesAndSubmenusCount.__second_dish_id = resp_json['id']

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert DishOutSchema.model_validate(resp_json)

    async def test_get_menu(
            self,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для вывода меню по id
        """
        resp = await client.get(f'/api/v1/menus/{TestCheckDishesAndSubmenusCount.__menu_id}')
        resp_json = resp.json()

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert MenuOutSchema.model_validate(resp_json)
        assert resp_json['submenus_count'] == 1
        assert resp_json['dishes_count'] == 2

    async def test_get_submenu(
            self,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для вывода подменю по id
        """
        resp = await client.get(
            f'/api/v1/menus/{TestCheckDishesAndSubmenusCount.__menu_id}/submenus/'
            f'{TestCheckDishesAndSubmenusCount.__submenu_id}'
        )
        resp_json = resp.json()

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert SubmenuOutSchema.model_validate(resp_json)
        assert resp_json['dishes_count'] == 2

    async def test_delete_submenu(
            self,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для удаления подменю
        """
        resp = await client.delete(
            f'/api/v1/menus/{TestCheckDishesAndSubmenusCount.__menu_id}/submenus/'
            f'{TestCheckDishesAndSubmenusCount.__submenu_id}'
        )

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert ResponseForDeleteSchema.model_validate(resp.json())

    async def test_get_list_submenu(
            self,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для вывода списка подменю
        """
        resp = await client.get(
            f'/api/v1/menus/{TestCheckDishesAndSubmenusCount.__menu_id}/submenus'
        )
        resp_json = resp.json()

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert isinstance(resp_json, list)
        assert len(resp_json) == 0

    async def test_get_list_dishes(
            self,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для вывода списка блюд
        """
        resp = await client.get(
            f'/api/v1/menus/{TestCheckDishesAndSubmenusCount.__menu_id}/submenus/'
            f'{TestCheckDishesAndSubmenusCount.__submenu_id}/dishes',
        )
        resp_json = resp.json()

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert isinstance(resp_json, list)
        assert len(resp_json) == 0

    async def test_get_menu_again(
            self,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для вывода меню по id
        """
        resp = await client.get(f'/api/v1/menus/{TestCheckDishesAndSubmenusCount.__menu_id}')
        resp_json = resp.json()

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert MenuOutSchema.model_validate(resp_json)
        assert resp_json['submenus_count'] == 0
        assert resp_json['dishes_count'] == 0

    async def test_delete_menu(
            self,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для удаления меню
        """
        resp = await client.delete(f'/api/v1/menus/{TestCheckDishesAndSubmenusCount.__menu_id}')

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert ResponseForDeleteSchema.model_validate(resp.json())

    async def test_get_list_menu(
            self,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для вывода списка меню
        """
        resp = await client.get('/api/v1/menus')
        resp_json = resp.json()

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert isinstance(resp_json, list)
