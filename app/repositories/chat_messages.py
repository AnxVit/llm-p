from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.db.models import ChatMessage
from app.repositories.decorator import handle_db_errors

class ChatRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    @handle_db_errors
    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        """
        Добавление нового сообщения в историю диалога.
        Args:
            user_id: int - ID пользователя
            role: str - Роль отправителя (user/assistant)
            content: str - Текст сообщения
        Return:
            ChatMessage: Объект сохранённого сообщения с присвоенным ID
        """
        msg = ChatMessage(user_id=user_id, role=role, content=content)
        self._session.add(msg)

        await self._session.commit()
        await self._session.refresh(msg)
        return msg            
    
    @handle_db_errors
    async def get_messages_by_user(self, user_id: int, count_msg: int | None = None) -> list[ChatMessage]:
        """
        Получение истории сообщений пользователя.
        Args:
            user_id: int - ID пользователя
            count_msg: int | None - Максимальное количество последних сообщений (опционально)
        Return:
            list[ChatMessage]: Список сообщений в хронологическом порядке
        """
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
        )

        if count_msg:
            stmt = stmt.limit(count_msg)

        result = await self._session.execute(stmt)
        messages = result.scalars().all()

        return list(reversed(messages))
    
    @handle_db_errors
    async def delete_history_by_user(self, user_id:int) -> int:
        """
        Удаление всех сообщений пользователя.
        Args:
            user_id: int - ID пользователя
        Return:
            int: Количество удалённых сообщений
        """
        stmt = (
            delete(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .returning(ChatMessage.id)
        )

        result = await self._session.execute(stmt)
        deleted_ids = result.scalars().all()
        await self._session.commit()
        
        return len(deleted_ids)
    
    