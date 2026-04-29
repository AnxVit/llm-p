from fastapi import APIRouter, Depends

from app.schemas.chat import ChatRequest, ChatResponse, ChatHistory, DeletedResponse
from app.api.deps import get_current_user_id, get_chat_usecases
from app.usecases.chat import ChatUsecase

router_chat = APIRouter(prefix="/chat", tags=["chat"])

@router_chat.post("", response_model=ChatResponse)
async def send_message(req: ChatRequest, user_id: int = Depends(get_current_user_id), usecase: ChatUsecase = Depends(get_chat_usecases)):
    response = await usecase.ask(req, user_id)
    return response


@router_chat.get("/history", response_model=ChatHistory)
async def get_history(user_id: int = Depends(get_current_user_id), usecase: ChatUsecase = Depends(get_chat_usecases)):
    response = await usecase.get_history(user_id)
    return response

@router_chat.delete("/history", response_model=DeletedResponse)
async def delete_history(user_id: int = Depends(get_current_user_id), usecase: ChatUsecase = Depends(get_chat_usecases)):
    response = await usecase.delete_history(user_id)
    return response
