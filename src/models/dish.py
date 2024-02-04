from sqlalchemy import ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column

from src.models.abc_model import BaseABC


class Dish(BaseABC):
    """
    Модель для хранения записей о блюде
    """

    __tablename__ = "dish"

    price: Mapped[float] = mapped_column(Float(precision=2))
    submenu_id: Mapped[int] = mapped_column(ForeignKey("submenu.id"))

    def as_dict(self):
        """
        Преобразование модели в словарь (для кэширования в Redis)
        """
        model_dict = super().as_dict()
        model_dict["submenu_id"] = str(model_dict["submenu_id"])

        return model_dict
