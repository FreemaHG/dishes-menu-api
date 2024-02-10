from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.menu import Menu
from src.repositories.cache.all_data import AllDataCacheRepository
from src.repositories.menu import MenuRepository


class AllDataService:
    """
    Сервис для вывода списка меню со всеми связанными подменю и со всеми связанными блюдами
    """

    @classmethod
    async def get_all_data(cls, session: AsyncSession) -> list[Menu] | None:
        """
        Метод кэширует и возвращает данные об имеющихся меню со всеми связанными данными по подменю и блюдами
        :param session: объект асинхронной сессии
        :return: список с меню
        """

        cache = await AllDataCacheRepository.get_data()

        if cache:
            logger.debug(f'Данные из кэша: {cache}')
            return cache

        logger.debug('Запрос данных из БД')
        menus_list = await MenuRepository.get_list(session=session)

        await AllDataCacheRepository.set_data(menus_list=menus_list)

        return menus_list
