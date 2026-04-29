from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserPublic
from app.schemas.auth import RegisterRequest, TokenResponse
from app.api.deps import get_auth_usecases, get_current_user_id
from app.usecases.auth import AuthUsecase

router_auth = APIRouter(prefix="/auth", tags=["auth"])

@router_auth.post("/register", response_model=UserPublic)
async def register(req: RegisterRequest, usecase: AuthUsecase = Depends(get_auth_usecases)):
    """
    Регистрация нового пользователя.
    Args:
        req: RegisterRequest - Запрос с email и паролем
        usecase: AuthUsecase - UseCase для аутентификации
    Return:
        UserPublic: Публичные данные зарегистрированного пользователя
    """
    response = await usecase.register(req.email, req.password)
    return response

@router_auth.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), usecase: AuthUsecase = Depends(get_auth_usecases)):
    """
    Аутентификация пользователя и получение токена.
    Args:
        form_data: OAuth2PasswordRequestForm - Форма с username(email) и password
        usecase: AuthUsecase - UseCase для аутентификации
    Return:
        TokenResponse: JWT токен доступа
    """
    response = await usecase.login(form_data.username, form_data.password)
    return response

@router_auth.get("/me", response_model=UserPublic)
async def me(id: int = Depends(get_current_user_id), usecase: AuthUsecase = Depends(get_auth_usecases)):
    """
    Получение информации о текущем авторизованном пользователе.
    Args:
        id: int - ID пользователя из JWT токена
        usecase: AuthUsecase - UseCase для аутентификации
    Return:
        UserPublic: Публичные данные текущего пользователя
    """
    response = await usecase.user_by_id(id)
    return response