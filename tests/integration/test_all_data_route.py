from http import HTTPStatus

import pytest
from httpx import AsyncClient

from src.main import app
from src.schemas.menu import MenuWithSubmenusOutSchema


@pytest.mark.integration
class TestAllDataRoute:
    """
    Тестирование роута для вывода всех данных
    """

    @pytest.mark.usefixtures('menu', 'submenu', 'dish')
    async def test_get_list_menu(
            self,
            client: AsyncClient
    ) -> None:
        """
        Проверка роута для вывода списка меню
        """

        url = app.url_path_for('get_all_data')
        resp = await client.get(url)
        resp_json = resp.json()

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert MenuWithSubmenusOutSchema.model_validate(resp_json[0])
        assert isinstance(resp_json, list)
