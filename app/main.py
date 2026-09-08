from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.qa import build_answer


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="RulebookAI",
    version="1.0.0",
    description=(
        "AI-powered university rulebook assistant "
        "that retrieves rules and identifies contradictions."
    )
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# MODELS
# ============================================================

class QuestionRequest(BaseModel):
    question: str


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "name": "RulebookAI",
        "status": "running",
        "message": "University rulebook assistant is ready."
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# ASK
# ============================================================

@app.post("/ask")
def ask_question(request: QuestionRequest):

    return build_answer(
        request.question
    )