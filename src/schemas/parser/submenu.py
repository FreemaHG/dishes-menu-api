from src.schemas.parser.base import BaseParserSchema
from src.schemas.parser.dish import DishParserSchema


class SubmenuParserSchema(BaseParserSchema):
    """
    Схема для проверки распарсенных данных о подменю
    """

    dishes: list[DishParserSchema] | None
