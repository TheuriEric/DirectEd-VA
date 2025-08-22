# from fastapi import FastAPI
# from .core.api.endpoints import router as api_router
# from langserve import add_routes

# app = FastAPI(
#     title="DirectEd Educational API",
#     description="Backend for the DirectEd educational platform.",
#     version="1.0.0"
# )

# app.include_router(api_router)

# @app.get("/")
# async def root():
#     return {"message": "DirectEd API is running. Visit /docs for more."}

from fastapi import FastAPI
from langserve import add_routes
from langchain.schema.runnable import RunnableLambda
from pydantic import BaseModel
from .core.chatbot import run_educational_assistant
from .core.components import LearningAnalyzer

class AssistantInput(BaseModel):
    request: str
    user_id: str = "anonymous"
    is_instructor: bool = False

educational_chain = RunnableLambda(
    lambda inp: run_educational_assistant(
        request=inp['request'],  
        user_id=inp['user_id'],      
        analyzer=LearningAnalyzer(),
        is_instructor=inp['is_instructor']  
    )
).with_types(input_type=AssistantInput)

app = FastAPI(
    title="DirectEd Educational API",
    description="Backend for the DirectEd educational platform.",
    version="1.0.0"
)

add_routes(app, educational_chain, path="/assistant")

@app.get("/")
async def root():
    return {"message": "DirectEd API is running. Visit /docs or /playground/assistant"}
