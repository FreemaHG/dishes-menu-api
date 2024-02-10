from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.abc_model import BaseABC
from src.models.dish import Dish


class Submenu(BaseABC):
    """
    Модель для хранения записей о подменю
    """

    __tablename__ = 'submenu'

    menu_id: Mapped[int] = mapped_column(ForeignKey('menu.id'))
    dishes: Mapped[list['Dish']] = relationship(
        backref='submenu', cascade='all, delete'
    )

    @hybrid_property
    def dishes_count(self) -> int:
        """
        Подсчет кол-ва блюд в подменю
        :return: кол-во блюд в подменю
        """
        return len(self.dishes)

    def as_dict(self) -> dict:
        """
        Преобразование модели в словарь (для кэширования в Redis)
        :return: словарь с данными
        """
        model_dict = super().as_dict()
        model_dict['menu_id'] = str(model_dict['menu_id'])
        model_dict['dishes_count'] = self.dishes_count

        return model_dict

    def as_all_dict(self) -> dict:
        """
        Преобразование модели в словарь (для кэширования в Redis) с данными о вложенных блюдах
        :return: словарь с данными
        """
        data = self.as_dict()
        data['dishes'] = [dish.as_dict() for dish in self.dishes]

        return data
