from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, create_model


class BaseInSchema(BaseModel):
    """
    Базовая схема для добавления нового меню / блюда
    """
    title: str
    description: str

    # Автоматическое преобразование данных ORM-модели в объект схемы для сериализации
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def all_optional(cls, name: str) -> type[Self]:
        """
        Создает новую модель с теми же полями, но все необязательные.

        Использование: SomeOptionalModel = SomeModel.all_optional('SomeOptionalModel')
        """
        return create_model(
            name,
            __base__=cls,
            **{name: (info.annotation, None) for name, info in cls.model_fields.items()}
        )


# Схема для обновления меню / подменю (patch-запрос, поля не обязательные)
BaseInOptionalSchema = BaseInSchema.all_optional('BaseInOptionalSchema')


class BaseOutSchema(BaseInSchema):
    """
    Базовая схема для вывода меню / блюда
    """
    id: UUID
