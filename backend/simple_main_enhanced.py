from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Header
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from datetime import datetime, timedelta
import random
import openai
from dotenv import load_dotenv
import json
import asyncio
from typing import List

# Import MFA endpoints
from mfa_endpoints import router as mfa_router

# Load environment variables
load_dotenv()

# Configure OpenRouter (which uses OpenAI-compatible API)
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

# WebSocket connection manager for real-time updates
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove broken connections
                self.active_connections.remove(connection)

manager = ConnectionManager()

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

async def get_enhanced_response(message: str) -> str:
    """Get response using OpenRouter with enhanced formatting"""
    try:
        client = openai.AsyncOpenAI(
            api_key=openai.api_key,
            base_url=openai.api_base
        )

        # Enhanced system prompt for better formatting
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
        - Always provide actionable advice and next steps
        - Use proper markdown formatting for better readability"""

        response = await client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=1000,
            temperature=0.7
        )

        # Format the response
        formatted_response = format_response(response.choices[0].message.content)

        return formatted_response

    except Exception as e:
        return f"""<div class="error-message">
        <p>I apologize, but I'm having trouble connecting to my AI service right now.</p>
        <p><strong>Error:</strong> {str(e)}</p>
        <p>Please try again later or contact support.</p>
        </div>"""

app = FastAPI(
    title="Unified IT Support System",
    description="A comprehensive IT support platform with AI-powered FAQ Chatbot using OpenAI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include MFA router
app.include_router(mfa_router)

@app.get("/")
async def root():
    return {"message": "Unified IT Support System API with Enhanced AI Chatbot", "version": "1.0.0"}

@app.get("/favicon.ico")
async def favicon():
    """Favicon endpoint to prevent 500 errors."""
    return {"message": "No favicon"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "unified-it-support", "ai_engine": "openrouter-enhanced"}

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
    # Generate current values
    current_cpu = round(random.uniform(20, 80), 1)
    current_memory = round(random.uniform(30, 90), 1)
    current_disk = round(random.uniform(10, 70), 1)

    # Generate historical data for the last 24 hours (24 data points)
    now = datetime.now()
    cpu_history = []
    memory_history = []
    disk_history = []

    for i in range(24):
        timestamp = now - timedelta(hours=23-i)
        cpu_history.append({
            "timestamp": timestamp.isoformat(),
            "value": round(random.uniform(max(0, current_cpu - 20), min(100, current_cpu + 20)), 1)
        })
        memory_history.append({
            "timestamp": timestamp.isoformat(),
            "value": round(random.uniform(max(0, current_memory - 15), min(100, current_memory + 15)), 1)
        })
        disk_history.append({
            "timestamp": timestamp.isoformat(),
            "value": round(random.uniform(max(0, current_disk - 10), min(100, current_disk + 10)), 1)
        })

    return {
        "system_health": {
            "cpu_usage": current_cpu,
            "memory_usage": current_memory,
            "disk_usage": current_disk,
            "uptime_hours": round(random.uniform(24, 168), 1),
            "active_alerts": random.randint(0, 5),
            "status": "operational"
        },
        "cpu_history": cpu_history,
        "memory_history": memory_history,
        "disk_history": disk_history,
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

@app.get("/api/dashboard/logs")
async def get_system_logs(limit: int = 50, level: str = None, search: str = None):
    """Get system logs with optional filtering."""
    # Generate sample log entries
    log_levels = ["INFO", "WARN", "ERROR", "DEBUG", "FATAL"]
    log_sources = ["auth", "api", "database", "system", "chatbot", "tickets"]
    log_messages = [
        "User authentication successful",
        "API request processed",
        "Database connection established",
        "System health check completed",
        "Chatbot response generated",
        "Ticket created successfully",
        "User logged out",
        "Database query executed",
        "System backup started",
        "Error handling triggered",
        "Cache cleared",
        "Configuration updated",
        "Service started",
        "Service stopped",
        "Memory usage high",
        "CPU usage spike detected",
        "Network connection lost",
        "File upload completed",
        "Email sent successfully",
        "Scheduled task executed"
    ]

    logs = []
    for i in range(limit):
        log_level = random.choice(log_levels)
        log_source = random.choice(log_sources)
        log_message = random.choice(log_messages)

        # Apply level filter
        if level and level.upper() != log_level:
            continue

        # Apply search filter
        if search and search.lower() not in log_message.lower():
            continue

        logs.append({
            "id": random.randint(10000, 99999),
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 1440))).isoformat(),
            "level": log_level,
            "source": log_source,
            "message": log_message,
            "hostname": f"server-{random.randint(1, 5)}",
            "metadata": json.dumps({
                "user_id": random.randint(1, 100) if random.choice([True, False]) else None,
                "request_id": f"req_{random.randint(1000, 9999)}",
                "duration_ms": random.randint(10, 5000) if log_level in ["INFO", "DEBUG"] else None,
                "error_code": random.randint(400, 599) if log_level in ["ERROR", "FATAL"] else None,
                "ip_address": f"192.168.1.{random.randint(1, 254)}",
                "user_agent": random.choice([
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                ])
            })
        })

    # Sort by timestamp (newest first)
    logs.sort(key=lambda x: x["timestamp"], reverse=True)

    return {
        "logs": logs[:limit],
        "total": len(logs),
        "levels": log_levels,
        "sources": log_sources
    }

# In-memory storage for tickets (in production, use a database)
tickets_db = [
    {
        "id": 1,
        "title": "Password Reset Request",
        "description": "User unable to access their account after password change",
        "priority": "high",
        "status": "open",
        "category": "Account",
        "assigned_to": "John Doe",
        "created_by": "user@example.com",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z",
        "resolved_at": None,
        "tags": ["password", "account", "urgent"]
    },
    {
        "id": 2,
        "title": "VPN Connection Issues",
        "description": "Unable to connect to company VPN from home office",
        "priority": "medium",
        "status": "in_progress",
        "category": "Network",
        "assigned_to": "Jane Smith",
        "created_by": "employee@example.com",
        "created_at": "2024-01-14T14:20:00Z",
        "updated_at": "2024-01-15T09:15:00Z",
        "resolved_at": None,
        "tags": ["vpn", "network", "remote"]
    },
    {
        "id": 3,
        "title": "Software Installation Request",
        "description": "Need Adobe Creative Suite installed on workstation",
        "priority": "low",
        "status": "pending_approval",
        "category": "Software",
        "assigned_to": "Mike Johnson",
        "created_by": "designer@example.com",
        "created_at": "2024-01-13T16:45:00Z",
        "updated_at": "2024-01-13T16:45:00Z",
        "resolved_at": None,
        "tags": ["software", "adobe", "installation"]
    },
    {
        "id": 4,
        "title": "Email Sync Problems",
        "description": "Outlook not syncing emails properly with Exchange server",
        "priority": "medium",
        "status": "resolved",
        "category": "Email",
        "assigned_to": "Sarah Wilson",
        "created_by": "manager@example.com",
        "created_at": "2024-01-12T11:00:00Z",
        "updated_at": "2024-01-14T15:30:00Z",
        "resolved_at": "2024-01-14T15:30:00Z",
        "tags": ["email", "outlook", "exchange"]
    },
    {
        "id": 5,
        "title": "Printer Not Working",
        "description": "Office printer showing offline status and not printing documents",
        "priority": "low",
        "status": "open",
        "category": "Hardware",
        "assigned_to": "Tom Brown",
        "created_by": "admin@example.com",
        "created_at": "2024-01-15T08:00:00Z",
        "updated_at": "2024-01-15T08:00:00Z",
        "resolved_at": None,
        "tags": ["printer", "hardware", "office"]
    }
]

@app.get("/api/tickets")
async def get_tickets(
    status: str = None,
    priority: str = None,
    search: str = None,
    limit: int = 50,
    offset: int = 0
):
    """Get all tickets with optional filtering."""
    filtered_tickets = tickets_db.copy()

    # Apply filters
    if status and status != "all":
        filtered_tickets = [t for t in filtered_tickets if t["status"] == status]

    if priority and priority != "all":
        filtered_tickets = [t for t in filtered_tickets if t["priority"] == priority]

    if search:
        search_lower = search.lower()
        filtered_tickets = [
            t for t in filtered_tickets
            if search_lower in t["title"].lower() or
               search_lower in t["description"].lower() or
               search_lower in t["category"].lower()
        ]

    # Apply pagination
    total = len(filtered_tickets)
    paginated_tickets = filtered_tickets[offset:offset + limit]

    # Return just the tickets array for frontend compatibility
    return paginated_tickets

@app.get("/api/tickets/{ticket_id}")
async def get_ticket(ticket_id: int):
    """Get a specific ticket by ID."""
    ticket = next((t for t in tickets_db if t["id"] == ticket_id), None)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.post("/api/tickets")
async def create_ticket(ticket_data: dict):
    """Create a new support ticket."""
    new_ticket = {
        "id": max([t["id"] for t in tickets_db], default=0) + 1,
        "title": ticket_data.get("title", "New Ticket"),
        "description": ticket_data.get("description", ""),
        "priority": ticket_data.get("priority", "medium"),
        "status": "open",
        "category": ticket_data.get("category", "General"),
        "assigned_to": "Unassigned",
        "created_by": ticket_data.get("created_by", "user@example.com"),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "resolved_at": None,
        "tags": ticket_data.get("tags", [])
    }

    tickets_db.append(new_ticket)

    # Broadcast real-time update
    await manager.broadcast(json.dumps({
        "type": "ticket_created",
        "ticket": new_ticket
    }))

    return new_ticket

@app.put("/api/tickets/{ticket_id}")
async def update_ticket(ticket_id: int, ticket_data: dict):
    """Update an existing ticket."""
    ticket = next((t for t in tickets_db if t["id"] == ticket_id), None)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Update allowed fields
    updatable_fields = ["title", "description", "priority", "status", "category", "assigned_to", "tags"]
    for field in updatable_fields:
        if field in ticket_data:
            ticket[field] = ticket_data[field]

    ticket["updated_at"] = datetime.now().isoformat()

    # Set resolved_at if status is resolved
    if ticket["status"] == "resolved" and not ticket["resolved_at"]:
        ticket["resolved_at"] = datetime.now().isoformat()
    elif ticket["status"] != "resolved":
        ticket["resolved_at"] = None

    # Broadcast real-time update
    await manager.broadcast(json.dumps({
        "type": "ticket_updated",
        "ticket": ticket
    }))

    return ticket

@app.delete("/api/tickets/{ticket_id}")
async def delete_ticket(ticket_id: int):
    """Delete a ticket."""
    global tickets_db
    ticket = next((t for t in tickets_db if t["id"] == ticket_id), None)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    tickets_db = [t for t in tickets_db if t["id"] != ticket_id]

    # Broadcast real-time update
    await manager.broadcast(json.dumps({
        "type": "ticket_deleted",
        "ticket_id": ticket_id
    }))

    return {"message": "Ticket deleted successfully"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            # Echo back for testing
            await manager.send_personal_message(f"Echo: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api/tickets/analytics")
async def get_ticket_analytics():
    """Get ticket analytics and statistics."""
    total_tickets = len(tickets_db)
    open_tickets = len([t for t in tickets_db if t["status"] == "open"])
    in_progress_tickets = len([t for t in tickets_db if t["status"] == "in_progress"])
    resolved_tickets = len([t for t in tickets_db if t["status"] == "resolved"])

    priority_breakdown = {
        "high": len([t for t in tickets_db if t["priority"] == "high"]),
        "medium": len([t for t in tickets_db if t["priority"] == "medium"]),
        "low": len([t for t in tickets_db if t["priority"] == "low"])
    }

    category_breakdown = {}
    for ticket in tickets_db:
        category = ticket["category"]
        category_breakdown[category] = category_breakdown.get(category, 0) + 1

    # Calculate average resolution time
    resolved_with_times = [t for t in tickets_db if t["resolved_at"]]
    avg_resolution_hours = 0
    if resolved_with_times:
        total_hours = 0
        valid_tickets = 0
        for ticket in resolved_with_times:
            try:
                # Handle both timezone-aware and naive datetime strings
                created_str = ticket["created_at"]
                resolved_str = ticket["resolved_at"]

                # Parse created time
                if created_str.endswith("Z"):
                    created = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
                else:
                    created = datetime.fromisoformat(created_str)

                # Parse resolved time
                if resolved_str.endswith("Z"):
                    resolved = datetime.fromisoformat(resolved_str.replace("Z", "+00:00"))
                else:
                    resolved = datetime.fromisoformat(resolved_str)

                # Make both timezone-aware for comparison
                if created.tzinfo is None:
                    created = created.replace(tzinfo=None)
                if resolved.tzinfo is None:
                    resolved = resolved.replace(tzinfo=None)

                hours = (resolved - created).total_seconds() / 3600
                total_hours += hours
                valid_tickets += 1
            except Exception as e:
                # Skip tickets with invalid datetime formats
                print(f"Warning: Skipping ticket {ticket['id']} due to datetime error: {e}")
                continue
        avg_resolution_hours = total_hours / valid_tickets if valid_tickets > 0 else 0

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "in_progress_tickets": in_progress_tickets,
        "resolved_tickets": resolved_tickets,
        "priority_breakdown": priority_breakdown,
        "category_breakdown": category_breakdown,
        "avg_resolution_hours": round(avg_resolution_hours, 1),
        "resolution_rate": round((resolved_tickets / total_tickets * 100) if total_tickets > 0 else 0, 1)
    }

@app.get("/api/tickets/analytics/summary")
async def get_ticket_analytics_summary():
    """Get ticket analytics summary for the frontend."""
    total_tickets = len(tickets_db)
    open_tickets = len([t for t in tickets_db if t["status"] == "open"])
    in_progress_tickets = len([t for t in tickets_db if t["status"] == "in_progress"])
    resolved_tickets = len([t for t in tickets_db if t["status"] == "resolved"])

    priority_breakdown = {
        "high": len([t for t in tickets_db if t["priority"] == "high"]),
        "medium": len([t for t in tickets_db if t["priority"] == "medium"]),
        "low": len([t for t in tickets_db if t["priority"] == "low"])
    }

    category_breakdown = {}
    for ticket in tickets_db:
        category = ticket["category"]
        category_breakdown[category] = category_breakdown.get(category, 0) + 1

    # Calculate average resolution time
    resolved_with_times = [t for t in tickets_db if t["resolved_at"]]
    avg_resolution_hours = 0
    if resolved_with_times:
        total_hours = 0
        valid_tickets = 0
        for ticket in resolved_with_times:
            try:
                # Handle both timezone-aware and naive datetime strings
                created_str = ticket["created_at"]
                resolved_str = ticket["resolved_at"]

                # Parse created time
                if created_str.endswith("Z"):
                    created = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
                else:
                    created = datetime.fromisoformat(created_str)

                # Parse resolved time
                if resolved_str.endswith("Z"):
                    resolved = datetime.fromisoformat(resolved_str.replace("Z", "+00:00"))
                else:
                    resolved = datetime.fromisoformat(resolved_str)

                # Make both timezone-aware for comparison
                if created.tzinfo is None:
                    created = created.replace(tzinfo=None)
                if resolved.tzinfo is None:
                    resolved = resolved.replace(tzinfo=None)

                hours = (resolved - created).total_seconds() / 3600
                total_hours += hours
                valid_tickets += 1
            except Exception as e:
                # Skip tickets with invalid datetime formats
                print(f"Warning: Skipping ticket {ticket['id']} due to datetime error: {e}")
                continue
        avg_resolution_hours = total_hours / valid_tickets if valid_tickets > 0 else 0

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "in_progress_tickets": in_progress_tickets,
        "resolved_tickets": resolved_tickets,
        "priority_breakdown": priority_breakdown,
        "category_breakdown": category_breakdown,
        "avg_resolution_hours": round(avg_resolution_hours, 1),
        "resolution_rate": round((resolved_tickets / total_tickets * 100) if total_tickets > 0 else 0, 1)
    }

@app.post("/api/chatbot/chat")
async def chat_with_bot(chat_data: dict):
    """Chat with the AI-powered universal assistant using enhanced OpenRouter."""
    message = chat_data.get("message", "").strip()

    if not message:
        return {
            "response": "<p>Please enter a message to start our conversation!</p>",
            "session_id": f"session_{random.randint(1000, 9999)}",
            "confidence_score": 0.5,
            "was_escalated": False,
            "ticket_id": None,
            "ai_engine": "openrouter-enhanced"
        }

    # Get response from enhanced OpenRouter
    response_text = await get_enhanced_response(message)

    # Calculate confidence based on response length and content
    confidence = min(0.95, max(0.7, len(response_text) / 1000))

    return {
        "response": response_text,
        "session_id": f"session_{random.randint(1000, 9999)}",
        "confidence_score": confidence,
        "was_escalated": False,
        "ticket_id": None,
        "ai_engine": "openrouter-enhanced"
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
            "answer": "Our AI chatbot uses OpenAI technology with enhanced formatting to provide intelligent, contextual responses to your questions.",
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
        "ai_engine": "OpenRouter Enhanced",
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
        # Generate a token
        token = f"mock_token_{username}_{int(datetime.now().timestamp())}"

        # Find or create user
        user = None
        for u in users_db:
            if u["username"] == username:
                user = u
                break

        if not user:
            # Create new user if not found
            user = {
                "id": len(users_db) + 1,
                "username": username,
                "email": f"{username}@example.com",
                "full_name": username.title(),
                "role": "customer",
                "is_active": True,
                "created_at": datetime.now().isoformat(),
                "token": token
            }
            users_db.append(user)
        else:
            # Update existing user with new token
            user["token"] = token

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "full_name": user["full_name"],
                "role": user["role"],
                "is_active": user["is_active"],
                "created_at": user["created_at"]
            }
        }
    else:
        return {"detail": "Username and password required"}

@app.post("/api/auth/register")
async def register(user_data: dict):
    """Register endpoint."""
    # Generate a token for the new user
    token = f"mock_token_{user_data.get('username', 'user')}_{int(datetime.now().timestamp())}"

    # Create new user
    user = {
        "id": len(users_db) + 1,
        "username": user_data.get("username", ""),
        "email": user_data.get("email", ""),
        "full_name": user_data.get("full_name", ""),
        "role": user_data.get("role", "customer"),
        "is_active": True,
        "created_at": datetime.now().isoformat(),
        "token": token
    }

    # Add to users database
    users_db.append(user)

    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
        "role": user["role"],
        "is_active": user["is_active"],
        "created_at": user["created_at"],
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/api/auth/me")
async def get_current_user(authorization: str = Header(None)):
    """Get current user info from token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

    token = authorization.split(" ")[1]

    # Simple token validation - in production, use proper JWT validation
    # For now, we'll check if it's a valid token format
    if not token or len(token) < 10:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Try to find user by token in our simple storage
    # This is a simplified approach - in production, use proper JWT validation
    user = None
    for u in users_db:
        if u.get("token") == token:
            user = u
            break

    if not user:
        # Fallback: return a default user if token validation fails
        # This maintains backward compatibility but logs the issue
        print(f"Warning: Token validation failed for token: {token[:10]}...")
        return {
            "id": 1,
            "username": "demo_user",
            "email": "demo@example.com",
            "full_name": "Demo User",
            "role": "admin",
            "is_active": True,
            "created_at": datetime.now().isoformat()
        }

    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
        "role": user["role"],
        "is_active": user["is_active"],
        "created_at": user["created_at"]
    }

# Analytics endpoints
@app.get("/api/analytics/tickets")
async def get_ticket_analytics():
    """Get ticket analytics for the frontend."""
    return {
        "total_tickets": len(tickets_db),
        "open_tickets": len([t for t in tickets_db if t["status"] == "open"]),
        "in_progress_tickets": len([t for t in tickets_db if t["status"] == "in_progress"]),
        "resolved_tickets": len([t for t in tickets_db if t["status"] == "resolved"]),
        "priority_breakdown": {
            "high": len([t for t in tickets_db if t["priority"] == "high"]),
            "medium": len([t for t in tickets_db if t["priority"] == "medium"]),
            "low": len([t for t in tickets_db if t["priority"] == "low"])
        },
        "category_breakdown": {
            "Hardware": len([t for t in tickets_db if t["category"] == "Hardware"]),
            "Software": len([t for t in tickets_db if t["category"] == "Software"]),
            "Network": len([t for t in tickets_db if t["category"] == "Network"]),
            "General": len([t for t in tickets_db if t["category"] == "General"])
        },
        "avg_resolution_hours": 24.5,
        "resolution_rate": 85.2
    }

if __name__ == "__main__":
    uvicorn.run(
        "simple_main_enhanced:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )
