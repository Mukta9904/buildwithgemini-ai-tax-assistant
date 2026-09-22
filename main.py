import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from app.agent import app as adk_app

app = FastAPI(title="AI Tax Assistant API")

# Allow CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_service = InMemorySessionService()
runner = InMemoryRunner(app=adk_app)

# Store simple context IDs for anonymous users
user_contexts = {}

class ChatRequest(BaseModel):
    message: str
    user_id: str

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    if not req.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    user_id = req.user_id
    if not user_id:
        user_id = str(uuid.uuid4())
        
    if user_id not in user_contexts:
        session = await session_service.create_session(app_name="app", user_id=user_id)
        user_contexts[user_id] = session.id
        
    session_id = user_contexts[user_id]
    
    try:
        # Check if the API key is configured
        if not os.getenv("GEMINI_API_KEY") and not os.getenv("GOOGLE_GENAI_USE_VERTEXAI"):
            return ChatResponse(
                response="Error: GEMINI_API_KEY environment variable is not set. Please set it in your terminal before running the backend.",
                session_id=session_id
            )
            
        print(f"Running agent for session: {session_id}, user: {user_id}")
        response = await runner.run_async(
            user_input=req.message,
            user_id=user_id,
            session_id=session_id
        )
        
        return ChatResponse(
            response=response.content.text if response.content else "No response generated.",
            session_id=session_id
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}
