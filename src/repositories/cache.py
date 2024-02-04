from typing import Dict

# from src.redis import redis


# TODO Удалить?
class CachingRepository:
    """
    Репозиторий для сохранения, проверки и извлечения данных из кэша
    """

    @classmethod
    async def set(cls):
        """
        Добавление данных в кэш
        :return:
        """
        pass

    @classmethod
    async def get(cls, key: str) -> Dict | None:
        """
        Возврат данных из кэша по ключу
        :return: словарь с данными | None
        """
        return await redis.get(key)

    @classmethod
    async def delete(cls):
        """
        Удаление данных из кэша
        :return:
        """
        pass
