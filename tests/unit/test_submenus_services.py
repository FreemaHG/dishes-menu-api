from uuid import UUID

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.menu import Menu
from src.models.submenu import Submenu
from src.repositories.submenu import SubmenuRepository
from src.schemas.base import BaseInOptionalSchema, BaseInSchema


@pytest.mark.unit
class TestSubmenusServices:
    """
    Тестирование сервисов для создания, вывода, обновления и удаления подменю
    """

    async def test_create_submenu(
            self,
            session: AsyncSession,
            menu: Menu,
            submenu_schema: BaseInSchema,
    ) -> None:
        """
        Проверка метода для создания подменю
        """
        submenu_id = await SubmenuRepository.create(menu_id=menu.id, new_submenu=submenu_schema, session=session)

        assert submenu_id
        assert isinstance(submenu_id, str)

    async def test_get_submenu(
            self,
            submenu: Submenu,
            session: AsyncSession,
    ) -> None:
        """
        Проверка метода для получения подменю по id
        """
        submenu_res = await SubmenuRepository.get(submenu_id=submenu.id, session=session)

        assert submenu_res
        assert isinstance(submenu_res.id, UUID)
        assert submenu_res.id == submenu.id

    async def test_get_list_submenus(
            self,
            menu: Menu,
            session: AsyncSession
    ) -> None:
        """
        Проверка метода для получения списка подменю
        """
        submenus_list = await SubmenuRepository.get_list(menu_id=menu.id, session=session)

        assert submenus_list
        assert isinstance(submenus_list, list)
        assert len(submenus_list) == 2

    async def test_update_submenu(
            self,
            submenu: Submenu,
            submenu_update_schema: BaseInOptionalSchema,
            session: AsyncSession,
    ) -> None:
        """
        Проверка метода для обновления меню
        """
        await SubmenuRepository.update(submenu_id=submenu.id, data=submenu_update_schema, session=session)

        query = select(Submenu).where(Submenu.id == submenu.id)
        res = await session.execute(query)
        updated_submenu = res.scalar()

        assert updated_submenu.title == submenu_update_schema.title

    async def test_delete_submenu(
            self,
            submenu: Submenu,
            session: AsyncSession,
    ) -> None:
        """
        Проверка метода для удаления подменю по id
        """
        await SubmenuRepository.delete(delete_submenu=submenu, session=session)

        query = select(Submenu).where(Submenu.id == submenu.id)
        res = await session.execute(query)

        assert res.scalar_one_or_none() is None
