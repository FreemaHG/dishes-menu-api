from fastapi_redis import redis_client
from loguru import logger

from src.models.dish import Dish


class DishesListCacheRepository:
    """
    Проверка и добавление записей о списке блюд в кэш
    """
    __dishes_list = 'submenu_{submenu_id}_dishes_list'

    @classmethod
    async def get_list(cls, submenu_id: str) -> list | None:
        """
        Метод проверяет в кэше записи о списке блюд
        :param submenu_id: id подменю
        :return: словарь с данными, если есть кэш, иначе None
        """
        return await redis_client.get(cls.__dishes_list.format(submenu_id=submenu_id))

    @classmethod
    async def set_list(cls, submenu_id: str, dishes_list: list[Dish]) -> None:
        """
        Метод записывает в кэш данные о списке блюд
        :param submenu_id: id подменю
        :param submenus_list: список с блюдами
        :return: None
        """
        await redis_client.set(
            cls.__dishes_list.format(submenu_id=submenu_id),
            [dish.as_dict() for dish in dishes_list]
        )
        logger.info('Список блюд кэширован')

    @classmethod
    async def delete_list(cls, submenu_id: str) -> None:
        """
        Метод очищает кэш со списком блюд
        :param submenu_id: id подменю, к которому относятся блюда
        :return: None
        """
        await redis_client.delete(cls.__dishes_list.format(submenu_id=submenu_id))
        logger.info('Кэш списка блюд очищен')


class DishCacheRepository:
    """
    Проверка и добавление записей о блюде в кэш
    """
    __dish_id = 'dish_{dish_id}'

    @classmethod
    async def get(cls, dish_id: str) -> dict | None:
        """
        Метод проверяет в кэше запись о блюде
        :param dish_id: id блюда
        :return: словарь с данными, если есть кэш, иначе None
        """
        return await redis_client.get(cls.__dish_id.format(dish_id=dish_id))

    @classmethod
    async def set(cls, dish: Dish) -> None:
        """
        Метод записывает в кэш данные о блюде
        :param dish: объект блюда
        :return: None
        """
        await redis_client.set(cls.__dish_id.format(dish_id=dish.id), dish.as_dict())
        logger.info('Данные о блюде кэшированы')

    @classmethod
    async def delete(cls, dish_id: str) -> None:
        """
        Метод очищает кэш с данными о блюде
        :param dish_id: id блюда
        :return: None
        """
        await redis_client.delete(cls.__dish_id.format(dish_id=dish_id))
        logger.info('Кэш блюда очищен')
