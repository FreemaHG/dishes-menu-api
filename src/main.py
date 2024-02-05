from fastapi import FastAPI

from src.urls import register_routers
from src.utils.exceptions import CustomApiException, custom_api_exception_handler

app = FastAPI(title='DishesApi', debug=True)


# Регистрация URL
register_routers(app)

# Регистрация кастомного исключения
app.add_exception_handler(CustomApiException, custom_api_exception_handler)
