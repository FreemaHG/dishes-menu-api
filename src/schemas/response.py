from pydantic import BaseModel, ConfigDict
from http import HTTPStatus


class ResponseSchema(BaseModel):
    """
    Базовая схема для возврата сообщения с ответом
    """
    detail: str


class ResponseForDeleteSchema(BaseModel):
    """
    Базовая схема для возврата сообщения при удалении меню / подменю / блюда
    """
    status: bool = True
    message: str
