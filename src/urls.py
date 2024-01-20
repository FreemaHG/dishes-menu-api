from fastapi import FastAPI

from src.routes.menu import router as menu_router


def register_routers(app: FastAPI) -> FastAPI:
    """
    Регистрация роутов для API
    """
    app.include_router(menu_router)  # Вывод списка с меню

    return app