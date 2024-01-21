from typing import List
from sqlalchemy.orm import Mapped, relationship

from src.models.abc_model import BaseABC
from src.models.submenu import Submenu


class Menu(BaseABC):
    """
    Модель для хранения записей о меню
    """

    __tablename__ = "menu"

    submenus: Mapped[List["Submenu"]] = relationship(backref="menu", cascade="all, delete-orphan")

    # TODO Прописать метод для вывода кол-ва всех блюд в меню (либо вынести в сервисы?)
    # def submenus_count(self):
    #     pass
