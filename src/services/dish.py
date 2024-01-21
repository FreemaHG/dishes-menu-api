from typing import Union, List
from uuid import UUID

from loguru import logger
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.dish import Dish
from src.schemas.dish import DishInSchema


class DishService:
    """
    Сервис для вывода списка блюд, создания, обновления и удаления блюда
    """

    @classmethod
    async def get_list(cls, submenu_id: UUID, session: AsyncSession) -> List[Dish]:
        """
        Метод возвращает список с блюдами
        :param submenu_id: id подменю, к которому относятся блюда
        :param session: объект асинхронной сессии для запросов к БД
        :return: список с объектами блюд
        """
        query = select(Dish).where(Dish.submenu_id == submenu_id)
        res = await session.execute(query)
        dishes_list = res.scalars().all()

        return list(dishes_list)


    @classmethod
    async def create(cls, submenu_id: UUID, new_dish: DishInSchema, session: AsyncSession) -> Union[Dish, False]:
        """
        Метод создает и возвращает новое блюдо
        :param submenu_id: id подменю, к которому относится блюдо
        :param new_dish: параметры для сохранения нового блюда
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект нового блюда
        """
        dish = Dish(
            title=new_dish.title,
            description=new_dish.description,
            price=new_dish.price,
            submenu_id=submenu_id
        )

        session.add(dish)
        await session.commit()

        return dish


    @classmethod
    async def get(cls, dish_id: UUID, session: AsyncSession) -> Union[Dish, None]:
        """
        Метод возвращает блюдо по переданному id
        :param dish_id: id блюда для поиска
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект блюда либо None
        """
        query = select(Dish).where(Dish.id == dish_id)
        submenu = await session.execute(query)

        return submenu.scalar_one_or_none()


    @classmethod
    async def update(cls, dish_id: UUID, data: DishInSchema, session: AsyncSession) -> None:
        """
        Метод обновляет блюдо по переданному id
        :param dish_id: id блюда для обновления
        :param data: параметры для сохранения нового блюда
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """
        # model_dump(exclude_unset=True) - распаковывает явно переданные поля в patch-запросе
        query = update(Dish).where(Dish.id == dish_id).values(data.model_dump(exclude_unset=True))
        await session.execute(query)
        await session.commit()


    @classmethod
    async def delete(cls, dish_id: UUID, session: AsyncSession) -> None:
        """
        Метод удаляет блюдо по переданному id
        :param dish_id: id блюда для поиска
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """
        query = delete(Dish).where(Dish.id == dish_id)
        await session.execute(query)
        await session.commit()
