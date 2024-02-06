from uuid import UUID

from src.main import app
from src.models.submenu import Submenu
from src.routes.submenu import (
    create_submenu,
    delete_submenu,
    get_submenu,
    get_submenus_list,
    update_submenu,
)


class SubmenuUrl:
    """
    Методы класса имитируют функции reverse() в Django, позволяя вызывать нужный роут по urlname для подменю
    """

    @app.get('api/v1/menus/{menu_id}/submenus')
    async def get_submenus_list_by_urlname(cls, menu_id: UUID) -> list[Submenu]:
        """
        Вызов роута для вывода списка подменю
        """
        return await get_submenus_list(menu_id)

    @app.post('api/v1/menus/{menu_id}/submenus')
    async def create_submenu_by_urlname(cls, menu_id: UUID) -> Submenu:
        """
        Вызов роута для создания подменю
        """
        return await create_submenu(menu_id)

    @app.get('api/v1/menus/{menu_id}/submenus/{submenu_id}')
    async def get_submenu_by_urlname(cls, submenu_id: UUID) -> Submenu:
        """
        Вызов роута для вывода подменю по id
        """
        return await get_submenu(submenu_id)

    @app.patch('api/v1/menus/{menu_id}/submenus/{submenu_id}')
    async def update_submenu_by_urlname(cls, submenu_id: UUID) -> Submenu:
        """
        Вызов роута для обновления подменю по id
        """
        return await update_submenu(submenu_id)

    @app.delete('api/v1/menus/{menu_id}/submenus/{submenu_id}')
    async def delete_submenu_by_urlname(cls, submenu_id: UUID) -> dict:
        """
        Вызов роута для удаления подменю по id
        """
        return await delete_submenu(submenu_id)
