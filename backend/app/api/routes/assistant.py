from fastapi import APIRouter

from app.schemas.assistant import ChatRequest, ChatResponse
from app.services.assistant_service import AssistantService


router = APIRouter(
    prefix="/api/assistant",
    tags=["Assistant"]
)

assistant_service = AssistantService()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return assistant_service.chat(request.message)