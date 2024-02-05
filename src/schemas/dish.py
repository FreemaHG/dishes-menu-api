from pydantic import field_validator

from src.schemas.base import BaseInSchema, BaseOutSchema


class DishInSchema(BaseInSchema):
    """
    Схема для добавления нового блюда
    """

    price: float


# Схема для обновления блюда (patch-запрос, поля не обязательные)
DishInOptionalSchema = DishInSchema.all_optional('DishInOptionalSchema')


class DishOutSchema(BaseOutSchema):
    """
    Схема для вывода блюда
    """

    price: str

    @field_validator('price', mode='before')
    def serialize_price(cls, val: float):
        """
        Возвращаем цену блюда в виде строки с округлением до двух знаков после запятой
        """
        return '%.2f' % float(val)
