from typing import Union, List
from uuid import UUID

from loguru import logger
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

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
        :menu_id session: id меню, к которому относится подменю
        :param session: объект асинхронной сессии для запросов к БД
        :return: список с объектами подменю
        """
        query = select(Submenu).where(Submenu.menu_id == menu_id)
        res = await session.execute(query)
        submenu_list = res.scalars().all()

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
        query = select(Submenu).where(Submenu.id == submenu_id)
        submenu = await session.execute(query)

        return submenu.scalar_one_or_none()


    @classmethod
    async def update(cls, submenu_id: UUID, data: BaseInSchema, session: AsyncSession) -> None:
        """
        Метод обновляет подменю по переданному id
        :param submenu_id: id подменю для одновления
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
    async def delete(cls, submenu_id: UUID, session: AsyncSession) -> None:
        """
        Метод удаляет подменю по переданному id
        :param submenu_id: id подменю для поиска
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """
        query = delete(Submenu).where(Submenu.id == submenu_id)
        await session.execute(query)
        await session.commit()
