from src.schemas.base import BaseOutSchema


class DishOutSchema(BaseOutSchema):
    """
    Схема для вывода блюда
    """
    price: float
