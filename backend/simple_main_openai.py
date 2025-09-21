from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from datetime import datetime
import random
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

async def get_openai_response(message: str) -> str:
    """Get response from OpenAI API"""
    try:
        client = openai.AsyncOpenAI(api_key=openai.api_key)
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """You are an AI assistant for an IT Support System. You are helpful, knowledgeable, and professional.
                    You can answer questions about technology, IT support, programming, science, business, health, travel, and virtually any topic.
                    Always provide detailed, well-formatted responses with emojis and clear structure. Be conversational but informative.
                    If it's an IT-related question, provide specific technical guidance. For other topics, be comprehensive and helpful."""
                },
                {"role": "user", "content": message}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I'm having trouble connecting to my AI service right now. Error: {str(e)}. Please try again later or contact support."

app = FastAPI(
    title="Unified IT Support System",
    description="A comprehensive IT support platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Unified IT Support System API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "unified-it-support"}

@app.get("/api/dashboard/health")
async def get_system_health():
    """Get current system health metrics."""
    return {
        "cpu_usage": round(random.uniform(20, 80), 1),
        "memory_usage": round(random.uniform(30, 90), 1),
        "disk_usage": round(random.uniform(10, 70), 1),
        "uptime_hours": round(random.uniform(24, 168), 1),
        "active_alerts": random.randint(0, 5),
        "status": "operational"
    }

@app.get("/api/dashboard/metrics")
async def get_dashboard_metrics():
    """Get comprehensive dashboard metrics."""
    return {
        "system_health": {
            "cpu_usage": round(random.uniform(20, 80), 1),
            "memory_usage": round(random.uniform(30, 90), 1),
            "disk_usage": round(random.uniform(10, 70), 1),
            "uptime_hours": round(random.uniform(24, 168), 1),
            "active_alerts": random.randint(0, 5),
            "status": "operational"
        },
        "tickets": {
            "total": random.randint(50, 200),
            "open": random.randint(10, 50),
            "resolved_today": random.randint(5, 25),
            "avg_resolution_time": f"{random.randint(2, 48)} hours"
        },
        "alerts": [
            {
                "id": random.randint(1000, 9999),
                "type": random.choice(["warning", "error", "info"]),
                "message": random.choice([
                    "High CPU usage detected",
                    "Memory usage above threshold",
                    "Disk space running low",
                    "Network connectivity issue",
                    "Service restart required"
                ]),
                "timestamp": datetime.now().isoformat(),
                "severity": random.choice(["low", "medium", "high", "critical"])
            }
            for _ in range(random.randint(0, 5))
        ]
    }

@app.post("/api/tickets/create")
async def create_ticket(ticket_data: dict):
    """Create a new support ticket."""
    return {
        "id": random.randint(100, 999),
        "title": ticket_data.get("title", "New Ticket"),
        "description": ticket_data.get("description", ""),
        "priority": ticket_data.get("priority", "medium"),
        "status": "open",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "resolved_at": None
    }

@app.post("/api/chatbot/chat")
async def chat_with_bot(chat_data: dict):
    """Chat with the AI-powered universal assistant using OpenAI."""
    message = chat_data.get("message", "").strip()

    if not message:
        return {
            "response": "Please enter a message to start our conversation!",
            "session_id": f"session_{random.randint(1000, 9999)}",
            "confidence_score": 0.5,
            "was_escalated": False,
            "ticket_id": None
        }

    # Get response from OpenAI
    response_text = await get_openai_response(message)

    # Calculate confidence based on response length and content
    confidence = min(0.95, max(0.7, len(response_text) / 1000))

    return {
        "response": response_text,
        "session_id": f"session_{random.randint(1000, 9999)}",
        "confidence_score": confidence,
        "was_escalated": False,
        "ticket_id": None
    }

@app.get("/api/chatbot/faqs")
async def get_faqs():
    """Get FAQ entries."""
    return [
        {
            "id": 1,
            "question": "How do I reset my password?",
            "answer": "Click 'Forgot Password' on the login page and follow the email instructions.",
            "category": "Account"
        },
        {
            "id": 2,
            "question": "How do I connect to VPN?",
            "answer": "Download the VPN client from the IT portal and use your company credentials.",
            "category": "Network"
        },
        {
            "id": 3,
            "question": "What are the support hours?",
            "answer": "IT support is available Monday-Friday, 8 AM - 6 PM. Emergency support is 24/7.",
            "category": "General"
        }
    ]

# Authentication endpoints
@app.post("/api/auth/login")
async def login(login_data: dict):
    """Login endpoint."""
    username = login_data.get("username", "")
    password = login_data.get("password", "")

    # Simple mock authentication - accept any username/password for demo
    if username and password:
        return {
            "access_token": f"mock_token_{username}_{int(datetime.now().timestamp())}",
            "token_type": "bearer"
        }
    else:
        return {"detail": "Username and password required"}

@app.post("/api/auth/register")
async def register(user_data: dict):
    """Register endpoint."""
    return {
        "id": 1,
        "username": user_data.get("username", ""),
        "email": user_data.get("email", ""),
        "full_name": user_data.get("full_name", ""),
        "role": user_data.get("role", "customer"),
        "is_active": True,
        "created_at": datetime.now().isoformat()
    }

@app.get("/api/auth/me")
async def get_current_user():
    """Get current user info."""
    return {
        "id": 1,
        "username": "demo_user",
        "email": "demo@example.com",
        "full_name": "Demo User",
        "role": "admin",
        "is_active": True,
        "created_at": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(
        "simple_main_openai:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )
