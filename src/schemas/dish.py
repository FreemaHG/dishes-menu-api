from typing import Any

from pydantic import field_validator, model_validator

from src.models.dish import Dish
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

    @model_validator(mode='before')
    @classmethod
    def out_price_with_discount(cls, data: Any) -> Any:
        """
        Вывод цены с учетом скидки
        """

        if isinstance(data, Dish):
            data.price = data.discount_price

        return data
