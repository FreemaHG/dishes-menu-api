from loguru import logger
from pydantic import field_validator

from src.schemas.dish import DishInSchema
from src.schemas.parser.base import BaseParserSchema


class DishParserSchema(BaseParserSchema, DishInSchema):
    """
    Схема для проверки распарсенных данных о блюде
    """

    discount: int

    @field_validator('discount', mode='after')
    def serialize_discount(cls, val: int):
        """
        Проверка корректности скидки (от 1 до 90)
        """

        if not 0 <= val <= 90 or val is None:
            logger.error(f'Скидка должна быть от 0 до 90%. Текущее значение: {val}')

            return 0

        return val
