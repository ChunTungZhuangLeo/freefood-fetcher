"""
Ara Hackathon - Main Application
Build your own AI Personal Computer/Assistant

Run with: uvicorn main:app --reload
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

from agents.assistant import AIAssistant, StudyBuddyAgent, EmailTriageAgent

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Personal Assistant",
    description="Your personal AI computer built at Ara x JHU Hackathon",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
general_assistant = AIAssistant()
study_buddy = StudyBuddyAgent()
email_agent = EmailTriageAgent()


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    agent: str = "general"  # general, study, email


class ChatResponse(BaseModel):
    response: str
    agent: str


class AnalyzeRequest(BaseModel):
    text: str
    task: str


class QuizRequest(BaseModel):
    topic: str
    num_questions: int = 5


# API Endpoints
@app.get("/")
async def root():
    """Serve the main page."""
    return HTMLResponse(content=open("frontend/index.html").read())


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with an AI assistant."""
    agents = {
        "general": general_assistant,
        "study": study_buddy,
        "email": email_agent
    }

    agent = agents.get(request.agent, general_assistant)
    response = agent.chat(request.message)

    return ChatResponse(response=response, agent=request.agent)


@app.post("/api/summarize")
async def summarize(request: AnalyzeRequest):
    """Summarize text content."""
    summary = study_buddy.summarize_notes(request.text)
    return {"summary": summary}


@app.post("/api/quiz")
async def generate_quiz(request: QuizRequest):
    """Generate a quiz on a topic."""
    quiz = study_buddy.generate_quiz(request.topic, request.num_questions)
    return {"quiz": quiz}


@app.post("/api/email/triage")
async def triage_email(request: AnalyzeRequest):
    """Categorize and triage an email."""
    result = email_agent.categorize_email(request.text)
    return {"triage": result}


@app.post("/api/email/reply")
async def draft_email_reply(request: AnalyzeRequest):
    """Draft a reply to an email."""
    reply = email_agent.draft_reply(request.text, request.task)
    return {"reply": reply}


@app.post("/api/clear")
async def clear_conversation(agent: str = "general"):
    """Clear conversation history."""
    agents = {
        "general": general_assistant,
        "study": study_buddy,
        "email": email_agent
    }
    agents.get(agent, general_assistant).clear_history()
    return {"status": "cleared"}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "AI Assistant is running!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
