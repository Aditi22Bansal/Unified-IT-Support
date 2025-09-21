from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

from database.connection import init_db
from api.routes import auth, dashboard, tickets, chatbot
from services.simple_monitoring import start_monitoring
from services.simple_alerting import AlertManager

# Load environment variables
load_dotenv()

# Initialize alert manager
alert_manager = AlertManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    start_monitoring(alert_manager)
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Unified IT Support System",
    description="A comprehensive IT support platform with operations monitoring, incident management, and AI-powered customer support",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(tickets.router, prefix="/api/tickets", tags=["tickets"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["chatbot"])

@app.get("/")
async def root():
    return {"message": "Unified IT Support System API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "unified-it-support"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if os.getenv("DEBUG", "False").lower() == "true" else False
    )

