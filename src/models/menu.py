from typing import List

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models.abc_menu import BaseABC
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
