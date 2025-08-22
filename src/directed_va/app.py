from fastapi import FastAPI, HTTPException, Request
from chatbot import *
from components import LearningAnalyzer

app = FastAPI(
    title="DirectEd Educational Assistant",
    description="AI-powered assistant for DirectEd"
)
