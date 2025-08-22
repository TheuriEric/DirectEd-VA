from fastapi import APIRouter, HTTPException
from core.schemas.chat_models import (
    ChatRequest, 
    ChatResponse, 
    ContentGenerateRequest,
    ContentGenerateResponse,
    AnalyticsResponse
)
from core.services.educational_assistant import handle_unified_chat, generate_content, get_user_analytics

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def unified_conversation_interface(request: ChatRequest):
    """
    Handles a unified conversation interface for tutoring and quick actions like quizzes.
    """
    try:
        response_data = handle_unified_chat(request.request_text, request.user_id, request.is_instructor)
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")

@router.post("/content/generate", response_model=ContentGenerateResponse)
async def generate_specific_content(request: ContentGenerateRequest):
    """
    Creates quizzes or flashcards for a specific subject.
    """
    try:
        content_output = generate_content(request.subject, request.request_type)
        return {"subject": request.subject, "content": content_output}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")

@router.get("/analytics/{user_id}", response_model=AnalyticsResponse)
async def get_analytics_for_user(user_id: str):
    """
    Retrieves the learning analytics for a specific user.
    """
    profile = get_user_analytics(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found.")
    return AnalyticsResponse(
        user_id=user_id,
        completed_quizzes=profile.get("completed_quizzes", []),
        struggling_topics=profile.get("struggling_topics", [])
    )