from fastapi import FastAPI, HTTPException, Request
from typing import Optional
from langserve import add_routes
from chatbot import *
from components import LearningAnalyzer
from src.core.schemas.chat_models import ChatRequest, ChatResponse
import uvicorn

app = FastAPI(
    title="DirectEd Educational Assistant",
    description="AI-powered assistant for DirectEd"
)

@app.get("/")
async def root():
    return {"Message": "Loaded successfully ✅! "}

@app.post("/api/assistant/chat", response_model=ChatResponse)
async def handle_user_request(request: ChatRequest):
    try:
        response_data = run_educational_assistant(
            request = request.request_text,
            user_id = request.user_id,
            analyzer = analyzer,
            is_instructor = request.is_instructor
        )
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, details=f"An internal error occured: {e}")
    

async def get_next_curriculum_topic(user_id: str) ->Optional[str]:
    profile = analyzer.get_profile(user_id=user_id)
    if profile["struggling_topics"]:
        return f"Next suggested content: {profile['struggling_topics'][0]}"
    curriculum_topics = ["Langchain", "LLM reasoning", "Design"]
    completed_topics = profile["completed_quizzes"]

    for topic in curriculum_topics:
        if topic not in completed_topics:
            return f"explain {topic} to me in detail."
        
    return None

@app.post("/api/assistant/adaptive_learning", response_model=ChatResponse)
async def get_adaptive_content(user_id: str):
    adaptive_request = get_next_curriculum_topic(user_id=user_id)
    if not adaptive_request:
        return "Congratulations🎉s🎉 You have gone through the whole curriculum"
    print(f"Adaptive Learning System is generating content for: '{adaptive_request}'")
    
    try:
        response_data = run_educational_assistant(
            request=adaptive_request,
            user_id=user_id,
            analyzer=analyzer,
            is_instructor=False
        )
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")

