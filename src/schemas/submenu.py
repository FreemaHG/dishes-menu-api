from src.schemas.base import BaseOutSchema
from src.schemas.mixin import DishesCountMixinSchema


# TODO Раскомментировать после вычисления блюд в подменю!!!
# class SubmenuOutSchema(BaseOutSchema, DishesCountMixinSchema):
class SubmenuOutSchema(BaseOutSchema):
    """
    Схема для вывода подменю
    """
    pass
