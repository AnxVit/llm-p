from __future__ import annotations

from dataclasses import dataclass, field

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

@dataclass
class AppException(Exception):
    status_code: int = 400
    error_code: str = "APP_ERROR"
    message: str = "Ошибка приложения"
    meta: dict = field(default_factory=dict)
    
    def __str__(self)-> str:
        return f"{self.error_code}: {self.message}"
    
@dataclass
class ConflictError(AppException):
    status_code: int = 409
    error_code: str = "CONFLICT"
    message: str = "Конфликт состояния данных"

@dataclass
class UnauthorizedError(AppException):
    status_code: int = 401
    error_code: str = "UNAUTHORIZED"
    message: str = "Не авторизован"

@dataclass
class PermissionDeniedError(AppException):
    status_code: int = 403
    error_code: str = "PERMISION_DENIED"
    message: str = "Нет доступа"

@dataclass
class NotFoundError(AppException):
    status_code: int = 404
    error_code: str = "NOT_FOUND"
    message: str = "Ресурс не найден"

@dataclass
class ServiceUnavailableError(AppException):
    error_code: str = "SERVICE_UNAVAILABLE"
    message: str = "Сервис временно недоступен"
    status_code: int = 503

    

def register_exception_handlers(app):
    @app.exception_handler(AppException)
    async def app_error_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error_code": exc.error_code,
                "message": exc.message,
                "meta": exc.meta,
                "path": request.url.path,
            },
        )
    
    @app.exception_handler(Exception)
    async def unexpected_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "error_code": "INTERNAL_ERROR",
                "message": "Внутренняя ошибка сервера",
                "path": request.url.path,
            },
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        simplified_errors = []

        for error in exc.errors():
            field_path = [
                str(loc) for loc in error["loc"] if loc not in ("body", "query", "path")
            ]
            field = ".".join(field_path)
            simplified_errors.append(
                {
                    "field": field,
                    "message": error["msg"],
                }
            )

        return JSONResponse(
            status_code=422,
            content={
                "error_code": "VALIDATION_ERROR",
                "message": "Некорректные данные запроса",
                "errors": simplified_errors,
                "path": request.url.path,
            },
        )