from fastapi import FastAPI

from src.routes.all_data import router as all_data_router
from src.routes.dish import router as dish_router
from src.routes.menu import router as menu_router
from src.routes.submenu import router as submenu_router


def register_routers(app: FastAPI) -> FastAPI:
    """
    Регистрация роутов для API
    """

    app.include_router(all_data_router)  # Для корректной отработки роута подключаем его первым!
    app.include_router(menu_router)
    app.include_router(submenu_router)
    app.include_router(dish_router)

    return app
