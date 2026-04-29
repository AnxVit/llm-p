from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose.exceptions import ExpiredSignatureError, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.users import UserRepository
from app.repositories.chat_messages import ChatRepository
from app.db.session import AsyncSessionLocal
from app.core.security import decode_token
from app.usecases.auth import AuthUsecase
from app.usecases.chat import ChatUsecase
from app.services.openrouter_client import OpenRouterClient

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор сессии базы данных для Dependency Injection.
    Args: -
    Return:
        AsyncGenerator[AsyncSession, None]: Асинхронный генератор сессии SQLAlchemy
    """
    async with AsyncSessionLocal() as conn:
        yield conn

async def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """
    Получение репозитория пользователя.
    Args:
        db: AsyncSession - Сессия базы данных
    Return:
        UserRepository: Экземпляр репозитория для работы с пользователями
    """
    return UserRepository(db)

async def get_chat_repository(db: AsyncSession = Depends(get_db)) -> ChatRepository:
    """
    Получение репозитория чата.
    Args:
        db: AsyncSession - Сессия базы данных
    Return:
        ChatRepository: Экземпляр репозитория для работы с сообщениями
    """
    return ChatRepository(db)

async def get_auth_usecases(repo: UserRepository = Depends(get_user_repository)) -> AuthUsecase:
    """
    Получение usecase для аутентификации.
    Args:
        repo: UserRepository - Репозиторий пользователя
    Return:
        AuthUsecase: Экземпляр usecase для аутентификации
    """
    return AuthUsecase(repo)

async def get_openrouter_client() -> AsyncGenerator[OpenRouterClient]:
    """
    Генератор клиента OpenRouter с управлением контекстом.
    Args: - 
    Return:
        AsyncGenerator[OpenRouterClient]: Асинхронный генератор клиента OpenRouter
    """
    async with OpenRouterClient() as client:
        yield client


async def get_chat_usecases(
        repo: ChatRepository = Depends(get_chat_repository), 
        service: OpenRouterClient = Depends(get_openrouter_client)
) -> ChatUsecase:
    """
    Получение usecase для работы с чатом.
    Args:
        repo: ChatRepository - Репозиторий чата
        service: OpenRouterClient - Клиент OpenRouter API
    Return:
        ChatUsecase: Экземпляр usecase для работы с чатом
    """
    return ChatUsecase(repo, service)

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """
    Извлечение ID текущего пользователя из JWT токена.
    Args:
        token: str - JWT токен из заголовка Authorization
    Return:
        int: ID пользователя из поля sub токена
    """
    try:
        payload = decode_token(token)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token" + str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has no subject")

    return int(sub)