from typing import Dict, Any
from ..chatbot import analyzer, run_educational_assistant, content_generator
from ..schemas.chat_models import ChatRequest, ContentGenerateRequest

def handle_unified_chat(request: ChatRequest) -> Dict[str, Any]:
    return run_educational_assistant(
        request.request_text, 
        request.user_id, 
        analyzer, 
        request.is_instructor
    )

def generate_content(request: ContentGenerateRequest) -> str:
    if request.request_type.lower() == "quiz":
        return content_generator.generate_quiz(request.subject)
    elif request.request_type.lower() == "flashcard":
        return f"Placeholder flashcards for {request.subject}."
    else:
        raise ValueError("Invalid content type. Choose 'quiz' or 'flashcard'.")

def get_user_analytics(user_id: str) -> Dict[str, Any]:
    return analyzer.get_profile(user_id)