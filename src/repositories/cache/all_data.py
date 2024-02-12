from fastapi_redis import redis_client
from loguru import logger

from src.models.menu import Menu


class AllDataCacheRepository:
    """
    Проверка и добавление записей о меню со всеми связанными подменю и со всеми связанными блюдами в кэш
    """
    __all_data = 'all_data'

    @classmethod
    async def get_data(cls) -> list | None:
        """
        Метод проверяет в кэше записи о всех данных
        :return: словарь с данными, если есть кэш, иначе None
        """
        return await redis_client.get(cls.__all_data)

    @classmethod
    async def set_data(cls, menus_list: list[Menu]) -> None:
        """
        Метод записывает в кэш данные о всех записях
        :param menus_list: список с меню
        :return: None
        """
        await redis_client.set(cls.__all_data, [menu.as_all_dict() for menu in menus_list])
        logger.info('Все данные кэшированы')

    @classmethod
    async def delete_data(cls) -> None:
        """
        Метод очищает кэш со списком меню
        :return: None
        """
        await redis_client.delete(cls.__all_data)
        logger.info('Кэш со всеми данными очищен')
