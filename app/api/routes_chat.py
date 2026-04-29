from fastapi import APIRouter, Depends

from app.schemas.chat import ChatRequest, ChatResponse, ChatHistory, DeletedResponse
from app.api.deps import get_current_user_id, get_chat_usecases
from app.usecases.chat import ChatUsecase

router_chat = APIRouter(prefix="/chat", tags=["chat"])

@router_chat.post("", response_model=ChatResponse)
async def send_message(req: ChatRequest, user_id: int = Depends(get_current_user_id), usecase: ChatUsecase = Depends(get_chat_usecases)):
    """
    Отправка сообщения в LLM и получение ответа.
    Args:
        req: ChatRequest - Запрос с полем prompt и настройками
        user_id: int - ID пользователя из JWT токена
        usecase: ChatUsecase - UseCase для работы с чатом
    Return:
        ChatResponse: Ответ от LLM
    """
    response = await usecase.ask(req, user_id)
    return response


@router_chat.get("/history", response_model=ChatHistory)
async def get_history(user_id: int = Depends(get_current_user_id), usecase: ChatUsecase = Depends(get_chat_usecases)):
    """
    Получение истории сообщений текущего пользователя.
    Args:
        user_id: int - ID пользователя из JWT токена
        usecase: ChatUsecase - UseCase для работы с чатом
    Return:
        ChatHistory: Объект со списком сообщений пользователя
    """
    response = await usecase.get_history(user_id)
    return response

@router_chat.delete("/history", response_model=DeletedResponse)
async def delete_history(user_id: int = Depends(get_current_user_id), usecase: ChatUsecase = Depends(get_chat_usecases)):
    """
    Удаление всей истории сообщений текущего пользователя.
    Args:
        user_id: int - ID пользователя из JWT токена
        usecase: ChatUsecase - UseCase для работы с чатом
    Return:
        DeletedResponse: Объект с информацией о результате удаления
    """
    response = await usecase.delete_history(user_id)
    return response
