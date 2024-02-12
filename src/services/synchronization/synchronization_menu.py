import asyncio
import os

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import PATH
from src.database import async_session_maker
from src.repositories.dish import DishRepository
from src.repositories.menu import MenuRepository
from src.repositories.submenu import SubmenuRepository
from src.repositories.synchronization.last_change_time import LastChangeFileRepository
from src.schemas.base import BaseInSchema
from src.schemas.parser.dish import DishParserSchema
from src.services.all_data import AllDataService
from src.services.synchronization.check import CheckDataService
from src.utils.parser.write_parsed_data import write_data_to_json


class DataSynchronizationService:
    """
    Сервис для синхронизации данных о меню, подменю и блюдам между БД и exel-файлом
    """
    __FILE = 'Menu.xlsx'
    __PATH = os.path.abspath(os.path.join(PATH, 'admin', __FILE))

    @classmethod
    async def _dish(cls, submenu_id: str, dishes: list[dict], session: AsyncSession) -> None:
        """
        Метод добавляет в БД записи о блюдах
        :param submenu_id: id подменю, к которому относятся блюда
        :param dishes: список блюд
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """
        for dish in dishes:
            dish_data = DishParserSchema(**dish)
            await DishRepository.create(
                submenu_id=submenu_id,
                new_dish=dish_data,
                session=session
            )

    @classmethod
    async def _submenu(cls, menu_id: str, submenus: list[dict], session: AsyncSession):
        """
        Метод добавляет в БД записи о подменю
        :param menu_id: id меню, к которому относятся подменю
        :param submenus: список подменю
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """
        if submenus and len(submenus) > 0:
            for submenu in submenus:
                submenu_data = BaseInSchema(**submenu)
                submenu_id = await SubmenuRepository.create(
                    menu_id=menu_id,
                    new_submenu=submenu_data,
                    session=session
                )

                dishes = submenu.get('dishes', None)

                if dishes and len(dishes) > 0:
                    await cls._dish(submenu_id=submenu_id, dishes=dishes, session=session)

    @classmethod
    async def _menu(cls, menus: list[dict], session: AsyncSession):
        """
        Метод добавляет в БД записи о меню
        :param menus: список меню
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """

        for menu in menus:
            menu_data = BaseInSchema(**menu)
            menu_id = await MenuRepository.create(new_menu=menu_data, session=session)

            submenus = menu.get('submenus', None)

            if submenus and len(submenus) > 0:
                await cls._submenu(menu_id=menu_id, submenus=submenus, session=session)

    @classmethod
    async def synchronization_db(cls) -> None:
        """
        Основной метод для синхронизации БД с exel-файлом
        :return: None
        """
        data = await CheckDataService.check_file(file=cls.__PATH)

        if not data:
            logger.warning('Синхронизация данных не проведена')

        else:
            write_path = cls.__PATH.replace(cls.__FILE, '')
            await write_data_to_json(data=data, path=write_path)

            await AllDataService.delete_all_data()

            menus = data.get('menus', None)

            if menus and len(menus) > 0:
                async with async_session_maker() as session:
                    await cls._menu(menus=menus, session=session)

                logger.debug('Синхронизация данных завершена')
            else:
                logger.warning('Файл синхронизации пуст. БД очищена')

            await LastChangeFileRepository.set(timestamp_data=data['time_change_file'])


# TODO ДЛЯ ПРОВЕРКИ
if __name__ == '__main__':
    asyncio.run(DataSynchronizationService.synchronization_db())
