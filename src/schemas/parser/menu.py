from pydantic import BaseModel

from src.schemas.parser.base import BaseParserSchema
from src.schemas.parser.submenu import SubmenuParserSchema


class MenuParserSchema(BaseParserSchema):
    """
    Схема для проверки распарсенных данных о меню
    """

    submenus: list[SubmenuParserSchema] | None


class MenusListParserSchema(BaseModel):
    """
    Схема для проверки распарсенных данных о списке меню
    """

    menus: list[MenuParserSchema] | None
