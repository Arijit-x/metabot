import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from agent import run_agent
from openmetadata import OpenMetadataClient
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="MetaBot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto-login to sandbox — no token needed, no Docker needed
om_client = OpenMetadataClient(
    base_url=os.getenv("OM_BASE_URL", "https://sandbox.open-metadata.org"),
    token=os.getenv("OM_TOKEN", ""),   # leave blank to auto-login
)


class Message(BaseModel):
    role: str
    text: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []


class ChatResponse(BaseModel):
    response: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "MetaBot",
        "openmetadata": os.getenv("OM_BASE_URL", "https://sandbox.open-metadata.org"),
        "auth": "auto-login (no bot token needed)",
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        gemini_history = []
        for msg in (req.history or []):
            gemini_history.append({
                "role": msg.role,
                "parts": [{"text": msg.text}]
            })
        response_text = run_agent(req.message, om_client, gemini_history)
        return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/suggestions")
def get_suggestions():
    return {
        "suggestions": [
            "Which tables contain customer data?",
            "Who owns the orders table?",
            "Show me all tables updated recently",
            "What columns does the dim_customer table have?",
            "Show lineage for the fact_order table",
            "Which tables have PII tags?",
        ]
    }
