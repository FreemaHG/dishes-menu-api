from http import HTTPStatus
from typing import Union

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.routes.abc_route import APIMenuRouter
from src.schemas.base import BaseInOptionalSchema, BaseInSchema
from src.schemas.menu import MenuOutSchema
from src.schemas.response import ResponseForDeleteSchema, ResponseSchema
from src.services.menu import MenuService
from src.utils.exceptions import CustomApiException

router = APIMenuRouter(tags=['menu'])


@router.get(
    '',
    response_model=list[MenuOutSchema],
    responses={
        200: {'model': list[MenuOutSchema]}
    },
)
async def get_menu_list(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Роут для вывода списка меню
    """
    menu_list = await MenuService.get_menus_list(session=session)

    return menu_list


@router.post(
    '',
    response_model=MenuOutSchema,
    responses={
        201: {'model': MenuOutSchema},
    },
    status_code=201,
)
async def create_menu(
    new_menu: BaseInSchema,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Роут для добавления нового меню
    """
    menu = await MenuService.create(new_menu=new_menu, session=session)

    return menu


@router.get(
    '/{menu_id}',
    response_model=Union[MenuOutSchema, ResponseSchema],
    responses={
        200: {'model': MenuOutSchema},
        404: {'model': ResponseSchema},
    },
)
async def get_menu(
    menu_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Роут для вывода меню по id
    """
    menu = await MenuService.get(menu_id=menu_id, session=session)

    if not menu:
        raise CustomApiException(status_code=HTTPStatus.NOT_FOUND, detail='menu not found')

    return menu


@router.patch(
    '/{menu_id}',
    response_model=Union[MenuOutSchema, ResponseSchema],
    responses={
        200: {'model': MenuOutSchema},
        404: {'model': ResponseSchema},
    },
)
async def update_menu(
    menu_id: str,
    data: BaseInOptionalSchema,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Роут для обновления меню по id
    """
    updated_menu = await MenuService.update(menu_id=menu_id, data=data, session=session)

    if not updated_menu:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail='menu not found'
        )

    return updated_menu


@router.delete(
    '/{menu_id}',
    response_model=Union[ResponseForDeleteSchema, ResponseSchema],
    responses={
        200: {'model': ResponseForDeleteSchema},
        404: {'model': ResponseSchema},
    },
)
async def delete_menu(
    menu_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Роут дл удаления меню по id
    """
    res = await MenuService.delete(menu_id=menu_id, session=session)

    if not res:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail='menu not found'
        )

    return ResponseForDeleteSchema(message='The menu has been deleted')
