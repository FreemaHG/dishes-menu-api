from fastapi_redis import redis_client
from loguru import logger

from src.models.menu import Menu
from src.redis import redis


class MenusListCacheRepository:
    """
    Проверка и добавление записей о списке меню в кэш
    """
    __menus_list = 'menus_list'

    @classmethod
    async def get_list(cls) -> list | None:
        """
        Метод проверяет в кэше записи о списке меню
        :return: словарь с данными, если есть кэш, иначе None
        """
        return await redis_client.get(cls.__menus_list)

    @classmethod
    async def set_list(cls, menus_list: list[Menu]) -> None:
        """
        Метод записывает в кэш данные о списке меню
        :param menus_list: список с меню
        :return: None
        """
        await redis_client.set(cls.__menus_list, [menu.as_dict() for menu in menus_list])
        logger.info('Список меню кэширован')

    @classmethod
    def delete_list(cls) -> None:
        """
        Метод очищает кэш со списком меню
        :return: None
        """
        redis.delete(cls.__menus_list)
        logger.info('Кэш списка меню очищен')


class MenuCacheRepository:
    """
    Проверка и добавление записей о меню в кэш
    """
    __menu_id = 'menu_{menu_id}'

    @classmethod
    async def get(cls, menu_id: str) -> dict | None:
        """
        Метод проверяет в кэше запись о меню
        :param menu_id: id меню
        :return: словарь с данными, если есть кэш, иначе None
        """
        return await redis_client.get(cls.__menu_id.format(menu_id=menu_id))

    @classmethod
    async def set(cls, menu: Menu) -> None:
        """
        Метод записывает в кэш данные о меню
        :param menu: объект меню
        :return: None
        """
        await redis_client.set(cls.__menu_id.format(menu_id=menu.id), menu.as_dict())
        logger.info('Данные о меню кэшированы')

    @classmethod
    def delete(cls, menu_id: str) -> None:
        """
        Метод очищает кэш с данными о меню
        :param menu_id: id меню
        :return: None
        """
        redis.delete(cls.__menu_id.format(menu_id=menu_id))
        logger.info('Кэш меню очищен')
