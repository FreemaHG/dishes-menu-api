from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.ext.hybrid import hybrid_property
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

    @hybrid_property
    def discount_price(self) -> int:
        """
        Цена с учетом скидки
        """
        if self.discount > 0:
            discount = self.price * (self.discount / 100)
            new_price = round(self.price - discount, 2)

            return new_price

        return round(self.price, 2)

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
        model_dict['price'] = str(self.discount_price)

        return model_dict
