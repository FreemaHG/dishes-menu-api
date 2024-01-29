from typing import Union, List
from uuid import UUID
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.menu import Menu
from src.models.submenu import Submenu
from src.schemas.base import BaseInSchema, BaseInOptionalSchema


class MenuService:
    """
    Сервис для вывода списка меню, создания, обновления и удаления меню
    """

    @classmethod
    async def get_list(cls, session: AsyncSession) -> List[Menu]:
        """
        Метод возвращает список меню
        :param session: объект асинхронной сессии для запросов к БД
        :return: список с объектами меню
        """
        # joinedload - связываем таблицы (join) для подсчета и вывода кол-во подменю и блюд
        query = select(Menu).options(
            joinedload(Menu.submenus).options(joinedload(Submenu.dishes))
        )
        res = await session.execute(query)
        menu_list = res.unique().scalars().all()

        return list(menu_list)

    @classmethod
    async def create(cls, new_menu: BaseInSchema, session: AsyncSession) -> UUID:
        """
        Метод создает и возвращает новое меню
        :param new_menu: параметры для сохранения нового меню
        :param session: объект асинхронной сессии для запросов к БД
        :return: UUID-id новой записи
        """
        query = insert(Menu).values(
            title=new_menu.title, description=new_menu.description
        )
        res = await session.execute(query)
        await session.commit()

        # Возвращаем id новой записи
        return res.inserted_primary_key[0]

    @classmethod
    async def get(cls, menu_id: UUID, session: AsyncSession) -> Union[Menu, None]:
        """
        Метод возвращает меню по переданному id
        :param menu_id: id меню для поиска
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект меню либо None
        """
        # joinedload - связываем таблицы (join) для подсчета и вывода кол-во подменю и блюд
        query = (
            select(Menu)
            .options(joinedload(Menu.submenus).options(joinedload(Submenu.dishes)))
            .where(Menu.id == menu_id)
        )
        res = await session.execute(query)
        menu = res.unique().scalar_one_or_none()

        return menu

    @classmethod
    async def update(
        cls, menu_id: UUID, data: BaseInOptionalSchema, session: AsyncSession
    ) -> None:
        """
        Метод обновляет меню по переданному id
        :param menu_id: id меню для поиска
        :param data: параметры для сохранения нового меню
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """
        # model_dump(exclude_unset=True) - распаковывает явно переданные поля в patch-запросе
        query = (
            update(Menu)
            .where(Menu.id == menu_id)
            .values(data.model_dump(exclude_unset=True))
        )
        await session.execute(query)
        await session.commit()

    @classmethod
    async def delete(cls, delete_menu: Menu, session: AsyncSession) -> None:
        """
        Метод удаляет меню по переданному id
        :param delete_menu: объект меню для удаления
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """
        # Каскадное удаление связанных дочерних записей возможно только через session.delete()
        await session.delete(delete_menu)
        await session.commit()
