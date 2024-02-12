from typing import Any

from pydantic import Field, field_validator, model_validator

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
    discount: int = Field(exclude=True)

    @model_validator(mode='after')
    @classmethod
    def out_price_with_discount(cls, data: Any) -> Any:
        """
        Валидатор проверяет есть ли скидка на данною блюдо и возвращает цену с учетом скидки
        :param data: данные записи о блюде
        :return: данные записи о блюде с учетом скидки
        """
        if data.discount != 0:
            discount = float(data.price) * (data.discount / 100)
            new_price = round(float(data.price) - discount, 2)
            data.price = '%.2f' % float(new_price)

        return data

    @field_validator('price', mode='before')
    def serialize_price(cls, val: float):
        """
        Возвращаем цену блюда в виде строки с округлением до двух знаков после запятой
        """
        return '%.2f' % float(val)
