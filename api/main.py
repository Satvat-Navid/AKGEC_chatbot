import logging
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import ChatRequest
from .agents import get_context, summerize, response, GENERAL_MODEL

# Configure logging to work with Vercel
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# This 'app' variable is what Vercel looks for
app = FastAPI(title="AKGEC Chatbot API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.post("/")
@app.post("/chat")
def chat(request: ChatRequest):
    request_start_time = time.time()
    logger.info("--- New Chat Request Received ---")
    logger.info(f"User Message: '{request.message}'")

    try:
        # Step 1: Summarize history (if it exists)
        history_summary = ""
        if request.history:
            logger.info("STEP 1: Summarizing conversation history...")
            history_summary = summerize(GENERAL_MODEL, request.history, 500)
            logger.info("STEP 1: History summarized.")
        
        # Step 2: Retrieve Context from Pinecone
        logger.info("STEP 2: Retrieving context from vector database...")
        db_context = get_context(request.message)
        logger.info("STEP 2: Context retrieved.")

        # Step 3: Generate Final Response from Groq
        logger.info("STEP 3: Generating final response...")
        final_reply = response(GENERAL_MODEL, request.message, db_context, history_summary)
        logger.info("STEP 3: Final response generated.")

        total_duration = round(time.time() - request_start_time, 2)
        logger.info(f"--- Request successfully processed in {total_duration}s ---")

        return {
            "reply": final_reply,
            "context_used": db_context,
            "history": history_summary,
            "processing_time": total_duration
        }

    except Exception as e:
        logger.error("!!! An unexpected error occurred !!!", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error occurred.")