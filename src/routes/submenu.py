from http import HTTPStatus
from typing import Union, List
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from src.database import get_async_session
from src.routes.abc_route import APIMenuRouter
from src.schemas.base import BaseInSchema
from src.schemas.submenu import SubmenuOutSchema
from src.schemas.response import ResponseSchema, ResponseForDeleteSchema
from src.services.menu import MenuService
from src.services.submenu import SubmenuService
from src.utils.exceptions import CustomApiException


router = APIMenuRouter(tags=["submenu"])


@router.get(
    "/{menu_id}/submenus",
    response_model=List[SubmenuOutSchema],  # Схема ответа
    responses={200: {"model": List[SubmenuOutSchema]}},  # Примеры схем ответов для документации
)
async def get_submenus_list(
        menu_id: UUID,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Вывод списка подменю
    """
    submenu_list = await SubmenuService.get_list(menu_id=menu_id, session=session)
    return submenu_list


@router.post(
    "/{menu_id}/submenus",
    response_model=Union[SubmenuOutSchema, ResponseSchema],
    responses={
        201: {"model": SubmenuOutSchema},
        404: {"model": ResponseSchema},
    },
    status_code=201,
)
async def create_submenu(
        menu_id: UUID,
        new_submenu: BaseInSchema,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Добавление подменю
    """
    menu = await MenuService.get(menu_id=menu_id, session=session)

    if menu:
        created_submenu = await SubmenuService.create(menu_id=menu_id, new_submenu=new_submenu, session=session)
        return created_submenu
    else:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail="menu not found"
        )


@router.get(
    "/{menu_id}/submenus/{submenu_id}",
    response_model=Union[SubmenuOutSchema, ResponseSchema],
    responses={
        200: {"model": SubmenuOutSchema},
        404: {"model": ResponseSchema},
    },
)
async def get_submenu(
        submenu_id: UUID,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Вывод подменю по id
    """
    submenu = await SubmenuService.get(submenu_id=submenu_id, session=session)

    if submenu:
        return submenu

    raise CustomApiException(
        status_code=HTTPStatus.NOT_FOUND, detail="submenu not found"
    )


@router.patch(
    "/{menu_id}/submenus/{submenu_id}",
    response_model=Union[SubmenuOutSchema, ResponseSchema],
    responses={
        200: {"model": SubmenuOutSchema},
        404: {"model": ResponseSchema},
    },
)
async def update_submenu(
        submenu_id: UUID,
        data: BaseInSchema,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Обновление подменю по id
    """
    update_menu = await SubmenuService.get(submenu_id=submenu_id, session=session)

    if update_menu:
        await SubmenuService.update(submenu_id=submenu_id, data=data, session=session)
        return update_menu
    else:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail="submenu not found"
        )


@router.delete(
    "/{menu_id}/submenus/{submenu_id}",
    response_model=Union[ResponseForDeleteSchema, ResponseSchema],
    responses={
        200: {"model": ResponseForDeleteSchema},
        404: {"model": ResponseSchema},
    },
)
async def delete_submenu(
        submenu_id: UUID,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Удаление подменю по id
    """
    delete_submenu = await SubmenuService.get(submenu_id=submenu_id, session=session)

    if delete_submenu:
        await SubmenuService.delete(delete_submenu=delete_submenu, session=session)
        return ResponseForDeleteSchema(message="The submenu has been deleted")
    else:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail="submenu not found"
        )
