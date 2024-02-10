from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.routes.abc_route import APIMenuRouter
from src.schemas.menu import MenuWithSubmenusOutSchema
from src.services.all_data import AllDataService

router = APIMenuRouter(tags=['all data'])


@router.get(
    '/all_data',
    response_model=list[MenuWithSubmenusOutSchema],
    responses={
        200: {'model': list[MenuWithSubmenusOutSchema]}
    },
)
async def get_all_data(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Роут для вывода всех меню со всеми связанными подменю и со всеми связанными блюдами
    """

    menu_list = await AllDataService.get_all_data(session=session)

    return menu_list
