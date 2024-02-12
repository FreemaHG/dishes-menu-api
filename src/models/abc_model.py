import uuid

from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class BaseABC(Base):
    """
    Абстрактная модель для описания основных полей моделей
    """

    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    title: Mapped[str] = mapped_column(String(280))
    description: Mapped[str] = mapped_column(Text)

    def as_dict(self) -> dict:
        """
        Преобразование модели в словарь (для кэширования в Redis)
        """
        model_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        model_dict['id'] = str(model_dict['id'])

        return model_dict
