from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest
from agents import get_context, summerize, response, GENERAL_MODEL, TOOL_MODEL
import time

app = FastAPI(title="AKGEC Chatbot API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can specify domains instead
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/chat")
def chat(request: ChatRequest):
    start_time = time.time()

    history = summerize(GENERAL_MODEL, request.history, 500) if request.history else ""
    db_context = get_context(request.message)
    reply = response(GENERAL_MODEL, request.message, db_context, history)

    end_time = time.time()
    return {
        "reply": reply,
        "context_used": db_context,
        "history": history,
        "processing_time": round(end_time - start_time, 2)
    }
