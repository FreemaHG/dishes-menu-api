from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_maker
from src.models.menu import Menu
from src.repositories.cache.all_data import AllDataCacheRepository
from src.repositories.menu import MenuListRepository, MenuRepository
from src.services.cache.menu import CascadeDeleteCacheMenuService


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

    @classmethod
    async def delete_all_data(cls) -> None:
        """
        Метод удаляет все данные из БД, очищает полностью кэш (используется при синхронизации пустого exel-файла с БД)
        :return: None
        """
        logger.debug('Очистка БД')

        async with async_session_maker() as session:

            # Получаем все меню из БД
            menus = await MenuRepository.get_list(session=session)

            # Удалить кэш со всеми данными
            AllDataCacheRepository.delete_data()

            # Удалить кэш каскадно для каждого меню, вложенного подменю и блюда
            for menu in menus:
                CascadeDeleteCacheMenuService.delete_menu(menu=menu)

            # Удаление всех меню
            await MenuListRepository.delete_list(session=session)

            logger.info('БД и кэш очищены')
