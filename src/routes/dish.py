from http import HTTPStatus
from typing import Union, List
from uuid import UUID
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.routes.abc_route import APIMenuRouter
from src.schemas.dish import DishOutSchema, DishInSchema, DishInOptionalSchema
from src.schemas.response import ResponseSchema, ResponseForDeleteSchema
from src.services.dish import DishService
from src.services.submenu import SubmenuService
from src.utils.exceptions import CustomApiException


router = APIMenuRouter(tags=["dish"])


@router.get(
    "/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=List[DishOutSchema],  # Схема ответа
    responses={
        200: {"model": List[DishOutSchema]}
    },  # Примеры схем ответов для документации
)
async def get_dishes_list(
    submenu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Вывод списка с блюдами
    """
    dishes_list = await DishService.get_list(submenu_id=submenu_id, session=session)
    return dishes_list


@router.post(
    "/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=Union[DishOutSchema, ResponseSchema],
    responses={
        201: {"model": DishOutSchema},
        404: {"model": ResponseSchema},
    },
    status_code=201,
)
async def create_dish(
    submenu_id: UUID,
    new_dish: DishInSchema,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Добавление блюда
    """
    submenu = await SubmenuService.get(submenu_id=submenu_id, session=session)

    if submenu:
        created_dish = await DishService.create(
            submenu_id=submenu_id, new_dish=new_dish, session=session
        )
        return created_dish
    else:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail="submenu not found"
        )


@router.get(
    "/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=Union[DishOutSchema, ResponseSchema],
    responses={
        200: {"model": DishOutSchema},
        404: {"model": ResponseSchema},
    },
)
async def get_dish(
    dish_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Вывод блюда по id
    """
    dish = await DishService.get(dish_id=dish_id, session=session)

    if dish:
        return dish

    raise CustomApiException(status_code=HTTPStatus.NOT_FOUND, detail="dish not found")


@router.patch(
    "/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=Union[DishOutSchema, ResponseSchema],
    responses={
        200: {"model": DishOutSchema},
        404: {"model": ResponseSchema},
    },
)
async def update_dish(
    dish_id: UUID,
    data: DishInOptionalSchema,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Обновление блюда по id
    """
    update_dish = await DishService.get(dish_id=dish_id, session=session)

    if update_dish:
        await DishService.update(dish_id=dish_id, data=data, session=session)
        return update_dish
    else:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail="dish not found"
        )


@router.delete(
    "/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=Union[ResponseForDeleteSchema, ResponseSchema],
    responses={
        200: {"model": ResponseForDeleteSchema},
        404: {"model": ResponseSchema},
    },
)
async def delete_dish(
    dish_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Удаление блюда по id
    """
    delete_dish = await DishService.get(dish_id=dish_id, session=session)

    if delete_dish:
        await DishService.delete(dish_id=dish_id, session=session)
        return ResponseForDeleteSchema(message="The dish has been deleted")
    else:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail="dish not found"
        )
