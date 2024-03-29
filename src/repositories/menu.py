from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.menu import Menu
from src.models.submenu import Submenu
from src.schemas.base import BaseInOptionalSchema, BaseInSchema


class MenuRepository:
    """
    Получение списка меню, создания, обновление и удаления меню из БД
    """

    @classmethod
    async def get_list(cls, session: AsyncSession) -> list[Menu]:
        """
        Метод возвращает меню из БД
        :param session: объект асинхронной сессии для запросов к БД
        :return: список меню
        """
        # joinedload - связываем таблицы (join) для подсчета и вывода кол-во подменю и блюд
        query = select(Menu).options(
            joinedload(Menu.submenus).options(joinedload(Submenu.dishes))
        )
        res = await session.execute(query)
        menus_list = res.unique().scalars().all()

        return list(menus_list)

    @classmethod
    async def create(cls, new_menu: BaseInSchema, session: AsyncSession) -> str:
        """
        Метод создает и возвращает id нового меню из БД
        :param new_menu: параметры для сохранения нового меню
        :param session: объект асинхронной сессии для запросов к БД
        :return: id созданного меню
        """
        query = insert(Menu).values(
            title=new_menu.title, description=new_menu.description
        )

        res = await session.execute(query)
        await session.commit()

        # Возвращаем id новой записи
        return str(res.inserted_primary_key[0])

    @classmethod
    async def get(cls, menu_id: str, session: AsyncSession) -> Menu:
        """
        Метод возвращает данные по меню из БД по переданному id
        :param menu_id: id меню для поиска в БД
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
        cls, menu_id: str, data: BaseInOptionalSchema, session: AsyncSession
    ) -> None:
        """
        Метод обновляет данные меню в БД по переданному id
        :param menu_id: id меню
        :param data: новые параметры для меню
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
        Метод удаляет меню из БД по переданному id
        :param delete_menu: объект меню для удаления
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """
        # Каскадное удаление связанных дочерних записей возможно только через session.delete()
        # а не через delete().where()
        await session.delete(delete_menu)
        await session.commit()


class MenuListRepository:
    """
    Получение списка меню и удаление всех меню из БД
    """

    # TODO Переместить метод вывода списка сюда и проверить везде корректную работы

    @classmethod
    async def delete_list(cls, session: AsyncSession) -> None:
        """
        Метод удаляет из БД все меню
        :param session: объект асинхронной сессии для запросов к БД
        :return: None
        """
        menus = await MenuRepository.get_list(session=session)

        for menu in menus:
            await session.delete(menu)
            await session.commit()
