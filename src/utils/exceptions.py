from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


class CustomApiException(HTTPException):
    """
    Кастомная ошибка для быстрого вызова исключений
    """

    pass


async def custom_api_exception_handler(request: Request, exc: HTTPException):
    """
    Кастомный обработчик ошибок для CustomApiException
    """

    return JSONResponse(
        {'detail': str(exc.detail)},
        status_code=exc.status_code,
    )
