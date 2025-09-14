import logging
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from models import ChatRequest
from agents import get_context, summerize, response, GENERAL_MODEL

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="AKGEC Chatbot API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/chat")
def chat(request: ChatRequest):
    logger.info(f"Received query: {request.message}")
    try:
        history = summerize(GENERAL_MODEL, request.history, 500) if request.history else ""
        db_context = get_context(request.message)
        reply = response(GENERAL_MODEL, request.message, db_context, history)
        return {
            "reply": reply,
            "context_used": db_context,
            "history": history,
        }
    except Exception as e:
        logger.error("!!! An unexpected error occurred !!!", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

# This is crucial part for serving the frontend
app.mount("/", StaticFiles(directory="public", html = True), name="static")