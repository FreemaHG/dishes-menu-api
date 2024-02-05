from fastapi_redis import redis_client
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.dish import Dish
from src.repositories.dish import DishRepository
from src.repositories.submenu import SubmenuRepository
from src.schemas.base import BaseInOptionalSchema
from src.schemas.dish import DishInSchema


class DishService:
    """
    Сервис для вывода списка блюд, создания, обновления и удаления блюд
    """

    @classmethod
    async def get_dishes_list(cls, submenu_id: str, session: AsyncSession) -> list[Dish]:
        """
        Метод кэширует и возвращает данные об имеющихся блюдах
        :param submenu_id: id подменю
        :param session: объект асинхронной сессии
        :return: список с блюдами
        """
        cache = await redis_client.get(f'submenu_{submenu_id}_dishes_list')

        if cache:
            logger.debug(f'Данные из кэша: {cache}')
            return cache

        logger.debug('Запрос данных из БД')
        dishes_list = await DishRepository.get_list(submenu_id=submenu_id, session=session)

        await redis_client.set(f'submenu_{submenu_id}_dishes_list', [dish.as_dict() for dish in dishes_list])
        logger.info('Данные кэшированы')

        return dishes_list

    @classmethod
    async def create(cls, submenu_id: str, new_dish: DishInSchema, session: AsyncSession) -> Dish | bool:
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
            dish = await DishRepository.create(
                submenu_id=submenu_id, new_dish=new_dish, session=session
            )

            await redis_client.delete('menus_list')
            await redis_client.delete(f'submenu_{submenu_id}_dishes_list')
            await redis_client.delete(f'menu_{submenu.menu_id}_submenus_list')
            await redis_client.delete(f'menu_{submenu.menu_id}')

            await redis_client.delete(f'submenu_{submenu_id}')

            return dish

        return False

    @classmethod
    async def get(cls, dish_id: str, session: AsyncSession) -> Dish | None:
        """
        Метод кэширует данные и возвращает блюдо по переданному id
        :param dish_id: id блюда для поиска
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект блюда либо None
        """
        cache = await redis_client.get(f'dish_{dish_id}')

        if cache:
            logger.debug(f'Данные из кэша: {cache}')
            return cache

        logger.debug('Запрос данных из БД')
        dish = await DishRepository.get(dish_id=dish_id, session=session)

        if dish:
            await redis_client.set(f'dish_{dish_id}', dish.as_dict())
            logger.info('Данные кэшированы')

        return dish

    @classmethod
    async def update(cls, dish_id: str, data: BaseInOptionalSchema, session: AsyncSession) -> Dish | bool:
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
            await redis_client.delete(f'submenu_{updated_dish.submenu_id}_dishes_list')
            await redis_client.delete(f'dish_{dish_id}')

            logger.info('Блюдо обновлено')
            return updated_dish

        else:
            logger.error('Блюдо не найдено!')
            return False

    @classmethod
    async def delete(cls, dish_id: str, session: AsyncSession) -> bool:
        """
        Метод удаляет и очищает кэш блюда по переданному id
        :param menu_id: id меню для очистки кэша (не передается ч/з swagger)
        :param dish_id: id блюда для удаления
        :param session: объект асинхронной сессии для запросов к БД
        :return: True - успешное удаление, иначе False
        """
        delete_dish = await DishRepository.get(dish_id=dish_id, session=session)

        if delete_dish:
            # Для получения id меню для очистки кэша
            submenu = await SubmenuRepository.get(submenu_id=delete_dish.submenu_id, session=session)

            if submenu:
                await redis_client.delete(f'menu_{submenu.menu_id}')
                await redis_client.delete(f'menu_{submenu.menu_id}_submenus_list')

            await DishRepository.delete(dish_id=dish_id, session=session)
            await redis_client.delete(f'dish_{dish_id}')
            await redis_client.delete(f'submenu_{delete_dish.submenu_id}')
            await redis_client.delete(f'submenu_{delete_dish.submenu_id}_dishes_list')
            await redis_client.delete('menus_list')

            logger.info('Блюдо удалено')
            return True

        logger.error('Блюдо не найдено!')
        return False
