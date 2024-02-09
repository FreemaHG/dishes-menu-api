from fastapi_redis import redis_client
from loguru import logger

from src.models.submenu import Submenu
from src.redis import redis


class SubmenusListCacheRepository:
    """
    Проверка и добавление записей о списке подменю в кэш
    """
    __submenus_list = 'menu_{menu_id}_submenus_list'

    @classmethod
    async def get_list(cls, menu_id: str) -> list | None:
        """
        Метод проверяет в кэше записи о списке подменю
        :param menu_id: id меню
        :return: словарь с данными, если есть кэш, иначе None
        """
        return await redis_client.get(cls.__submenus_list.format(menu_id=menu_id))

    @classmethod
    async def set_list(cls, menu_id: str, submenus_list: list[Submenu]) -> None:
        """
        Метод записывает в кэш данные о списке подменю
        :param menu_id: id меню
        :param submenus_list: список с подменю
        :return: None
        """
        await redis_client.set(
            cls.__submenus_list.format(menu_id=menu_id),
            [submenu.as_dict() for submenu in submenus_list]
        )
        logger.info('Список подменю кэширован')

    @classmethod
    def delete_list(cls, menu_id: str) -> None:
        """
        Метод очищает кэш со списком подменю
        :param menu_id: id меню, к которому относится подменю
        :return: None
        """
        redis.delete(cls.__submenus_list.format(menu_id=menu_id))
        logger.info('Кэш списка подменю очищен')


class SubmenuCacheRepository:
    """
    Проверка и добавление записей о подменю в кэш
    """
    __submenu_id = 'submenu_{submenu_id}'

    @classmethod
    async def get(cls, submenu_id: str) -> dict | None:
        """
        Метод проверяет в кэше запись о меню
        :param submenu_id: id подменю
        :return: словарь с данными, если есть кэш, иначе None
        """
        return await redis_client.get(cls.__submenu_id.format(submenu_id=submenu_id))

    @classmethod
    async def set(cls, submenu: Submenu) -> None:
        """
        Метод записывает в кэш данные о меню
        :param submenu: объект подменю
        :return: None
        """
        await redis_client.set(cls.__submenu_id.format(submenu_id=submenu.id), submenu.as_dict())
        logger.info('Данные о подменю кэшированы')

    @classmethod
    def delete(cls, submenu_id: str) -> None:
        """
        Метод очищает кэш с данными о подменю
        :param submenu_id: id подменю
        :return: None
        """
        redis.delete(cls.__submenu_id.format(submenu_id=submenu_id))
        logger.info('Кэш подменю очищен')
