from fastapi import BackgroundTasks
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.submenu import Submenu
from src.repositories.cache.submenu import (
    SubmenuCacheRepository,
    SubmenusListCacheRepository,
)
from src.repositories.menu import MenuRepository
from src.repositories.submenu import SubmenuRepository
from src.schemas.base import BaseInOptionalSchema, BaseInSchema
from src.services.cache.menu import DeleteCacheMenuService
from src.services.cache.submenu import (
    CascadeDeleteCacheSubmenuService,
    DeleteCacheSubmenuService,
)


class SubmenuService:
    """
    Сервис для вывода списка меню, создания, обновления и удаления меню
    """

    @classmethod
    async def get_submenus_list(cls, menu_id: str, session: AsyncSession) -> list[Submenu] | None:
        """
        Метод кэширует и возвращает данные об имеющихся меню
        :param menu_id: id меню
        :param session: объект асинхронной сессии
        :return: список с меню
        """
        cache = await SubmenusListCacheRepository.get_list(menu_id=menu_id)

        if cache:
            logger.debug(f'Данные из кэша: {cache}')
            return cache

        logger.debug('Запрос данных из БД')
        submenus_list = await SubmenuRepository.get_list(menu_id=menu_id, session=session)

        await SubmenusListCacheRepository.set_list(menu_id=menu_id, submenus_list=submenus_list)

        return submenus_list

    @classmethod
    async def create(
            cls,
            menu_id: str,
            new_submenu: BaseInSchema,
            background_tasks: BackgroundTasks,
            session: AsyncSession
    ) -> Submenu | None | bool:
        """
        Метод создает и возвращает новое меню и очищает кэш со списком меню
        :param new_menu: валидные данные для создания нового подменю
        :param session: объект асинхронной сессии
        :return: объект нового подменю
        """
        menu = await MenuRepository.get(menu_id=menu_id, session=session)

        if menu:
            # Делаем два запроса, чтобы при первом создании подменю не было ошибки при выводе связанных данных
            # (которых еще нет) из дочерних таблиц
            submenu_id = await SubmenuRepository.create(
                menu_id=menu_id, new_submenu=new_submenu, session=session
            )
            submenu = await SubmenuRepository.get(submenu_id=submenu_id, session=session)

            background_tasks.add_task(DeleteCacheMenuService.delete_menu, menu=menu)
            background_tasks.add_task(SubmenusListCacheRepository.delete_list, menu_id=menu.id)

            return submenu

        return False

    @classmethod
    async def get(cls, submenu_id: str, session: AsyncSession) -> Submenu | dict | None:
        """
        Метод кэширует данные и возвращает подменю по переданному id
        :param submenu_id: id подменю для поиска
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект подменю либо None
        """
        cache = await SubmenuCacheRepository.get(submenu_id=submenu_id)

        if cache:
            logger.debug(f'Данные из кэша: {cache}')
            return cache

        logger.debug('Запрос данных из БД')
        submenu = await SubmenuRepository.get(submenu_id=submenu_id, session=session)

        if submenu:
            await SubmenuCacheRepository.set(submenu=submenu)

        return submenu

    @classmethod
    async def update(
            cls,
            submenu_id: str,
            data: BaseInOptionalSchema,
            background_tasks: BackgroundTasks,
            session: AsyncSession
    ) -> Submenu | bool:
        """
        Метод обновляет подменю по переданному id, очищает кэш списка подменю
        :param submenu_id: id подменю для обновления
        :param data: данные для обновления подменю
        :param session: объект асинхронной сессии для запросов к БД
        :return: обновленное подменю либо None
        """
        await SubmenuRepository.update(submenu_id=submenu_id, data=data, session=session)
        updated_submenu = await SubmenuRepository.get(submenu_id=submenu_id, session=session)

        if updated_submenu:
            background_tasks.add_task(DeleteCacheSubmenuService.delete_submenu, submenu=updated_submenu)
            logger.info('Подменю обновлено')

            return updated_submenu

        else:
            logger.error('Подменю не найдено!')
            return False

    @classmethod
    async def delete(cls, submenu_id: str, background_tasks: BackgroundTasks, session: AsyncSession) -> bool:
        """
        Метод удаляет и очищает кэш подменю по переданному id
        :param submenu_id: id подменю для удаления
        :param session: объект асинхронной сессии для запросов к БД
        :return: True - успешное удаление, иначе False
        """
        delete_submenu = await SubmenuRepository.get(submenu_id=submenu_id, session=session)

        if delete_submenu:
            menu = await MenuRepository.get(menu_id=delete_submenu.menu_id, session=session)

            background_tasks.add_task(
                CascadeDeleteCacheSubmenuService.delete_submenu, menu=menu, submenu=delete_submenu
            )

            await SubmenuRepository.delete(delete_submenu=delete_submenu, session=session)
            logger.info('Подменю удалено')

            return True

        logger.error('Подменю не найдено!')

        return False
