from src.schemas.base import BaseInSchema


class BaseParserSchema(BaseInSchema):
    """
    Базовая схема для проверки данных о после парсинга
    """

    number: int
