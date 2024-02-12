from src.models.dish import Dish
from src.models.menu import Menu
from src.models.submenu import Submenu
from src.repositories.cache.all_data import AllDataCacheRepository
from src.repositories.cache.dish import DishCacheRepository, DishesListCacheRepository
from src.services.cache.menu import DeleteCacheMenuService
from src.services.cache.submenu import DeleteCacheSubmenuService


class DeleteCacheDishService:
    """
    Класс используется для очистки кэша при удалении блюда
    """

    @classmethod
    async def delete_dish(cls, dish: Dish) -> None:
        """
        Метод очищает кэш списка блюд и конкретного блюда
        :param menu: удаляемое блюдо
        :return: None
        """
        await DishesListCacheRepository.delete_list(submenu_id=dish.submenu_id)
        await DishCacheRepository.delete(dish_id=dish.id)
        await AllDataCacheRepository.delete_data()


class CascadeDeleteCacheDishService(DeleteCacheDishService):
    """
    Класс для каскадного удаления кэша связанных записей меню и подменю при удалении блюда
    """

    @classmethod
    async def delete_dish(cls, dish: Dish, menu: Menu | None = None, submenu: Submenu | None = None) -> None:
        """
        Метод для каскадного удаления кэша связанных записей меню и подменю при удалении блюда
        :param dish: удаляемое блюдо
        :param submenu: подменю, в котором находится блюдо
        :param menu: меню, в котором находится блюдо
        :return:
        """
        await super().delete_dish(dish=dish)

        if menu and submenu:
            await DeleteCacheSubmenuService.delete_submenu(submenu=submenu)
            await DeleteCacheMenuService.delete_menu(menu=menu)
