from uuid import UUID

from http import HTTPStatus
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, ConfigDict


class MenuInSchema(BaseModel):
    """
    Схема для добавления нового меню
    """
    title: str
    description: str

    # Автоматическое преобразование данных ORM-модели в объект схемы для сериализации
    model_config = ConfigDict(from_attributes=True)


class MenuOutSchema(MenuInSchema):
    """
    Схема для вывода меню
    """
    id: UUID
    # FIXME Реализовать позже!
    # submenus_count: int
    # dishes_count: int
