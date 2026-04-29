from passlib.context import CryptContext
from typing import Any, Dict
import time
from jose import jwt

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _now() -> int:
    return int(time.time())

def hash_password(password: str) -> str:
    """
    Хеширование пароля с использованием bcrypt.
    Args:
        password: str - Пароль в открытом виде
    Return:
        str: Хешированный пароль
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Проверка соответствия пароля его хешу.
    Args:
        password: str - Пароль в открытом виде
        hashed_password: str - Хеш пароля из базы данных
    Return:
        bool: True если пароль совпадает, False если нет
    """
    return pwd_context.verify(password, hashed_password)


def create_access_token(sub: str, role: str) -> str:
    """
    Создание JWT токена доступа для пользователя.
    Args:
        sub: str - Уникальный идентификатор пользователя (subject)
        role: str - Роль пользователя для авторизации
    Return:
        str: Закодированный JWT токен
    """
    payload = {
        "sub": sub,
        "role": role,
        "iat": _now(),
        "exp": _now() + settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG]) 