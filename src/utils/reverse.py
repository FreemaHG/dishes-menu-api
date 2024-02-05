from src.main import app
from src.models.menu import Menu
from src.routes.menu import get_menu


@app.get('api/v1/menus/{menu_id}')
async def get_menu_by_urlname(menu_id: str) -> Menu:
    """
    Функция имитирует работу функции reverse() в Django, позволяя вызывать нужный роут по urlname
    """
    return await get_menu(menu_id)
