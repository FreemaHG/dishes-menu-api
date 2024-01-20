from sqlalchemy import ForeignKey, Float, FLOAT
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.models.abc_model import BaseABC


class Dish(BaseABC):
    """
    Модель для хранения записей о блюде
    """
    __tablename__ = "dish"

    # TODO Создать и применить миграции (проверить!)
    price: Mapped[float] = mapped_column(Float(precision=2))
    submenu_id: Mapped[int] = mapped_column(ForeignKey("submenu.id"))
