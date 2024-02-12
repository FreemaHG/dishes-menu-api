from src.main import app
from src.models.menu import Menu
from src.routes.all_data import get_all_data


class AllDataUrl:
    """
    Метод класса имитирует функцию reverse() в Django, позволяя вызывать роут по urlname для вывода всех данных
    """

    @app.get('api/v1/menus/all_data')
    async def get_all_data_by_urlname(cls) -> list[Menu]:
        """
        Вызов роута для вывода всех данных
        """
        return await get_all_data()
