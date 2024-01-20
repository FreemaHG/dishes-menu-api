from http import HTTPStatus
from typing import Union, List
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from src.database import get_async_session
from src.routes.abc_route import APIMenuRouter
from src.schemas.menu import MenuOutSchema, MenuInSchema
from src.schemas.response import ResponseSchema, ResponseForDeleteSchema
from src.services.menu import MenuService
from src.utils.exceptions import CustomApiException


router = APIMenuRouter(tags=["menu"])


@router.get(
    "/",
    response_model=List[MenuOutSchema],  # Схема ответа
    responses={200: {"model": List[MenuOutSchema]}},  # Примеры схем ответов для документации
)
async def get_menu_list(
        session: AsyncSession = Depends(get_async_session),
):
    """
    Вывод списка меню
    """
    menu_list = await MenuService.get_list(session=session)
    return menu_list


@router.post(
    "/",
    response_model=MenuOutSchema,
    responses={
        201: {"model": MenuOutSchema},
    },
    status_code=201,
)
async def create_menu(
        new_menu: MenuInSchema,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Добавление меню
    """
    new_menu = await MenuService.create(new_menu=new_menu, session=session)
    return new_menu

@router.get(
    "/{menu_id}",
    response_model=Union[MenuOutSchema, ResponseSchema],
    responses={
        200: {"model": MenuOutSchema},
        404: {"model": ResponseSchema},
    },
)
async def get_menu(
        menu_id: UUID,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Вывод меню по id
    """
    menu = await MenuService.get(menu_id=menu_id, session=session)

    if menu:
        return menu

    raise CustomApiException(
        status_code=HTTPStatus.NOT_FOUND, detail="menu not found"
    )


@router.patch(
    "/{menu_id}",
    response_model=Union[MenuOutSchema, ResponseSchema],
    responses={
        200: {"model": MenuOutSchema},
        404: {"model": ResponseSchema},
    },
)
async def update_menu(
        menu_id: UUID,
        data: MenuInSchema,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Обновление меню по id
    """
    menu = await MenuService.update(menu_id=menu_id, data=data, session=session)

    if menu:
        return menu

    raise CustomApiException(
        status_code=HTTPStatus.NOT_FOUND, detail="menu not found"
    )


@router.delete(
    "/{menu_id}",
    response_model=Union[ResponseForDeleteSchema, ResponseSchema],
    responses={
        200: {"model": ResponseForDeleteSchema},
        404: {"model": ResponseSchema},
    },
)
async def delete_menu(
        menu_id: UUID,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Удаление меню по id
    """
    res = await MenuService.delete(menu_id=menu_id, session=session)

    if res:
        return ResponseForDeleteSchema(message="The menu has been deleted")

    raise CustomApiException(
        status_code=HTTPStatus.NOT_FOUND, detail="menu not found"
    )
