from uuid import UUID

from src.main import app
from src.models.dish import Dish
from src.routes.dish import (
    create_dish,
    delete_dish,
    get_dish,
    get_dishes_list,
    update_dish,
)


class DishUrl:
    """
    Методы класса имитируют функции reverse() в Django, позволяя вызывать нужный роут по urlname для блюд
    """

    @app.get('api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    async def get_dishes_list_by_urlname(cls, submenu_id: UUID) -> list[Dish]:
        """
        Вызов роута для вывода списка блюд
        """
        return await get_dishes_list(submenu_id)

    @app.post('api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    async def create_dish_by_urlname(cls, submenu_id: UUID) -> Dish:
        """
        Вызов роута для создания блюда
        """
        return await create_dish(submenu_id)

    @app.get('api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    async def get_dish_by_urlname(cls, dish_id: UUID) -> Dish:
        """
        Вызов роута для вывода блюда по id
        """
        return await get_dish(dish_id)

    @app.patch('api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    async def update_dish_by_urlname(cls, dish_id: UUID) -> Dish:
        """
        Вызов роута для обновления блюда по id
        """
        return await update_dish(dish_id)

    @app.delete('api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    async def delete_dish_by_urlname(cls, dish_id: UUID) -> dict:
        """
        Вызов роута для удаления блюда по id
        """
        return await delete_dish(dish_id)
