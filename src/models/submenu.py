from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.abc_model import BaseABC
from src.models.dish import Dish


class Submenu(BaseABC):
    """
    Модель для хранения записей о подменю
    """
    __tablename__ = "submenu"

    menu_id: Mapped[int] = mapped_column(ForeignKey("menu.id"))
    dishes: Mapped[List["Dish"]] = relationship(backref="submenu", cascade="all, delete")

    # TODO Прописать метод для вывода кол-ва всех блюд в подменю (либо вынести в сервисы?)
    # def dishes_count(self):
    #     pass
