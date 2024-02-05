from uuid import UUID

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.menu import Menu
from src.repositories.menu import MenuRepository
from src.schemas.base import BaseInOptionalSchema, BaseInSchema


@pytest.mark.unit
class TestMenusServices:
    """
    Тестирование сервисов для создания, вывода, обновления и удаления меню
    """

    async def test_create_menu(
            self,
            session: AsyncSession,
            menu_schema: BaseInSchema,
    ) -> None:
        """
        Проверка метода для создания меню
        """
        menu_id = await MenuRepository.create(new_menu=menu_schema, session=session)

        assert menu_id
        assert isinstance(menu_id, str)

    async def test_get_menu(
            self,
            session: AsyncSession,
            menu: Menu,
    ) -> None:
        """
        Проверка метода для получения меню по id
        """
        menu_res = await MenuRepository.get(menu_id=menu.id, session=session)

        assert menu_res
        assert isinstance(menu_res.id, UUID)
        assert menu_res.id == menu.id

    async def test_get_list_menus(
            self,
            session: AsyncSession
    ) -> None:
        """
        Проверка метода для получения списка меню
        """
        menus_list = await MenuRepository.get_list(session=session)

        assert menus_list
        assert isinstance(menus_list, list)

    async def test_update_menu(
            self,
            menu: Menu,
            menu_update_schema: BaseInOptionalSchema,
            session: AsyncSession,
    ) -> None:
        """
        Проверка метода для обновления меню
        """
        await MenuRepository.update(menu_id=menu.id, data=menu_update_schema, session=session)

        query = select(Menu).where(Menu.id == menu.id)
        res = await session.execute(query)
        updated_menu = res.scalar()

        assert updated_menu.title == menu_update_schema.title

    async def test_delete_menu(
            self,
            session: AsyncSession,
            menu: Menu,
    ) -> None:
        """
        Проверка метода для удаления меню по id
        """
        await MenuRepository.delete(delete_menu=menu, session=session)

        query = select(Menu).where(Menu.id == menu.id)
        res = await session.execute(query)

        assert res.scalar_one_or_none() is None
