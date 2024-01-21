from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseInSchema(BaseModel):
    """
    Базовая схема для добавления нового меню / блюда
    """
    title: str
    description: str

    # Автоматическое преобразование данных ORM-модели в объект схемы для сериализации
    model_config = ConfigDict(from_attributes=True)


class BaseOutSchema(BaseInSchema):
    """
    Базовая схема для вывода меню / блюда
    """
    id: UUID
