from typing import Dict, Protocol, Union

from app.db.models import ChatMessage, MESSAGE_ROLE_ASSISTANT, MESSAGE_ROLE_USER
from app.core.config import settings
from app.schemas.chat import ChatRequest, ChatResponse, ChatHistory, Message, DeletedResponse

class ChatRepo(Protocol):
    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage: ...
    async def get_messages_by_user(self, user_id: int, count_msg: int | None) -> list[ChatMessage]: ...
    async def delete_history_by_user(self, user_id:int) -> int: ...

class Service(Protocol):
    async def post_chat(self, req: Dict[str, Union[str, float, list]]) -> str: ...


class ChatUsecase:
    def __init__(self, repo: ChatRepo, service: Service):
        self._repo = repo
        self._service = service

    async def ask(self, req: ChatRequest, user_id: int) -> ChatResponse:
        messages = await self._repo.get_messages_by_user(user_id, req.max_history)

        openAIReq = convert_message_in_openai_format(messages, req)
        content = await self._service.post_chat(openAIReq)
        
        await self._repo.add_message(user_id, MESSAGE_ROLE_USER, req.prompt)
        await self._repo.add_message(user_id, MESSAGE_ROLE_ASSISTANT, content)
        return ChatResponse(answer=content)

        
    async def get_history(self, user_id: int) -> ChatHistory:
        messages = await self._repo.get_messages_by_user(user_id)

        chat_messages = [Message.model_validate(msg) for msg in messages]

        return ChatHistory(messages=chat_messages)

    async def delete_history(self, user_id: int) -> DeletedResponse:
        count_deleted_rows = await self._repo.delete_history_by_user(user_id)
        if count_deleted_rows == 0:
            return DeletedResponse(message="empty history")
        return DeletedResponse(message=f"successfully delete {count_deleted_rows}")


def convert_message_in_openai_format(messages: list[ChatMessage], req: ChatRequest) -> Dict[str, Union[str, float, list]]:
    openAIMessages = []
    if req.system is not None:
        openAIMessages.append({
            "role": "system",
            "content": req.system
        })

    for msg in messages:
        chatMsg = {
            "role": msg.role,
            "content": msg.content
        }
        openAIMessages.append(chatMsg)

    openAIMessages.append({
        "role": "user",
        "content": req.prompt
    })

    openAIReq = {
        "model": settings.OPENROUTER_MODEL,
        "messages": openAIMessages
    }
    if req.temperature is not None:
        openAIReq["temperature"] = req.temperature

    return openAIReq
