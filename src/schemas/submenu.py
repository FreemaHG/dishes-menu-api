from src.schemas.base import BaseOutSchema
from src.schemas.mixin import DishesCountMixinSchema


class SubmenuOutSchema(BaseOutSchema, DishesCountMixinSchema):
    """
    Схема для вывода подменю
    """
    pass
