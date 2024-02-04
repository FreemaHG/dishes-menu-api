from typing import List

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, relationship

from src.models.abc_model import BaseABC
from src.models.submenu import Submenu


class Menu(BaseABC):
    """
    Модель для хранения записей о меню
    """

    __tablename__ = "menu"

    submenus: Mapped[List["Submenu"]] = relationship(
        backref="menu", cascade="all, delete"
    )

    @hybrid_property
    def submenus_count(self) -> int:
        """
        Кол-во подменю в меню
        """
        return len(self.submenus)

    @hybrid_property
    def dishes_count(self) -> int:
        """
        Кол-во блюд в меню
        """
        count = sum(submenu.dishes_count for submenu in self.submenus)
        return count

    def as_dict(self):
        """
        Преобразование модели в словарь (для кэширования в Redis)
        """
        model_dict = super().as_dict()
        model_dict["submenus_count"] = self.submenus_count
        model_dict["dishes_count"] = self.dishes_count

        return model_dict
