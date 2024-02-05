from fastapi import FastAPI

from src.urls import register_routers
from src.utils.exceptions import CustomApiException, custom_api_exception_handler

app = FastAPI(title='DishesApi', debug=True)

# TODO Очищать кэш полностью при каждом новом запуске сервера
# TODO автоматическая проверка, что не будет лагов при запуске API с новой БД

# Регистрация URL
register_routers(app)

# Регистрация кастомного исключения
app.add_exception_handler(CustomApiException, custom_api_exception_handler)
