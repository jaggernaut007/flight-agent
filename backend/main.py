from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
import traceback
import os

LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
LOG_PATH = os.path.join(LOG_DIR, 'backend.log')
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import the chat service
from services.chat_service import chat_service

# Initialize FastAPI app
app = FastAPI(title="Travel Assistant API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chat Models
class ChatMessage(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    context: Optional[Dict[str, Any]] = None

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "ok", "message": "Travel Assistant API is running"}

# Exception handler for the chat endpoint
@app.exception_handler(Exception)
async def chat_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception in chat endpoint: {str(exc)}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"response": "Sorry, an error occurred while processing your request.", "context": None}
    )

# Main chat endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """
    Handle chat messages and return responses using the DeepSeek API.
    This is the main endpoint for all chat interactions.
    """
    try:
        logger.info(f"Received chat message: {chat_message.message}")
        logger.debug(f"Chat context: {chat_message.context}")
        # Process the message using our chat service
        response = await chat_service.process_message(
            user_message=chat_message.message,
            context=chat_message.context or {}
        )
        logger.info("Successfully generated response")
        logger.debug(f"Response content: {response}")
        return ChatResponse(
            response=response,
            context=chat_message.context or {}
        )
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail={"response": "Sorry, I encountered an error processing your request.", "context": None}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
