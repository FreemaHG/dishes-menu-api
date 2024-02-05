from fastapi_redis import redis_client
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.submenu import Submenu
from src.repositories.submenu import SubmenuRepository
from src.schemas.base import BaseInOptionalSchema, BaseInSchema
from src.services.menu import MenuService


class SubmenuService:
    """
    Сервис для вывода списка меню, создания, обновления и удаления меню
    """

    @classmethod
    async def get_submenus_list(cls, menu_id: str, session: AsyncSession) -> list[Submenu]:
        """
        Метод кэширует и возвращает данные об имеющихся меню
        :param menu_id: id меню
        :param session: объект асинхронной сессии
        :return: список с меню
        """
        cache = await redis_client.get(f'menu_{menu_id}_submenus_list')

        if cache:
            logger.debug(f'Данные из кэша: {cache}')
            return cache

        logger.debug('Запрос данных из БД')
        submenus_list = await SubmenuRepository.get_list(menu_id=menu_id, session=session)

        await redis_client.set(f'menu_{menu_id}_submenus_list', [submenu.as_dict() for submenu in submenus_list])
        logger.info('Данные кэшированы')

        return submenus_list

    @classmethod
    async def create(cls, menu_id: str, new_submenu: BaseInSchema, session: AsyncSession) -> Submenu | None | bool:
        """
        Метод создает и возвращает новое меню и очищает кэш со списком меню
        :param new_menu: валидные данные для создания нового подменю
        :param session: объект асинхронной сессии
        :return: объект нового подменю
        """
        menu = await MenuService.get(menu_id=menu_id, session=session)

        if menu:
            # Делаем два запроса, чтобы при первом создании подменю не было ошибки при выводе связанных данных
            # (которых еще нет) из дочерних таблиц
            submenu_id = await SubmenuRepository.create(
                menu_id=menu_id, new_submenu=new_submenu, session=session
            )
            submenu = await SubmenuRepository.get(submenu_id=submenu_id, session=session)

            await redis_client.delete(f'menu_{menu_id}_submenus_list')
            await redis_client.delete('menus_list')
            await redis_client.delete(f'menu_{menu_id}')

            return submenu

        return False

    @classmethod
    async def get(cls, submenu_id: str, session: AsyncSession) -> Submenu | None:
        """
        Метод кэширует данные и возвращает подменю по переданному id
        :param submenu_id: id подменю для поиска
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект подменю либо None
        """
        cache = await redis_client.get(f'submenu_{submenu_id}')

        if cache:
            logger.debug(f'Данные из кэша: {cache}')
            return cache

        logger.debug('Запрос данных из БД')
        submenu = await SubmenuRepository.get(submenu_id=submenu_id, session=session)

        if submenu:
            await redis_client.set(f'submenu_{submenu_id}', submenu.as_dict())
            logger.info('Данные кэшированы')

        return submenu

    @classmethod
    async def update(cls, submenu_id: str, data: BaseInOptionalSchema, session: AsyncSession) -> Submenu | bool:
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
            await redis_client.delete(f'menu_{updated_submenu.menu_id}_submenus_list')
            await redis_client.delete(f'submenu_{submenu_id}')

            logger.info('Подменю обновлено')
            return updated_submenu

        else:
            logger.error('Подменю не найдено!')
            return False

    @classmethod
    async def delete(cls, submenu_id: str, session: AsyncSession) -> bool:
        """
        Метод удаляет и очищает кэш подменю по переданному id
        :param submenu_id: id подменю для удаления
        :param session: объект асинхронной сессии для запросов к БД
        :return: True - успешное удаление, иначе False
        """
        delete_submenu = await SubmenuRepository.get(submenu_id=submenu_id, session=session)

        if delete_submenu:
            await SubmenuRepository.delete(delete_submenu=delete_submenu, session=session)

            await redis_client.delete(f'submenu_{delete_submenu.id}_dishes_list')
            await redis_client.delete(f'menu_{delete_submenu.menu_id}_submenus_list')
            await redis_client.delete('menus_list')
            await redis_client.delete(f'submenu_{submenu_id}')
            await redis_client.delete(f'menu_{delete_submenu.menu_id}')

            # Очистка кэша для всех блюд в подменю
            for dish in delete_submenu.dishes:
                await redis_client.delete(f'dish_{dish.id}')

            logger.info('Подменю удалено')
            return True

        logger.error('Подменю не найдено!')
        return False
