from fastapi import BackgroundTasks
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.dish import Dish
from src.repositories.cache.dish import DishCacheRepository, DishesListCacheRepository
from src.repositories.dish import DishRepository
from src.repositories.menu import MenuRepository
from src.repositories.submenu import SubmenuRepository
from src.schemas.base import BaseInOptionalSchema
from src.schemas.dish import DishInSchema
from src.services.cache.dish import (
    CascadeDeleteCacheDishService,
    DeleteCacheDishService,
)


class DishService:
    """
    Сервис для вывода списка блюд, создания, обновления и удаления блюд
    """

    @classmethod
    async def get_dishes_list(cls, submenu_id: str, session: AsyncSession) -> list[Dish] | None:
        """
        Метод кэширует и возвращает данные об имеющихся блюдах
        :param submenu_id: id подменю
        :param session: объект асинхронной сессии
        :return: список с блюдами
        """
        cache = await DishesListCacheRepository.get_list(submenu_id=submenu_id)

        if cache:
            logger.debug(f'Данные из кэша: {cache}')
            return cache

        logger.debug('Запрос данных из БД')
        dishes_list = await DishRepository.get_list(submenu_id=submenu_id, session=session)
        await DishesListCacheRepository.set_list(submenu_id=submenu_id, dishes_list=dishes_list)

        return dishes_list

    @classmethod
    async def create(
            cls,
            submenu_id: str,
            new_dish: DishInSchema,
            background_tasks: BackgroundTasks,
            session: AsyncSession
    ) -> Dish | bool:
        """
        Метод создает и возвращает новое блюдо и очищает кэш со списком меню, подменю и блюд
        :param menu_id: id меню, к которому относится блюдо (не передается ч/з swagger)
        :param submenu_id: id подменю, к которому относится блюдо
        :param new_dish: валидные данные для создания нового блюда
        :param session: объект асинхронной сессии
        :return: объект нового блюда
        """
        submenu = await SubmenuRepository.get(submenu_id=submenu_id, session=session)

        if submenu:
            dish = await DishRepository.create(submenu_id=submenu_id, new_dish=new_dish, session=session)
            menu = await MenuRepository.get(menu_id=submenu.menu_id, session=session)

            # Обязательно передаем объекты меню и подменю, а не id,
            # т.к. из них выбираются id связанных записей для корректной очистки кэша!
            background_tasks.add_task(
                CascadeDeleteCacheDishService.delete_dish, dish=dish, menu=menu, submenu=submenu
            )

            return dish

        return False

    @classmethod
    async def get(cls, dish_id: str, session: AsyncSession) -> Dish | dict | None:
        """
        Метод кэширует данные и возвращает блюдо по переданному id
        :param dish_id: id блюда для поиска
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект блюда либо None
        """
        cache = await DishCacheRepository.get(dish_id=dish_id)

        if cache:
            logger.debug(f'Данные из кэша: {cache}')
            return cache

        logger.debug('Запрос данных из БД')
        dish = await DishRepository.get(dish_id=dish_id, session=session)

        if dish:
            await DishCacheRepository.set(dish=dish)

        return dish

    @classmethod
    async def update(
            cls,
            dish_id: str,
            data: BaseInOptionalSchema,
            background_tasks: BackgroundTasks,
            session: AsyncSession
    ) -> Dish | bool:
        """
        Метод обновляет блюдо по переданному id, очищает кэш со списком меню, подменю и блюд
        :param dish_id: id блюда для обновления
        :param data: данные для обновления блюда
        :param session: объект асинхронной сессии для запросов к БД
        :return: обновленное блюдо либо None
        """
        await DishRepository.update(dish_id=dish_id, data=data, session=session)
        updated_dish = await DishRepository.get(dish_id=dish_id, session=session)

        if updated_dish:
            background_tasks.add_task(DeleteCacheDishService.delete_dish, dish=updated_dish)

            logger.info('Блюдо обновлено')
            return updated_dish

        else:
            logger.error('Блюдо не найдено!')
            return False

    @classmethod
    async def delete(cls, dish_id: str, background_tasks: BackgroundTasks, session: AsyncSession) -> bool:
        """
        Метод удаляет и очищает кэш блюда по переданному id
        :param menu_id: id меню для очистки кэша (не передается ч/з swagger)
        :param dish_id: id блюда для удаления
        :param session: объект асинхронной сессии для запросов к БД
        :return: True - успешное удаление, иначе False
        """
        delete_dish = await DishRepository.get(dish_id=dish_id, session=session)

        if delete_dish:
            submenu = await SubmenuRepository.get(submenu_id=delete_dish.submenu_id, session=session)
            menu = await MenuRepository.get(menu_id=submenu.menu_id, session=session)

            # Обязательно передаем объекты меню и подменю, а не id,
            # т.к. из них выбираются id связанных записей для корректной очистки кэша!
            background_tasks.add_task(
                CascadeDeleteCacheDishService.delete_dish, dish=delete_dish, menu=menu, submenu=submenu
            )

            await DishRepository.delete(dish_id=dish_id, session=session)

            logger.info('Блюдо удалено')
            return True

        logger.error('Блюдо не найдено!')
        return False
