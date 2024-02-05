from http import HTTPStatus
from typing import Union

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.routes.abc_route import APIMenuRouter
from src.schemas.dish import DishInOptionalSchema, DishInSchema, DishOutSchema
from src.schemas.response import ResponseForDeleteSchema, ResponseSchema
from src.services.dish import DishService
from src.utils.exceptions import CustomApiException

router = APIMenuRouter(tags=['dish'])


@router.get(
    '/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=list[DishOutSchema],
    responses={
        200: {'model': list[DishOutSchema]}
    },
)
async def get_dishes_list(
    submenu_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Роут для вывода списка с блюдами
    """
    dishes_list = await DishService.get_dishes_list(submenu_id=submenu_id, session=session)

    return dishes_list


@router.post(
    '/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=Union[DishOutSchema, ResponseSchema],
    responses={
        201: {'model': DishOutSchema},
    },
    status_code=201,
)
async def create_dish(
    submenu_id: str,
    new_dish: DishInSchema,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Роут для добавления блюда
    """
    dish = await DishService.create(submenu_id=submenu_id, new_dish=new_dish, session=session)

    if not dish:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail='submenu not found'
        )

    return dish


@router.get(
    '/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=Union[DishOutSchema, ResponseSchema],
    responses={
        200: {'model': DishOutSchema},
        404: {'model': ResponseSchema},
    },
)
async def get_dish(
    dish_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Роут для вывода блюда по id
    """
    dish = await DishService.get(dish_id=dish_id, session=session)

    if not dish:
        raise CustomApiException(status_code=HTTPStatus.NOT_FOUND, detail='dish not found')

    return dish


@router.patch(
    '/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=Union[DishOutSchema, ResponseSchema],
    responses={
        200: {'model': DishOutSchema},
        404: {'model': ResponseSchema},
    },
)
async def update_dish(
    dish_id: str,
    data: DishInOptionalSchema,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Роут для обновления блюда по id
    """
    updated_dish = await DishService.update(dish_id=dish_id, data=data, session=session)

    if not updated_dish:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail='dish not found'
        )

    return updated_dish


@router.delete(
    '/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=Union[ResponseForDeleteSchema, ResponseSchema],
    responses={
        200: {'model': ResponseForDeleteSchema},
        404: {'model': ResponseSchema},
    },
)
async def delete_dish(
    dish_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Роят для удаления блюда по id
    """
    res = await DishService.delete(dish_id=dish_id, session=session)

    if not res:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail='dish not found'
        )

    return ResponseForDeleteSchema(message='The dish has been deleted')
