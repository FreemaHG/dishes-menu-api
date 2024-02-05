from fastapi import APIRouter


class APIMenuRouter(APIRouter):
    """
    Модель описывает базовый URL и версию API для вывода меню
    """

    def __init__(self, *args, **kwargs):
        self.prefix = '/api/v1/menus'
        super().__init__(*args, **kwargs, prefix=self.prefix)
