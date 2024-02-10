from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.util.preloaded import orm

from src.models.abc_model import BaseABC


class Dish(BaseABC):
    """
    Модель для хранения записей о блюде
    """

    __tablename__ = 'dish'

    price: Mapped[float] = mapped_column(Float(precision=2))
    discount: Mapped[int] = mapped_column(Integer, default=0)
    submenu_id: Mapped[int] = mapped_column(ForeignKey('submenu.id'))

    @orm.validates('discount')
    def validate_discount(self, key, value):
        """
        Проверка скидки перед сохранением в БД
        """
        if not 0 <= value <= 90:
            raise ValueError(f'Невалидное значение скидки: {value}')
        return value

    def as_dict(self):
        """
        Преобразование модели в словарь (для кэширования в Redis)
        """
        model_dict = super().as_dict()
        model_dict['submenu_id'] = str(model_dict['submenu_id'])

        return model_dict
