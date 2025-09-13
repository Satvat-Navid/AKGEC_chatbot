from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import ChatRequest
from .agents import get_context, summerize, response, GENERAL_MODEL, TOOL_MODEL
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AKGEC Chatbot API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
def chat(request: ChatRequest):
    start_time = time.time()
    logger.info(f"Received request: {request.message}")

    try:
        # Step 1: Summarize history (if it exists)
        history = ""
        if request.history:
            logger.info("Summarizing history...")
            history = summerize(GENERAL_MODEL, request.history, 500)
            logger.info("History summarized.")

        # Step 2: Get context from Pinecone
        logger.info("Getting context from Pinecone...")
        db_context = get_context(request.message)
        logger.info("Context retrieved.")

        # Step 3: Get the final response from Groq
        logger.info("Getting response from Groq...")
        reply = response(GENERAL_MODEL, request.message, db_context, history)
        logger.info("Response received.")

        end_time = time.time()
        processing_time = round(end_time - start_time, 2)
        logger.info(f"Request processed in {processing_time} seconds.")

        return {
            "reply": reply,
            "context_used": db_context,
            "history": history,
            "processing_time": processing_time
        }

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error occurred.")