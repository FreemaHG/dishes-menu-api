from src.models.menu import Menu
from src.repositories.cache.dish import DishCacheRepository, DishesListCacheRepository
from src.repositories.cache.menu import MenuCacheRepository, MenusListCacheRepository
from src.repositories.cache.submenu import (
    SubmenuCacheRepository,
    SubmenusListCacheRepository,
)


class DeleteCacheMenuService:
    """
    Класс используется для очистки кэша при удалении меню
    """

    @classmethod
    def delete_menu(cls, menu: Menu) -> None:
        """
        Метод очищает кэш списка меню и конкретного меню
        :param menu: удаляемое меню
        :return: None
        """
        MenusListCacheRepository.delete_list()
        MenuCacheRepository.delete(menu_id=menu.id)


class CascadeDeleteCacheMenuService(DeleteCacheMenuService):
    """
    Класс для каскадного удаления кэша связанных записей подменю и блюд при удалении меню
    """

    @classmethod
    def delete_menu(cls, menu: Menu) -> None:
        """
        Метод каскадно очищает кэш для всех подменю и блюд, относящихся к удаляемому меню
        :param menu: удаляемое меню
        :return: None
        """
        super().delete_menu(menu=menu)

        # Очистка кэша списка подменю и всех подменю, которые относятся к удаляемому меню
        SubmenusListCacheRepository.delete_list(menu_id=menu.id)

        for submenu in menu.submenus:
            SubmenuCacheRepository.delete(submenu_id=submenu.id)

            # Очистка кэша списка блюд и всех блюд, которые относятся к удаляемому подменю
            DishesListCacheRepository.delete_list(submenu_id=submenu.id)

            for dish in submenu.dishes:
                DishCacheRepository.delete(dish_id=dish.id)
