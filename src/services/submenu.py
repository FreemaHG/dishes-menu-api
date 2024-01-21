from typing import Union, List
from uuid import UUID

from loguru import logger
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.submenu import Submenu
from src.schemas.base import BaseInSchema


class SubmenuService:
    """
    Сервис для вывода списка подменю, создания, обновления и удаления подменю
    """

    @classmethod
    async def get_list(cls, menu_id: UUID, session: AsyncSession) -> List[Submenu]:
        """
        Метод возвращает список подменю
        :param session: id меню, к которому относится подменю
        :param session: объект асинхронной сессии для запросов к БД
        :return: список с объектами подменю
        """
        # joinedload - связываем таблицы (join) для подсчета и вывода кол-во блюд
        query = select(Submenu).options(joinedload(Submenu.dishes)).where(Submenu.menu_id == menu_id)
        res = await session.execute(query)
        submenu_list = res.unique().scalars().all()

        return list(submenu_list)


    @classmethod
    async def create(cls, menu_id: UUID, new_submenu: BaseInSchema, session: AsyncSession) -> Union[Submenu, False]:
        """
        Метод создает и возвращает новое подменю
        :param menu_id: id меню, к которому относится подменю
        :param new_sybmenu: параметры для сохранения нового подменю
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект нового подменю
        """
        submenu = Submenu(
            title=new_submenu.title,
            description=new_submenu.description,
            menu_id=menu_id
        )

        session.add(submenu)
        await session.commit()

        return submenu


    @classmethod
    async def get(cls, submenu_id: UUID, session: AsyncSession) -> Union[Submenu, None]:
        """
        Метод возвращает подменю по переданному id
        :param submenu_id: id подменю для поиска
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект меню либо None
        """
        query = select(Submenu).options(joinedload(Submenu.dishes)).where(Submenu.id == submenu_id)
        res = await session.execute(query)
        submenu = res.unique().scalar_one_or_none()

        return submenu


    @classmethod
    async def update(cls, submenu_id: UUID, data: BaseInSchema, session: AsyncSession) -> None:
        """
        Метод обновляет подменю по переданному id
        :param submenu_id: id подменю для обновления
        :param data: параметры для сохранения нового подменю
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """
        query = update(Submenu).where(Submenu.id == submenu_id).values(
            title=data.title,
            description=data.description,
        )
        await session.execute(query)
        await session.commit()


    @classmethod
    async def delete(cls, delete_submenu: Submenu, session: AsyncSession) -> None:
        """
        Метод удаляет подменю по переданному id
        :param delete_submenu: объект подменю для удаления
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """
        # Каскадное удаление связанных дочерних записей возможно только через session.delete(),
        # а не через delete().where()
        await session.delete(delete_submenu)
        await session.commit()
