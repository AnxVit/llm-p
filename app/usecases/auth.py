from typing import Optional, Protocol

from app.core.errors import ConflictError, UnauthorizedError, NotFoundError
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user import UserPublic
from app.schemas.auth import TokenResponse
from app.db.models import Users

class UserRepo(Protocol):
    async def get_user_by_id(self, id: int) -> Optional[Users]: ...
    async def get_user_by_email(self, email: str) -> Optional[Users]: ...
    async def add_user(self, email: str, password_hash, role: str | None) -> Users: ...


class AuthUsecase:
    def __init__(self, repo: UserRepo):
        self._repo = repo
    
    async def register(self, email: str, password: str) -> None:
        """
        Регистрация нового пользователя в системе.
        Args:
            email: str - Email адрес пользователя
            password: str - Пароль для аккаунта
        Return:
            UserPublic: Общедоступные данные зарегистрированного пользователя
        """
        user = await self._repo.get_user_by_email(email)
        if user:
            raise ConflictError(message="email already exists")
        
        hashed_password = hash_password(password)
    
        user = await self._repo.add_user(email, hashed_password, None)
        return UserPublic.model_validate(user)

    async def login(self, email: str, password: str) -> str:
        """
        Аутентификация пользователя и выдача JWT токена доступа.
        Args:
            email: str - Email адрес пользователя
            password: str - Пароль в открытом виде
        Return:
            TokenResponse: Объект с access token
        """
        user = await self._repo.get_user_by_email(email)
        if not user:
            raise UnauthorizedError(message="user does't exists")
                
        if not verify_password(password, user.password_hash):
            raise UnauthorizedError(message="wrong password")
        
        token = create_access_token(str(user.id), user.role)

        return TokenResponse(access_token=token)
    
    async def user_by_id(self, id: int) -> UserPublic: 
        """
        Получение публичных данных пользователя по ID.
        Args:
            id: int - Уникальный идентификатор пользователя
        Return:
            UserPublic: Общедоступные данные пользователя
        """
        user = await self._repo.get_user_by_id(id)
        if not user:
            raise NotFoundError(message="user not found")

        return UserPublic.model_validate(user)