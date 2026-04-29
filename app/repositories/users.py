from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import Users, ROLE_USER
from app.repositories.decorator import handle_db_errors

class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    @handle_db_errors
    async def get_user_by_id(self, id: int) -> Users | None:
        stmt = select(Users).where(Users.id == id)

        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()

        return user
    
    @handle_db_errors
    async def get_user_by_email(self, email: str) -> Users | None:
        stmt = select(Users).where(Users.email == email)

        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()

        return user
    
    @handle_db_errors
    async def add_user(self, email: str, password_hash, role: str | None) -> Users:
        if role is None:
            role = ROLE_USER
        user = Users(email=email, password_hash=password_hash, role=role)

        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)

        return user