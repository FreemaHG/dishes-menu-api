from typing import Union, List
from uuid import UUID
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from loguru import logger

from src.models.submenu import Submenu
from src.schemas.base import BaseInSchema, BaseInOptionalSchema


class SubmenuRepository:
    """
    Получение списка подменю, создания, обновления и удаления подменю
    """

    @classmethod
    async def get_list(cls, menu_id: str, session: AsyncSession) -> List[Submenu]:
        """
        Метод возвращает список подменю из БД
        :param menu_id: id меню, к которому относится подменю
        :param session: объект асинхронной сессии для запросов к БД
        :return: список подменю
        """
        # joinedload - связываем таблицы (join) для подсчета и вывода кол-во блюд
        query = (
            select(Submenu)
            .options(joinedload(Submenu.dishes))
            .where(Submenu.menu_id == menu_id)
        )
        res = await session.execute(query)
        submenu_list = res.unique().scalars().all()

        return list(submenu_list)


    @classmethod
    async def create(
        cls, menu_id: str, new_submenu: BaseInSchema, session: AsyncSession
    ) -> str:
        """
        Метод создает и возвращает id нового подменю из БД
        :param menu_id: id меню, к которому относится подменю
        :param new_sybmenu: параметры для сохранения нового подменю
        :param session: объект асинхронной сессии для запросов к БД
        :return: id нового подменю
        """
        query = insert(Submenu).values(
            title=new_submenu.title,
            description=new_submenu.description,
            menu_id=menu_id,
        )
        res = await session.execute(query)
        await session.commit()

        # Возвращаем id новой записи
        return res.inserted_primary_key[0]


    @classmethod
    async def get(cls, submenu_id: str, session: AsyncSession) -> Submenu | None:
        """
        Метод возвращает данные по подменю из БД по переданному id
        :param submenu_id: id подменю для поиска в БД
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект подменю либо None
        """
        query = (
            select(Submenu)
            .options(joinedload(Submenu.dishes))
            .where(Submenu.id == submenu_id)
        )
        res = await session.execute(query)
        submenu = res.unique().scalar_one_or_none()

        return submenu


    @classmethod
    async def update(
        cls, submenu_id: str, data: BaseInOptionalSchema, session: AsyncSession
    ) -> None:
        """
        Метод обновляет данные подменю в БД по переданному id
        :param submenu_id: id подменю
        :param data: параметры для сохранения нового подменю
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """
        # model_dump(exclude_unset=True) - распаковывает явно переданные поля в patch-запросе
        query = (
            update(Submenu)
            .where(Submenu.id == submenu_id)
            .values(data.model_dump(exclude_unset=True))
        )
        await session.execute(query)
        await session.commit()


    @classmethod
    async def delete(cls, delete_submenu: Submenu, session: AsyncSession) -> None:
        """
        Метод удаляет подменю из БД по переданному id
        :param delete_submenu: объект подменю для удаления
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """
        # Каскадное удаление связанных дочерних записей возможно только через session.delete(),
        # а не через delete().where()
        await session.delete(delete_submenu)
        await session.commit()
