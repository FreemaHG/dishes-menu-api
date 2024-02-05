from http import HTTPStatus

import pytest
from httpx import AsyncClient

from src.main import app
from src.models.menu import Menu
from src.schemas.menu import MenuOutSchema


@pytest.mark.unit
class TestReverse:
    """
    Тестирование reverse-функции, позволяющей делать запросы к роуту через urlname
    """

    @pytest.fixture(scope='class')
    async def control_url(
            self,
            menu: Menu
    ) -> str:
        """
        URL для проверки
        """
        return f'/api/v1/menus/{menu.id}'

    async def test_reverse(
            self,
            control_url: str,
            menu: Menu,
            client: AsyncClient
    ):
        """
        Проверка корректности отправки запроса по urlname
        """
        url = app.url_path_for('get_menu', menu_id=menu.id)

        resp = await client.get(url)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert MenuOutSchema.model_validate(resp.json())
        assert url == control_url
