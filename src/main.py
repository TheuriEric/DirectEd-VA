from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from langchain.schema.runnable import RunnableLambda
from pydantic import BaseModel
from .core.chatbot import run_educational_assistant
from .core.components import LearningAnalyzer

from pydantic import BaseModel
from typing import List, Dict, Any


# Define output schema
class AssistantOutput(BaseModel):
    user_type: str
    content_type: str
    output: str
    updated_profile: Dict[str, Any]  


class AssistantInput(BaseModel):
    request: str
    user_id: str = "anonymous"
    is_instructor: bool = False

educational_chain = RunnableLambda(
    lambda inp: run_educational_assistant(
        request=inp.get("request", ""),
        user_id=inp.get("user_id", "anonymous"),
        analyzer=LearningAnalyzer(),
        is_instructor=inp.get("is_instructor", False)
    )
).with_types(
    input_type=AssistantInput,
    output_type=AssistantOutput
)


app = FastAPI(
    title="DirectEd Educational API",
    description="Backend for the DirectEd educational platform.",
    version="1.0.0"
)

origins = [
    "*"
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_methods = ["*"],
                   allow_credentials = True,
                   allow_headers = ["*"]
                   )

add_routes(app, educational_chain, path="/assistant")

@app.get("/")
async def root():
    return {"message": "DirectEd API is running. Visit /docs or /playground/assistant"}
