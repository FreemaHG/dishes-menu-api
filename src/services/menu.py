from typing import Union, List
from uuid import UUID

from loguru import logger
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.menu import Menu
from src.schemas.menu import MenuInSchema


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
        res = await session.execute(select(Menu))
        menu_list = res.scalars().all()

        return list(menu_list)


    @classmethod
    async def create(cls, new_menu: MenuInSchema, session: AsyncSession) -> Menu:
        """
        Метод создает и возвращает новое меню
        :param new_menu: параметры для сохранения нового меню
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект нового меню
        """
        new_menu = Menu(
            title=new_menu.title,
            description=new_menu.description
        )

        session.add(new_menu)
        await session.commit()

        return new_menu


    @classmethod
    async def get(cls, menu_id: UUID, session: AsyncSession) -> Union[Menu, None]:
        """
        Метод возвращает меню по переданному id
        :param menu_id: id меню для поиска
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект меню либо None
        """
        query = select(Menu).where(Menu.id == menu_id)
        tweet = await session.execute(query)

        return tweet.scalar_one_or_none()


    @classmethod
    async def update(cls, menu_id: UUID, data: MenuInSchema, session: AsyncSession) -> Union[Menu, None]:
        """
        Метод обновляет меню по переданному id
        :param menu_id: id меню для поиска
        :param new_menu: параметры для сохранения нового меню
        :param session: объект асинхронной сессии для запросов к БД
        :return: обновленный объект меню либо None
        """
        query = update(Menu).where(Menu.id == menu_id).values(
            title=data.title,
            description=data.description,
        )
        await session.execute(query)
        await session.commit()

        updated_menu = await cls.get(menu_id=menu_id, session=session)

        return updated_menu


    @classmethod
    async def delete(cls, menu_id: UUID, session: AsyncSession) -> bool:
        """
        Метод удаляет меню по переданному id
        :param menu_id: id меню для поиска
        :param session: объект асинхронной сессии для запросов к БД
        :return: True - успешное удаление, иначе False
        """
        delete_menu = await cls.get(menu_id=menu_id, session=session)

        if delete_menu:
            query = delete(Menu).where(Menu.id == menu_id)
            await session.execute(query)
            await session.commit()

            return True

        else:
            return False
