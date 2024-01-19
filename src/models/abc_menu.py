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

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title: Mapped[str] = mapped_column(String(280))
    description: Mapped[str] = mapped_column(Text)

    # FIXME Возможно нужно...
    # Отключаем проверку строк, тем самым убирая уведомление, возникающее при удалении несуществующей строки
    # __mapper_args__ = {"confirm_deleted_rows": False}
