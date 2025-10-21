# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints import router as chat_router
from app.json_memory import close_mongodb_connection
import uvicorn
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup
    from app.json_memory import json_memory
    try:
        await json_memory.connect()
        print("✅ JSON memory storage initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize JSON memory storage: {e}")
    
    yield
    
    # Shutdown
    try:
        await close_mongodb_connection()
        print("✅ JSON memory storage closed")
    except Exception as e:
        print(f"⚠️ Error closing JSON memory storage: {e}")

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,  # Enable credentials for OAuth
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Add a simple health check endpoint
@app.get("/")
async def root():
    return {"message": "CF Chatbot API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Server is running"}

app.include_router(chat_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)

