import pytest


@pytest.fixture(scope='class')
async def invalid_data() -> dict:
    """
    Невалидные данные для добавления нового меню / подменю
    """
    return {'title': 123, 'description': 456}
