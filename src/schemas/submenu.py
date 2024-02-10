from src.schemas.base import BaseOutSchema
from src.schemas.dish import DishOutSchema
from src.schemas.mixin import DishesCountMixinSchema


class SubmenuOutSchema(BaseOutSchema, DishesCountMixinSchema):
    """
    Схема для вывода подменю
    """

    pass


class SubmenuWithDishesOutSchema(SubmenuOutSchema):
    """
    Схема для вывода подменю со всеми связанными блюдами
    """

    dishes: list[DishOutSchema]
