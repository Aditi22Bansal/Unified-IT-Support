from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from datetime import datetime
import random
import openai
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
import json

# Load environment variables
load_dotenv()

# Configure OpenRouter (which uses OpenAI-compatible API)
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

# Initialize LangChain with OpenRouter
llm = ChatOpenAI(
    model_name="openai/gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.7,
    max_tokens=1000
)

# Create a formatted response template
def format_response(text: str) -> str:
    """Format the AI response with proper HTML-like formatting for better display"""
    # Convert markdown-style formatting to HTML-like formatting
    formatted = text.replace('**', '<strong>').replace('**', '</strong>')
    formatted = formatted.replace('*', '<em>').replace('*', '</em>')

    # Convert bullet points to proper HTML lists
    lines = formatted.split('\n')
    formatted_lines = []
    in_list = False

    for line in lines:
        line = line.strip()
        if line.startswith('• '):
            if not in_list:
                formatted_lines.append('<ul>')
                in_list = True
            formatted_lines.append(f'<li>{line[2:]}</li>')
        elif line.startswith('- '):
            if not in_list:
                formatted_lines.append('<ul>')
                in_list = True
            formatted_lines.append(f'<li>{line[2:]}</li>')
        elif line.startswith(('1. ', '2. ', '3. ', '4. ', '5. ', '6. ', '7. ', '8. ', '9. ')):
            if not in_list:
                formatted_lines.append('<ol>')
                in_list = True
            # Extract number and text
            parts = line.split('. ', 1)
            if len(parts) == 2:
                formatted_lines.append(f'<li>{parts[1]}</li>')
        else:
            if in_list:
                formatted_lines.append('</ul>' if '•' in formatted_lines[-2] or '-' in formatted_lines[-2] else '</ol>')
                in_list = False
            if line:
                formatted_lines.append(f'<p>{line}</p>')

    if in_list:
        formatted_lines.append('</ul>')

    return '\n'.join(formatted_lines)

async def get_langchain_response(message: str) -> str:
    """Get response using LangChain with OpenRouter"""
    try:
        # Create a system prompt for IT support
        system_prompt = """You are an AI assistant for an IT Support System. You are helpful, knowledgeable, and professional.
        You can answer questions about technology, IT support, programming, science, business, health, travel, and virtually any topic.

        IMPORTANT FORMATTING RULES:
        - Use **bold** for headings and important terms
        - Use bullet points (•) for lists
        - Use numbered lists (1., 2., 3.) for step-by-step instructions
        - Use emojis to make responses engaging
        - Structure responses with clear sections
        - Be conversational but informative
        - If it's an IT-related question, provide specific technical guidance
        - For other topics, be comprehensive and helpful
        - Always provide actionable advice and next steps"""

        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template("{input}")
        ])

        # Create the chain
        chain = LLMChain(llm=llm, prompt=prompt)

        # Get response
        response = await chain.arun(input=message)

        # Format the response
        formatted_response = format_response(response)

        return formatted_response

    except Exception as e:
        return f"""<div class="error-message">
        <p>I apologize, but I'm having trouble connecting to my AI service right now.</p>
        <p><strong>Error:</strong> {str(e)}</p>
        <p>Please try again later or contact support.</p>
        </div>"""

app = FastAPI(
    title="Unified IT Support System",
    description="A comprehensive IT support platform with AI-powered FAQ Chatbot using LangChain + OpenAI",
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
    return {"message": "Unified IT Support System API with LangChain + OpenAI", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "unified-it-support", "ai_engine": "langchain-openrouter"}

@app.get("/api/dashboard/health")
async def get_system_health():
    """Get current system health metrics."""
    return {
        "cpu_usage": round(random.uniform(20, 80), 1),
        "memory_usage": round(random.uniform(30, 90), 1),
        "disk_usage": round(random.uniform(10, 70), 1),
        "uptime_hours": round(random.uniform(24, 168), 1),
        "active_alerts": random.randint(0, 5),
        "status": "operational",
        "ai_status": "active"
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
        "ai_chatbot": {
            "total_queries": random.randint(100, 1000),
            "successful_responses": random.randint(95, 100),
            "avg_response_time": f"{random.uniform(0.5, 2.0):.1f}s",
            "active_sessions": random.randint(5, 50),
            "satisfaction_score": round(random.uniform(4.0, 5.0), 1)
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
    """Chat with the AI-powered universal assistant using LangChain + OpenRouter."""
    message = chat_data.get("message", "").strip()

    if not message:
        return {
            "response": "<p>Please enter a message to start our conversation!</p>",
            "session_id": f"session_{random.randint(1000, 9999)}",
            "confidence_score": 0.5,
            "was_escalated": False,
            "ticket_id": None,
            "ai_engine": "langchain-openrouter"
        }

    # Get response from LangChain + OpenRouter
    response_text = await get_langchain_response(message)

    # Calculate confidence based on response length and content
    confidence = min(0.95, max(0.7, len(response_text) / 1000))

    return {
        "response": response_text,
        "session_id": f"session_{random.randint(1000, 9999)}",
        "confidence_score": confidence,
        "was_escalated": False,
        "ticket_id": None,
        "ai_engine": "langchain-openrouter"
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
        },
        {
            "id": 4,
            "question": "How does the AI chatbot work?",
            "answer": "Our AI chatbot uses LangChain + OpenAI technology to provide intelligent, contextual responses to your questions.",
            "category": "AI Support"
        }
    ]

@app.get("/api/chatbot/analytics")
async def get_chatbot_analytics():
    """Get chatbot analytics and performance metrics."""
    return {
        "total_queries": random.randint(1000, 10000),
        "successful_responses": random.randint(950, 1000),
        "avg_response_time": f"{random.uniform(0.5, 2.0):.1f}s",
        "active_sessions": random.randint(10, 100),
        "satisfaction_score": round(random.uniform(4.0, 5.0), 1),
        "top_queries": [
            "Password reset help",
            "VPN connection issues",
            "Software installation",
            "Performance optimization",
            "General IT questions"
        ],
        "ai_engine": "LangChain + OpenRouter",
        "model": "GPT-3.5-turbo",
        "uptime": "99.9%"
    }

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
        "simple_main_langchain:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )




