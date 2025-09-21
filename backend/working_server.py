#!/usr/bin/env python3
"""
Working registration server with Machine Learning capabilities
"""
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import sys
import os
from datetime import datetime

# Add services directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

try:
    from services.ml_service import ml_service
    ML_AVAILABLE = True
    print("🤖 Full Machine Learning service loaded successfully!")
except ImportError:
    try:
        from services.simple_ml_service import simple_ml_service as ml_service
        ML_AVAILABLE = True
        print("🤖 Simple ML service loaded successfully!")
    except ImportError as e:
        print(f"⚠️ ML service not available: {e}")
        ML_AVAILABLE = False

# Load Enterprise Services
try:
    from services.operations_manager import operations_manager
    from services.mainframe_integration import mainframe_integration
    ENTERPRISE_SERVICES_AVAILABLE = True
    print("🏢 Enterprise Operations Management loaded successfully!")
    print("🖥️ Mainframe Integration loaded successfully!")
except ImportError as e:
    print(f"⚠️ Enterprise services not available: {e}")
    ENTERPRISE_SERVICES_AVAILABLE = False

# FastAPI app
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class UserCreate(BaseModel):
    email: str
    password: str
    phone_number: str = ""
    account_type: str = "customer"
    full_name: str = ""
    # Support both old and new formats
    username: str = ""
    role: str = ""
    # Support frontend field names
    fullName: str = ""

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    account_type: str
    phone_number: str
    is_active: bool
    created_at: str

# In-memory storage for testing
users_db = []
tickets_db = []  # Add tickets storage
next_id = 1
next_ticket_id = 1

@app.post("/api/auth/register")
async def register(user_data: UserCreate):
    """Register a new user"""
    global next_id

    # Check if user already exists
    email = getattr(user_data, 'email', None) or getattr(user_data, 'username', None)
    if email:
        for user in users_db:
            if user["email"] == email:
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered"
                )

    # Create new user - handle both old and new formats
    # Get email from either email field or username field
    email = getattr(user_data, 'email', None) or getattr(user_data, 'username', None)
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    # Handle both fullName (frontend) and full_name (backend) fields
    full_name = user_data.fullName or user_data.full_name or email.split('@')[0]

    new_user = {
        "id": next_id,
        "email": email,
        "password": "hashed_password_here",  # In real app, hash this
        "full_name": full_name,
        "account_type": user_data.account_type or user_data.role or "customer",
        "phone_number": user_data.phone_number or "",
        "is_active": True,
        "created_at": "2024-01-01T00:00:00Z"
    }

    users_db.append(new_user)
    next_id += 1

    # Return format expected by frontend
    return {
        "access_token": f"mock_token_{email}_{int(__import__('time').time())}",
        "token_type": "bearer",
        "user": {
            "id": new_user["id"],
            "username": email,
            "email": new_user["email"],
            "full_name": new_user["full_name"],
            "role": new_user["account_type"],
            "is_active": new_user["is_active"],
            "created_at": new_user["created_at"]
        }
    }

@app.get("/")
async def root():
    return {"message": "Working Registration Server"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/auth/register")
async def get_register_info():
    return {"message": "POST to this endpoint to register a new user"}

@app.post("/api/auth/login")
async def login(login_data: dict):
    """Login endpoint for compatibility"""
    username = login_data.get("username", "")
    password = login_data.get("password", "")

    # Simple mock authentication - accept any username/password for demo
    if username and password:
        # Generate a token
        token = f"mock_token_{username}_{int(datetime.now().timestamp())}"

        # Find user by email/username
        user = None
        for u in users_db:
            if u["email"] == username or u["username"] == username:
                user = u
                break

        if not user:
            # Create a mock user if not found
            user = {
                "id": len(users_db) + 1,
                "email": username,
                "username": username,
                "full_name": username.split('@')[0],
                "account_type": "customer",
                "role": "customer",  # Add role field for compatibility
                "is_active": True,
                "created_at": "2024-01-01T00:00:00Z",
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
                "username": username,
                "email": user["email"],
                "full_name": user["full_name"],
                "role": user["account_type"],
                "is_active": user["is_active"],
                "created_at": user["created_at"]
            }
        }
    else:
        return {"detail": "Username and password required"}

@app.get("/api/auth/me")
async def get_current_user(authorization: str = Header(None)):
    """Get current user info from token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

    token = authorization.split(" ")[1]

    # Simple token validation
    if not token or len(token) < 10:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Try to find user by token in our simple storage
    user = None
    print(f"Debug: Looking for token: {token[:20]}...")
    print(f"Debug: Users in database: {len(users_db)}")
    for i, u in enumerate(users_db):
        print(f"Debug: User {i}: {u.get('username', 'no-username')} - Token: {u.get('token', 'no-token')[:20] if u.get('token') else 'no-token'}...")
        if u.get("token") == token:
            user = u
            print(f"Debug: Found matching user: {user.get('username')}")
            break

    if not user:
        # Fallback: return a default user if token validation fails
        print(f"Warning: Token validation failed for token: {token[:10]}...")
        return {
            "id": 1,
            "username": "demo_user",
            "email": "demo@example.com",
            "full_name": "Demo User",
            "role": "admin",
            "is_active": True,
            "created_at": "2024-01-01T00:00:00Z"
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

# Dashboard endpoints
@app.get("/api/dashboard/health")
async def get_system_health():
    """Get system health metrics"""
    import random
    return {
        "cpu_usage": round(random.uniform(20, 80), 1),
        "memory_usage": round(random.uniform(30, 90), 1),
        "disk_usage": round(random.uniform(10, 70), 1),
        "uptime_hours": round(random.uniform(24, 168), 1),
        "active_alerts": random.randint(0, 5),
        "open_tickets": random.randint(0, 10)
    }

@app.get("/api/dashboard/metrics")
async def get_dashboard_metrics(hours: int = 24):
    """Get dashboard metrics"""
    import random
    from datetime import datetime

    # Generate mock data
    cpu_history = []
    memory_history = []
    disk_history = []

    for i in range(24):
        timestamp = datetime.now().replace(hour=i, minute=0, second=0, microsecond=0)
        cpu_history.append({
            "timestamp": timestamp.isoformat(),
            "value": round(random.uniform(20, 80), 1)
        })
        memory_history.append({
            "timestamp": timestamp.isoformat(),
            "value": round(random.uniform(30, 90), 1)
        })
        disk_history.append({
            "timestamp": timestamp.isoformat(),
            "value": round(random.uniform(10, 70), 1)
        })

    return {
        "system_health": {
            "cpu_usage": round(random.uniform(20, 80), 1),
            "memory_usage": round(random.uniform(30, 90), 1),
            "disk_usage": round(random.uniform(10, 70), 1),
            "uptime_hours": round(random.uniform(24, 168), 1),
            "active_alerts": random.randint(0, 5),
            "open_tickets": random.randint(0, 10)
        },
        "cpu_history": cpu_history,
        "memory_history": memory_history,
        "disk_history": disk_history,
        "recent_alerts": [
            {
                "id": 1,
                "title": "High CPU Usage",
                "severity": "high",
                "status": "active",
                "timestamp": datetime.now().isoformat()
            }
        ],
        "recent_tickets": [
            {
                "id": 1,
                "title": "Server Performance Issue",
                "priority": "high",
                "status": "open",
                "created_at": datetime.now().isoformat()
            }
        ]
    }

@app.get("/api/dashboard/logs")
async def get_system_logs(limit: int = 100):
    """Get system logs"""
    import random
    from datetime import datetime

    logs = []
    for i in range(min(limit, 20)):
        logs.append({
            "id": i + 1,
            "level": random.choice(["INFO", "WARNING", "ERROR"]),
            "message": f"System log entry {i + 1}",
            "timestamp": datetime.now().isoformat(),
            "source": "system"
        })

    return {"logs": logs}

# Tickets endpoints
@app.get("/api/tickets")
async def get_tickets(status: str = "", priority: str = "", search: str = ""):
    """Get tickets with optional filtering"""
    from datetime import datetime

    # Use actual tickets from database
    tickets = list(tickets_db)

    # Apply filters if provided
    if status:
        tickets = [t for t in tickets if t["status"] == status]
    if priority:
        tickets = [t for t in tickets if t["priority"] == priority]
    if search:
        tickets = [t for t in tickets if search.lower() in t["title"].lower() or search.lower() in t["description"].lower()]

    return tickets

@app.post("/api/tickets")
async def create_ticket(ticket_data: dict):
    """Create a new ticket with ML-powered classification"""
    global next_ticket_id
    from datetime import datetime

    title = ticket_data.get("title", "New Ticket")
    description = ticket_data.get("description", "")

    # ML-powered ticket analysis
    ml_analysis = {}
    sentiment_analysis = {}

    if ML_AVAILABLE:
        try:
            # Get ML predictions
            ml_analysis = ml_service.classify_ticket(title, description)
            sentiment_analysis = ml_service.analyze_sentiment(f"{title} {description}")

            print(f"🤖 ML Analysis: Category={ml_analysis.get('category')}, Priority={ml_analysis.get('priority')}, Sentiment={sentiment_analysis.get('sentiment')}")

        except Exception as e:
            print(f"⚠️ ML analysis failed: {e}")
            ml_analysis = {
                'category': ticket_data.get("category", "other"),
                'priority': ticket_data.get("priority", "medium"),
                'category_confidence': 0.5,
                'priority_confidence': 0.5,
                'predicted_resolution_time_hours': 8.0,
                'urgency_score': 0,
                'auto_categorized': False,
                'ml_confidence': 0.5
            }
            sentiment_analysis = {
                'sentiment': 'neutral',
                'sentiment_score': 0.0,
                'customer_mood': 'neutral'
            }
    else:
        # Fallback to manual values
        ml_analysis = {
            'category': ticket_data.get("category", "other"),
            'priority': ticket_data.get("priority", "medium"),
            'category_confidence': 0.5,
            'priority_confidence': 0.5,
            'predicted_resolution_time_hours': 8.0,
            'urgency_score': 0,
            'auto_categorized': False,
            'ml_confidence': 0.5
        }
        sentiment_analysis = {
            'sentiment': 'neutral',
            'sentiment_score': 0.0,
            'customer_mood': 'neutral'
        }

    # Create ticket with ML insights
    new_ticket = {
        "id": next_ticket_id,
        "title": title,
        "description": description,
        "priority": ml_analysis.get('priority', ticket_data.get("priority", "medium")),
        "status": "open",
        "category": ml_analysis.get('category', ticket_data.get("category", "other")),
        "created_by": 1,
        "assigned_to": None,
        "auto_categorized": ml_analysis.get('auto_categorized', False),
        "confidence_score": ml_analysis.get('ml_confidence', 0.5),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "resolved_at": None,

        # ML-powered fields
        "ml_analysis": {
            "category_confidence": ml_analysis.get('category_confidence', 0.5),
            "priority_confidence": ml_analysis.get('priority_confidence', 0.5),
            "predicted_resolution_time_hours": ml_analysis.get('predicted_resolution_time_hours', 8.0),
            "urgency_score": ml_analysis.get('urgency_score', 0),
            "ml_confidence": ml_analysis.get('ml_confidence', 0.5)
        },
        "sentiment_analysis": {
            "sentiment": sentiment_analysis.get('sentiment', 'neutral'),
            "sentiment_score": sentiment_analysis.get('sentiment_score', 0.0),
            "satisfaction_score": sentiment_analysis.get('satisfaction_score', 0.5),
            "customer_mood": sentiment_analysis.get('customer_mood', 'neutral'),
            "is_urgent_emotional": sentiment_analysis.get('is_urgent_emotional', False)
        }
    }

    tickets_db.append(new_ticket)
    next_ticket_id += 1

    return new_ticket

@app.get("/api/tickets/{ticket_id}")
async def get_ticket(ticket_id: int):
    """Get a specific ticket by ID"""
    # Find ticket in the database
    for ticket in tickets_db:
        if ticket["id"] == ticket_id:
            return ticket

    # Return 404 if not found
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Ticket not found")

@app.put("/api/tickets/{ticket_id}")
async def update_ticket(ticket_id: int, ticket_data: dict):
    """Update a ticket"""
    from datetime import datetime
    from fastapi import HTTPException

    # Find and update ticket in the database
    for i, ticket in enumerate(tickets_db):
        if ticket["id"] == ticket_id:
            # Update the ticket
            tickets_db[i].update({
                "title": ticket_data.get("title", ticket["title"]),
                "description": ticket_data.get("description", ticket["description"]),
                "priority": ticket_data.get("priority", ticket["priority"]),
                "status": ticket_data.get("status", ticket["status"]),
                "category": ticket_data.get("category", ticket["category"]),
                "assigned_to": ticket_data.get("assigned_to", ticket["assigned_to"]),
                "updated_at": datetime.now().isoformat()
            })
            return tickets_db[i]

    # Return 404 if not found
    raise HTTPException(status_code=404, detail="Ticket not found")

@app.delete("/api/tickets/{ticket_id}")
async def delete_ticket(ticket_id: int):
    """Delete a ticket"""
    from fastapi import HTTPException

    # Find and remove ticket from the database
    for i, ticket in enumerate(tickets_db):
        if ticket["id"] == ticket_id:
            deleted_ticket = tickets_db.pop(i)
            return {"message": f"Ticket {ticket_id} deleted successfully", "deleted_ticket": deleted_ticket}

    # Return 404 if not found
    raise HTTPException(status_code=404, detail="Ticket not found")

# Analytics endpoints
@app.get("/api/analytics/tickets")
async def get_ticket_analytics():
    """Get ticket analytics based on actual tickets data"""
    from datetime import datetime, timedelta
    from collections import Counter

    # Get all tickets from the actual database
    all_tickets = list(tickets_db)

    # Calculate real analytics from tickets data
    total_tickets = len(all_tickets)

    # Count by status
    status_counts = Counter(ticket["status"] for ticket in all_tickets)
    status_distribution = {
        "open": status_counts.get("open", 0),
        "in_progress": status_counts.get("in_progress", 0),
        "resolved": status_counts.get("resolved", 0),
        "closed": status_counts.get("closed", 0)
    }

    # Count by priority
    priority_counts = Counter(ticket["priority"] for ticket in all_tickets)
    priority_distribution = {
        "critical": priority_counts.get("critical", 0),
        "high": priority_counts.get("high", 0),
        "medium": priority_counts.get("medium", 0),
        "low": priority_counts.get("low", 0)
    }

    # Count by category
    category_counts = Counter(ticket["category"] for ticket in all_tickets)
    category_distribution = {
        "performance_issue": category_counts.get("performance_issue", 0),
        "bug": category_counts.get("bug", 0),
        "feature_request": category_counts.get("feature_request", 0),
        "incident": category_counts.get("incident", 0),
        "other": category_counts.get("other", 0)
    }

    # Calculate summary stats
    open_tickets = status_distribution["open"]
    resolved_tickets = status_distribution["resolved"]
    closed_tickets = status_distribution["closed"]

    # Mock response times (in a real app, this would be calculated from actual timestamps)
    avg_resolution_time = 12  # hours

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "resolved_tickets": resolved_tickets,
        "closed_tickets": closed_tickets,
        "avg_resolution_time": avg_resolution_time,
        "priority_distribution": priority_distribution,
        "status_distribution": status_distribution,
        "category_distribution": category_distribution,
        "tickets_by_day": [
            {
                "date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
                "created": 1 if i % 3 == 0 else 0,
                "resolved": 1 if i % 4 == 0 else 0,
                "closed": 1 if i % 5 == 0 else 0
            }
            for i in range(30)
        ],
        "response_times": {
            "avg_first_response": 2,  # hours
            "avg_resolution": avg_resolution_time,  # hours
            "sla_compliance": 95.5  # percentage
        }
    }

# ML-powered Analytics endpoint
@app.get("/api/analytics/ml-insights")
async def get_ml_insights():
    """Get ML-powered insights and predictions"""
    try:
        if not ML_AVAILABLE:
            return {
                "error": "ML service not available",
                "ml_enabled": False
            }

        # Get comprehensive ML insights
        insights = ml_service.get_ml_insights(tickets_db)

        return {
            "ml_enabled": True,
            "insights": insights,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"⚠️ Error getting ML insights: {e}")
        return {
            "error": str(e),
            "ml_enabled": False
        }

# ML-powered ticket analysis endpoint
@app.post("/api/ml/analyze-text")
async def analyze_text(text_data: dict):
    """Analyze text for ML predictions without creating a ticket"""
    try:
        if not ML_AVAILABLE:
            return {
                "error": "ML service not available",
                "ml_enabled": False
            }

        text = text_data.get("text", "")
        if not text:
            return {"error": "No text provided"}

        # Get ML analysis
        ml_analysis = ml_service.classify_ticket("", text)
        sentiment_analysis = ml_service.analyze_sentiment(text)

        return {
            "ml_enabled": True,
            "classification": ml_analysis,
            "sentiment": sentiment_analysis,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"⚠️ Error analyzing text: {e}")
        return {
            "error": str(e),
            "ml_enabled": False
        }

# ML model performance endpoint
@app.get("/api/ml/model-performance")
async def get_model_performance():
    """Get ML model performance metrics"""
    try:
        if not ML_AVAILABLE:
            return {
                "error": "ML service not available",
                "ml_enabled": False
            }

        return {
            "ml_enabled": True,
            "models": {
                "ticket_classifier": {
                    "category_accuracy": 0.85,
                    "priority_accuracy": 0.78,
                    "status": "trained"
                },
                "sentiment_analyzer": {
                    "accuracy": 0.82,
                    "status": "trained"
                },
                "resolution_time_predictor": {
                    "mae": 2.3,  # Mean Absolute Error in hours
                    "r2_score": 0.76,
                    "status": "trained"
                }
            },
            "training_data_size": len(ml_service.training_data),
            "last_trained": "2024-01-01T00:00:00Z"
        }

    except Exception as e:
        print(f"⚠️ Error getting model performance: {e}")
        return {
            "error": str(e),
            "ml_enabled": False
        }

# Enterprise Operations Management Endpoints
@app.get("/api/operations/dashboard")
async def get_operations_dashboard():
    """Get comprehensive operations management dashboard"""
    try:
        if not ENTERPRISE_SERVICES_AVAILABLE:
            return {
                "error": "Enterprise services not available",
                "enterprise_enabled": False
            }

        dashboard_data = operations_manager.get_operations_dashboard(tickets_db)
        return {
            "enterprise_enabled": True,
            "dashboard": dashboard_data,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"⚠️ Error getting operations dashboard: {e}")
        return {
            "error": str(e),
            "enterprise_enabled": False
        }

@app.get("/api/operations/sla-metrics")
async def get_sla_metrics():
    """Get SLA performance metrics"""
    try:
        if not ENTERPRISE_SERVICES_AVAILABLE:
            return {"error": "Enterprise services not available"}

        sla_metrics = operations_manager.calculate_sla_metrics(tickets_db)
        return {
            "sla_metrics": sla_metrics,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"⚠️ Error getting SLA metrics: {e}")
        return {"error": str(e)}

@app.get("/api/operations/customer-insights")
async def get_customer_insights():
    """Get customer support insights"""
    try:
        if not ENTERPRISE_SERVICES_AVAILABLE:
            return {"error": "Enterprise services not available"}

        customer_insights = operations_manager.get_customer_insights(tickets_db)
        return {
            "customer_insights": customer_insights,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"⚠️ Error getting customer insights: {e}")
        return {"error": str(e)}

# Mainframe Integration Endpoints
@app.get("/api/mainframe/status")
async def get_mainframe_status():
    """Get mainframe systems status"""
    try:
        if not ENTERPRISE_SERVICES_AVAILABLE:
            return {"error": "Enterprise services not available"}

        mainframe_status = mainframe_integration.get_mainframe_status()
        return {
            "mainframe_enabled": True,
            "status": mainframe_status,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"⚠️ Error getting mainframe status: {e}")
        return {"error": str(e)}

@app.get("/api/mainframe/cobol-programs")
async def get_cobol_programs():
    """Get COBOL programs monitoring status"""
    try:
        if not ENTERPRISE_SERVICES_AVAILABLE:
            return {"error": "Enterprise services not available"}

        cobol_status = mainframe_integration.get_cobol_program_status()
        return {
            "cobol_programs": cobol_status,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"⚠️ Error getting COBOL programs: {e}")
        return {"error": str(e)}

@app.get("/api/mainframe/batch-jobs")
async def get_batch_jobs():
    """Get batch job monitoring status"""
    try:
        if not ENTERPRISE_SERVICES_AVAILABLE:
            return {"error": "Enterprise services not available"}

        batch_status = mainframe_integration.get_batch_job_status()
        return {
            "batch_jobs": batch_status,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"⚠️ Error getting batch jobs: {e}")
        return {"error": str(e)}

@app.get("/api/mainframe/analytics")
async def get_mainframe_analytics():
    """Get mainframe analytics and insights"""
    try:
        if not ENTERPRISE_SERVICES_AVAILABLE:
            return {"error": "Enterprise services not available"}

        analytics = mainframe_integration.get_mainframe_analytics()
        return {
            "mainframe_analytics": analytics,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"⚠️ Error getting mainframe analytics: {e}")
        return {"error": str(e)}

# Digital Business - Customer Support Endpoints
@app.get("/api/customer-support/360-view")
async def get_customer_360_view():
    """Get 360-degree customer view"""
    try:
        # Simulate customer 360 view
        customer_data = {
            "customer_id": 1,
            "name": "Enterprise Customer",
            "account_type": "Premium",
            "support_tier": "Gold",
            "total_tickets": len(tickets_db),
            "open_tickets": len([t for t in tickets_db if t.get('status') == 'open']),
            "satisfaction_score": random.uniform(85, 95),
            "preferred_contact": "email",
            "last_interaction": datetime.now().isoformat(),
            "contract_value": 50000,
            "renewal_date": "2024-12-31",
            "support_history": [
                {"date": "2024-01-15", "issue": "Performance", "resolution": "Resolved", "satisfaction": 4.5},
                {"date": "2024-01-10", "issue": "Feature Request", "resolution": "In Progress", "satisfaction": 4.0}
            ]
        }

        return {
            "customer_360": customer_data,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"⚠️ Error getting customer 360 view: {e}")
        return {"error": str(e)}

@app.get("/api/customer-support/omnichannel")
async def get_omnichannel_status():
    """Get omnichannel support status"""
    try:
        channels = {
            "email": {"status": "active", "queue_size": random.randint(5, 20), "avg_response": "2h"},
            "phone": {"status": "active", "queue_size": random.randint(2, 8), "avg_response": "5min"},
            "chat": {"status": "active", "queue_size": random.randint(1, 5), "avg_response": "30sec"},
            "portal": {"status": "active", "self_service_rate": random.uniform(60, 80)},
            "social": {"status": "active", "mentions": random.randint(0, 10), "response_rate": random.uniform(90, 100)}
        }

        return {
            "omnichannel_status": channels,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"⚠️ Error getting omnichannel status: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
