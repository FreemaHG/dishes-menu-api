from src.models.menu import Menu
from src.models.submenu import Submenu
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
    def delete_submenu(cls, submenu: Submenu) -> None:
        """
        Метод очищает кэш списка подменю и конкретного подменю
        :param submenu: удаляемое подменю
        :return: None
        """
        SubmenusListCacheRepository.delete_list(menu_id=submenu.menu_id)
        SubmenuCacheRepository.delete(submenu_id=submenu.id)


class CascadeDeleteCacheSubmenuService(DeleteCacheSubmenuService):
    """
    Класс для каскадного удаления кэша связанных записей меню и блюд при удалении подменю
    """

    @classmethod
    def delete_submenu(cls, submenu: Submenu, menu: Menu | None = None) -> None:
        """
        Метод для каскадного удаления кэша связанных записей меню и блюд при удалении подменю
        :param menu: меню, к которому относится удаляемое подменю
        :param submenu: удаляемое подменю
        :return: None
        """
        super().delete_submenu(submenu=submenu)

        if menu:
            DeleteCacheMenuService.delete_menu(menu=menu)

        DishesListCacheRepository.delete_list(submenu_id=submenu.id)

        for dish in submenu.dishes:
            DishCacheRepository.delete(dish_id=dish.id)
