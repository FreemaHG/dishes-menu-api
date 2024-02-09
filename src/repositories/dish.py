from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.dish import Dish
from src.schemas.dish import DishInOptionalSchema, DishInSchema


class DishRepository:
    """
    Получение списка блюд, создания, обновление и удаления блюда из БД
    """

    @classmethod
    async def get_list(cls, submenu_id: str, session: AsyncSession) -> list[Dish]:
        """
        Метод возвращает список с блюдами из БД
        :param submenu_id: id подменю, к которому относятся блюда
        :param session: объект асинхронной сессии для запросов к БД
        :return: список с блюдами
        """
        query = select(Dish).where(Dish.submenu_id == submenu_id)
        res = await session.execute(query)
        dishes_list = res.scalars().all()

        return list(dishes_list)

    @classmethod
    async def create(
        cls, submenu_id: str, new_dish: DishInSchema, session: AsyncSession
    ) -> Dish:
        """
        Метод создает и возвращает новое блюдо из БД
        :param submenu_id: id подменю, к которому относится блюдо
        :param new_dish: параметры для сохранения нового блюда
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект нового блюда
        """
        dish = Dish(
            title=new_dish.title,
            description=new_dish.description,
            price=new_dish.price,
            submenu_id=submenu_id,
        )

        session.add(dish)
        await session.commit()

        return dish

    @classmethod
    async def get(cls, dish_id: str, session: AsyncSession) -> Dish:
        """
        Метод возвращает блюдо из БД по переданному id
        :param dish_id: id блюда для поиска
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект блюда либо None
        """
        query = select(Dish).where(Dish.id == dish_id)
        submenu = await session.execute(query)

        return submenu.scalar_one_or_none()

    @classmethod
    async def update(
        cls, dish_id: str, data: DishInOptionalSchema, session: AsyncSession
    ) -> None:
        """
        Метод обновляет блюдо в БД по переданному id
        :param dish_id: id блюда для обновления
        :param data: параметры для сохранения нового блюда
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """
        # model_dump(exclude_unset=True) - распаковывает явно переданные поля в patch-запросе
        query = (
            update(Dish)
            .where(Dish.id == dish_id)
            .values(data.model_dump(exclude_unset=True))
        )
        await session.execute(query)
        await session.commit()

    @classmethod
    async def delete(cls, dish_id: str, session: AsyncSession) -> None:
        """
        Метод удаляет блюдо из БД по переданному id
        :param dish_id: id блюда для поиска
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """
        query = delete(Dish).where(Dish.id == dish_id)
        await session.execute(query)
        await session.commit()
