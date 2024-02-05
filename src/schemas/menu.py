from src.schemas.base import BaseOutSchema
from src.schemas.mixin import DishesCountMixinSchema, SubmenusCountMixinSchema


class MenuOutSchema(BaseOutSchema, SubmenusCountMixinSchema, DishesCountMixinSchema):
    """
    Схема для вывода меню
    """

    pass
