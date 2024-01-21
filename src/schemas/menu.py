from src.schemas.base import BaseOutSchema
from src.schemas.mixin import SubmenusCountMixinSchema, DishesCountMixinSchema


class MenuOutSchema(BaseOutSchema, SubmenusCountMixinSchema, DishesCountMixinSchema):
    """
    Схема для вывода меню
    """

    pass
