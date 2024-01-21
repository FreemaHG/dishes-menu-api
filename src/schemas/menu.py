from src.schemas.base import BaseOutSchema
from src.schemas.mixin import SubmenusCountMixinSchema, DishesCountMixinSchema


# TODO Раскомментировать после вычисления подменю и блюд в меню!!!
# class MenuOutSchema(BaseOutSchema, SubmenusCountMixinSchema, DishesCountMixinSchema):
class MenuOutSchema(BaseOutSchema):
    """
    Схема для вывода меню
    """
    pass
