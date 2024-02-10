from fastapi import BackgroundTasks
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.menu import Menu
from src.repositories.cache.all_data import AllDataCacheRepository
from src.repositories.cache.menu import MenuCacheRepository, MenusListCacheRepository
from src.repositories.menu import MenuRepository
from src.schemas.base import BaseInOptionalSchema, BaseInSchema
from src.services.cache.menu import (
    CascadeDeleteCacheMenuService,
    DeleteCacheMenuService,
)


class MenuService:
    """
    Сервис для вывода списка меню, создания, обновления и удаления меню
    """

    @classmethod
    async def get_menus_list(cls, session: AsyncSession) -> list[Menu] | None:
        """
        Метод кэширует и возвращает данные об имеющихся меню
        :param session: объект асинхронной сессии
        :return: список с меню
        """
        cache = await MenusListCacheRepository.get_list()

        if cache:
            logger.debug(f'Данные из кэша: {cache}')
            return cache

        logger.debug('Запрос данных из БД')
        menus_list = await MenuRepository.get_list(session=session)

        await MenusListCacheRepository.set_list(menus_list=menus_list)

        return menus_list

    @classmethod
    async def create(
            cls,
            new_menu: BaseInSchema,
            background_tasks: BackgroundTasks,
            session: AsyncSession
    ) -> Menu | None:
        """
        Метод создает и возвращает новое меню, очищает кэш со списком меню
        :param new_menu: валидные данные для создания нового меню
        :param session: объект асинхронной сессии
        :return: объект нового меню
        """
        menu_id = await MenuRepository.create(new_menu=new_menu, session=session)
        menu = await MenuRepository.get(menu_id=menu_id, session=session)

        background_tasks.add_task(MenusListCacheRepository.delete_list)
        background_tasks.add_task(AllDataCacheRepository.delete_data)

        return menu

    @classmethod
    async def get(cls, menu_id: str, session: AsyncSession) -> Menu | dict | None:
        """
        Метод кэширует данные и возвращает меню по переданному id
        :param menu_id: id меню для поиска
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект меню либо None
        """
        cache = await MenuCacheRepository.get(menu_id=menu_id)

        if cache:
            logger.debug(f'Данные из кэша: {cache}')
            return cache

        logger.debug('Запрос данных из БД')
        menu = await MenuRepository.get(menu_id=menu_id, session=session)

        if menu:
            await MenuCacheRepository.set(menu=menu)

        return menu

    @classmethod
    async def update(
            cls,
            menu_id: str,
            data: BaseInOptionalSchema,
            background_tasks: BackgroundTasks,
            session: AsyncSession
    ) -> Menu | bool:
        """
        Метод обновляет меню по переданному id, очищает кэш списка меню
        :param menu_id: id меню для обновления
        :param data: данные для обновления меню
        :param session: объект асинхронной сессии для запросов к БД
        :return: обновленное меню либо None
        """
        await MenuRepository.update(menu_id=menu_id, data=data, session=session)
        update_menu = await MenuRepository.get(menu_id=menu_id, session=session)

        if update_menu:
            background_tasks.add_task(DeleteCacheMenuService.delete_menu, menu=update_menu)

            logger.info('Меню обновлено')
            return update_menu

        else:
            logger.error('Меню не найдено!')
            return False

    @classmethod
    async def delete(cls, menu_id: str, background_tasks: BackgroundTasks, session: AsyncSession) -> bool:
        """
        Метод удаляет и очищает кэш меню по переданному id
        :param menu_id: id меню для удаления
        :param session: объект асинхронной сессии для запросов к БД
        :return: True - успешное удаление, иначе False
        """
        delete_menu = await MenuRepository.get(menu_id=menu_id, session=session)

        if delete_menu:
            # Каскадное удаление кэша для всех связанных записей
            background_tasks.add_task(CascadeDeleteCacheMenuService.delete_menu, menu=delete_menu)

            await MenuRepository.delete(delete_menu=delete_menu, session=session)
            logger.info('Меню удалено')

            return True

        logger.error('Меню не найдено!')

        return False
