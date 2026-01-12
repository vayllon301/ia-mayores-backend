import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.chain import chat

app = FastAPI(
    title="IA Mayores Backend",
    description="Chatbot API with weather integration for seniors",
    version="1.0.0"
)

# Configure CORS for Azure
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "IA Mayores Backend is running",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    """Azure health check endpoint"""
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    """Main chat endpoint"""
    reply = chat(req.message)
    return {"response": reply}