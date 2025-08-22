from fastapi import FastAPI
from core.api.endpoints import router as api_router
from langserve import add_routes

app = FastAPI(
    title="DirectEd Educational API",
    description="Backend for the DirectEd educational platform.",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/assistant")

@app.get("/")
async def root():
    return {"message": "DirectEd API is running. Visit /docs for more."}