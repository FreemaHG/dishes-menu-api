from uuid import UUID

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.dish import Dish
from src.models.submenu import Submenu
from src.repositories.dish import DishRepository
from src.schemas.dish import DishInOptionalSchema, DishInSchema


@pytest.mark.unit
class TestDishesServices:
    """
    Тестирование сервисов для создания, вывода, обновления и удаления блюд
    """

    async def test_create_dish(
            self,
            submenu: Submenu,
            dish_schema: DishInSchema,
            session: AsyncSession,
    ) -> None:
        """
        Проверка метода для создания блюда
        """
        created_dish = await DishRepository.create(submenu_id=submenu.id, new_dish=dish_schema, session=session)

        assert created_dish
        assert isinstance(created_dish.id, UUID)

    async def test_get_dish(
            self,
            dish: Dish,
            session: AsyncSession,
    ) -> None:
        """
        Проверка метода для получения блюда по id
        """
        dish_res = await DishRepository.get(dish_id=dish.id, session=session)

        assert dish_res
        assert isinstance(dish_res.id, UUID)
        assert dish_res.id == dish.id

    async def test_get_list_dishes(
            self,
            submenu: Submenu,
            session: AsyncSession
    ) -> None:
        """
        Проверка метода для получения списка блюд
        """
        dishes_list = await DishRepository.get_list(submenu_id=submenu.id, session=session)

        assert dishes_list
        assert isinstance(dishes_list, list)

    async def test_update_dish(
            self,
            dish: Dish,
            dish_update_schema: DishInOptionalSchema,
            session: AsyncSession,
    ) -> None:
        """
        Проверка метода для обновления меню
        """
        await DishRepository.update(dish_id=dish.id, data=dish_update_schema, session=session)

        query = select(Dish).where(Dish.id == dish.id)
        res = await session.execute(query)
        updated_dish = res.scalar()

        assert updated_dish.title == dish_update_schema.title

    async def test_delete_dish(
            self,
            dish: Dish,
            session: AsyncSession,
    ) -> None:
        """
        Проверка метода для удаления блюда по id
        """
        await DishRepository.delete(dish_id=dish.id, session=session)

        query = select(Dish).where(Dish.id == dish.id)
        res = await session.execute(query)

        assert res.scalar_one_or_none() is None
