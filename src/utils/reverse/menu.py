from uuid import UUID

from src.main import app
from src.models.menu import Menu
from src.routes.menu import (
    create_menu,
    delete_menu,
    get_menu,
    get_menu_list,
    update_menu,
)


class MenuUrl:
    """
    Методы класса имитируют функции reverse() в Django, позволяя вызывать нужный роут по urlname для меню
    """

    @app.get('api/v1/menus')
    async def get_menus_list_by_urlname(cls) -> list[Menu]:
        """
        Вызов роута для вывода списка меню
        """
        return await get_menu_list()

    @app.post('api/v1/menus')
    async def create_menu_by_urlname(cls) -> Menu:
        """
        Вызов роута для создания меню
        """
        return await create_menu()

    @app.get('api/v1/menus/{menu_id}')
    async def get_menu_by_urlname(cls, menu_id: UUID) -> Menu:
        """
        Вызов роута для вывода меню по id
        """
        return await get_menu(menu_id)

    @app.patch('api/v1/menus/{menu_id}')
    async def update_menu_by_urlname(cls, menu_id: UUID) -> Menu:
        """
        Вызов роута для обновления меню по id
        """
        return await update_menu(menu_id)

    @app.delete('api/v1/menus/{menu_id}')
    async def delete_menu_by_urlname(cls, menu_id: UUID) -> dict:
        """
        Вызов роута для удаления меню по id
        """
        return await delete_menu(menu_id)
