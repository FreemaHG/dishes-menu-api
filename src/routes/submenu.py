from http import HTTPStatus
from typing import Union
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.routes.abc_route import APIMenuRouter
from src.schemas.base import BaseInOptionalSchema, BaseInSchema
from src.schemas.response import ResponseForDeleteSchema, ResponseSchema
from src.schemas.submenu import SubmenuOutSchema
from src.services.submenu import SubmenuService
from src.utils.exceptions import CustomApiException

router = APIMenuRouter(tags=['submenu'])


@router.get(
    '/{menu_id}/submenus',
    response_model=list[SubmenuOutSchema],
    responses={
        200: {'model': list[SubmenuOutSchema]}
    },
)
async def get_submenus_list(
    menu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Роут для вывода списка подменю
    """
    submenu_list = await SubmenuService.get_submenus_list(menu_id=str(menu_id), session=session)

    return submenu_list


@router.post(
    '/{menu_id}/submenus',
    response_model=SubmenuOutSchema,
    responses={
        201: {'model': SubmenuOutSchema}
    },
    status_code=201,
)
async def create_submenu(
    menu_id: UUID,
    new_submenu: BaseInSchema,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Роут для добавления подменю
    """
    submenu = await SubmenuService.create(menu_id=str(menu_id), new_submenu=new_submenu, session=session)

    if not submenu:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail='menu not found'
        )

    return submenu


@router.get(
    '/{menu_id}/submenus/{submenu_id}',
    response_model=Union[SubmenuOutSchema, ResponseSchema],
    responses={
        200: {'model': SubmenuOutSchema},
        404: {'model': ResponseSchema},
    },
)
async def get_submenu(
    submenu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Роут для вывода подменю по id
    """
    submenu = await SubmenuService.get(submenu_id=str(submenu_id), session=session)

    if not submenu:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail='submenu not found'
        )

    return submenu


@router.patch(
    '/{menu_id}/submenus/{submenu_id}',
    response_model=Union[SubmenuOutSchema, ResponseSchema],
    responses={
        200: {'model': SubmenuOutSchema},
        404: {'model': ResponseSchema},
    },
)
async def update_submenu(
    submenu_id: UUID,
    data: BaseInOptionalSchema,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Роут для обновления подменю по id
    """
    updated_submenu = await SubmenuService.update(submenu_id=str(submenu_id), data=data, session=session)

    if not updated_submenu:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail='submenu not found'
        )

    return updated_submenu


@router.delete(
    '/{menu_id}/submenus/{submenu_id}',
    response_model=Union[ResponseForDeleteSchema, ResponseSchema],
    responses={
        200: {'model': ResponseForDeleteSchema},
        404: {'model': ResponseSchema},
    },
)
async def delete_submenu(
    submenu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Роут для удаления подменю по id
    """
    res = await SubmenuService.delete(submenu_id=str(submenu_id), session=session)

    if not res:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND, detail='submenu not found'
        )

    return ResponseForDeleteSchema(message='The submenu has been deleted')
