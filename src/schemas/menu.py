from src.schemas.base import BaseOutSchema
from src.schemas.mixin import DishesCountMixinSchema, SubmenusCountMixinSchema
from src.schemas.submenu import SubmenuWithDishesOutSchema


class MenuOutSchema(BaseOutSchema, SubmenusCountMixinSchema, DishesCountMixinSchema):
    """
    Схема для вывода меню
    """

    pass


class MenuWithSubmenusOutSchema(MenuOutSchema):
    """
    Схема для вывода меню со всеми связанными подменю и блюдами
    """

    submenus: list[SubmenuWithDishesOutSchema]
