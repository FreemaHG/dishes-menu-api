class SubmenusCountMixinSchema:
    """
    Схема добавляет поле для вывода кол-ва подменю в меню
    """
    submenus_count: int


class DishesCountMixinSchema:
    """
    Схема добавляет поле для вывода кол-ва блюд в меню / подменю
    """
    dishes_count: int
