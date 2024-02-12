from fastapi_redis import redis_client


class LastChangeFileRepository:
    """
    Чтение и сохранение последнего изменения файла для синхронизации данных в БД
    """
    __KEY = 'last_change_time'

    @classmethod
    async def get(cls) -> int:
        """
        Метод выводит последнее записанное timestamp-время изменения файла для синхронизации
        :return: timestamp
        """
        return await redis_client.get(cls.__KEY)

    @classmethod
    async def set(cls, timestamp_data: int) -> None:
        """
        Метод записывает timestamp-время изменения файла при синхронизации
        :return: None
        """
        await redis_client.set(cls.__KEY, timestamp_data)
