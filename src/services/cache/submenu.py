from src.models.menu import Menu
from src.models.submenu import Submenu
from src.repositories.cache.all_data import AllDataCacheRepository
from src.repositories.cache.dish import DishCacheRepository, DishesListCacheRepository
from src.repositories.cache.submenu import (
    SubmenuCacheRepository,
    SubmenusListCacheRepository,
)
from src.services.cache.menu import DeleteCacheMenuService


class DeleteCacheSubmenuService:
    """
    Класс используется для очистки кэша при удалении подменю
    """

    @classmethod
    async def delete_submenu(cls, submenu: Submenu) -> None:
        """
        Метод очищает кэш списка подменю и конкретного подменю
        :param submenu: удаляемое подменю
        :return: None
        """
        await SubmenusListCacheRepository.delete_list(menu_id=submenu.menu_id)
        await SubmenuCacheRepository.delete(submenu_id=submenu.id)
        await AllDataCacheRepository.delete_data()


class CascadeDeleteCacheSubmenuService(DeleteCacheSubmenuService):
    """
    Класс для каскадного удаления кэша связанных записей меню и блюд при удалении подменю
    """

    @classmethod
    async def delete_submenu(cls, submenu: Submenu, menu: Menu | None = None) -> None:
        """
        Метод для каскадного удаления кэша связанных записей меню и блюд при удалении подменю
        :param menu: меню, к которому относится удаляемое подменю
        :param submenu: удаляемое подменю
        :return: None
        """
        await super().delete_submenu(submenu=submenu)

        if menu:
            await DeleteCacheMenuService.delete_menu(menu=menu)

        await DishesListCacheRepository.delete_list(submenu_id=submenu.id)

        for dish in submenu.dishes:
            await DishCacheRepository.delete(dish_id=dish.id)
