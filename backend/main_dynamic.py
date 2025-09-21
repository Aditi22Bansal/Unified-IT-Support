"""
Dynamic IT Support System with Real-time Monitoring, Auto-triage, and Role-based Access
"""
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import uvicorn
import logging

# Import services
from database.prisma_client import db_manager, get_database
from services.auth_service import auth_service
from services.rbac import rbac_service, Permission
from services.realtime_monitor import realtime_monitor
from services.auto_triage import auto_triage_service
from services.chatbot_service import ChatbotService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    fullName: str
    password: str
    role: str = "CUSTOMER"

class UserLogin(BaseModel):
    username: str
    password: str

class TicketCreate(BaseModel):
    title: str
    description: str
    priority: str = "MEDIUM"
    category: str = "General"
    tags: Optional[List[str]] = []

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    assignedTo: Optional[str] = None
    tags: Optional[List[str]] = None

class ChatMessage(BaseModel):
    message: str
    sessionId: Optional[str] = None

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str = None):
        await websocket.accept()
        self.active_connections.append(websocket)
        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = []
            self.user_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str = None):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if user_id and user_id in self.user_connections:
            if websocket in self.user_connections[user_id]:
                self.user_connections[user_id].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_to_user(self, message: str, user_id: str):
        if user_id in self.user_connections:
            for connection in self.user_connections[user_id]:
                try:
                    await connection.send_text(message)
                except:
                    self.disconnect(connection, user_id)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                self.active_connections.remove(connection)

manager = ConnectionManager()

# Initialize FastAPI app
app = FastAPI(
    title="Dynamic IT Support System",
    description="Real-time IT support with auto-triage, role-based access, and AI chatbot",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Dependency to get current user
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = await auth_service.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Dependency to check permissions
def require_permission(permission: Permission):
    def permission_checker(current_user: dict = Depends(get_current_user)):
        if not rbac_service.has_permission(current_user['role'], permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return permission_checker

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        # Connect to database
        await db_manager.connect()

        # Initialize chatbot service
        chatbot_service = ChatbotService()

        # Start real-time monitoring
        await realtime_monitor.start_monitoring()

        # Start SLA monitoring
        asyncio.create_task(auto_triage_service.start_sla_monitoring())

        logger.info("Dynamic IT Support System started successfully")

    except Exception as e:
        logger.error(f"Error during startup: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    try:
        await realtime_monitor.stop_monitoring()
        await db_manager.disconnect()
        logger.info("System shutdown complete")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_healthy = await db_manager.health_check()
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": "healthy" if db_healthy else "unhealthy",
            "monitoring": "active" if realtime_monitor.monitoring else "inactive"
        }
    }

# Authentication endpoints
@app.post("/api/auth/register")
async def register(user_data: UserCreate):
    """Register a new user"""
    user = await auth_service.register_user(user_data.dict())
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )

    # Create access token
    access_token = auth_service.create_access_token(
        data={"sub": user['id'], "type": "access"}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@app.post("/api/auth/login")
async def login(login_data: UserLogin):
    """Login user"""
    user = await auth_service.authenticate_user(
        login_data.username,
        login_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Create access token
    access_token = auth_service.create_access_token(
        data={"sub": user['id'], "type": "access"}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@app.get("/api/auth/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return current_user

# System monitoring endpoints
@app.get("/api/dashboard/health")
async def get_system_health(current_user: dict = Depends(require_permission(Permission.VIEW_METRICS))):
    """Get real-time system health metrics"""
    metrics = await realtime_monitor.get_current_metrics()
    return {
        "cpu_usage": metrics.get('cpu_usage', 0),
        "memory_usage": metrics.get('memory_usage', 0),
        "disk_usage": metrics.get('disk_usage', 0),
        "uptime_hours": metrics.get('uptime_hours', 0),
        "active_alerts": len(await realtime_monitor.get_alerts(limit=10)),
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/dashboard/metrics")
async def get_dashboard_metrics(
    hours: int = 24,
    current_user: dict = Depends(require_permission(Permission.VIEW_METRICS))
):
    """Get system metrics history"""
    try:
        db = await get_database()

        # Get metrics from database
        cutoff_time = datetime.now() - timedelta(hours=hours)

        cpu_metrics = await db.systemmetric.find_many(
            where={
                'metricType': 'cpu',
                'timestamp': {'gte': cutoff_time}
            },
            order_by={'timestamp': 'asc'}
        )

        memory_metrics = await db.systemmetric.find_many(
            where={
                'metricType': 'memory',
                'timestamp': {'gte': cutoff_time}
            },
            order_by={'timestamp': 'asc'}
        )

        disk_metrics = await db.systemmetric.find_many(
            where={
                'metricType': 'disk',
                'timestamp': {'gte': cutoff_time}
            },
            order_by={'timestamp': 'asc'}
        )

        # Format data for charts
        cpu_history = [
            {
                "timestamp": m.timestamp.isoformat(),
                "value": m.value
            } for m in cpu_metrics
        ]

        memory_history = [
            {
                "timestamp": m.timestamp.isoformat(),
                "value": m.value
            } for m in memory_metrics
        ]

        disk_history = [
            {
                "timestamp": m.timestamp.isoformat(),
                "value": m.value
            } for m in disk_metrics
        ]

        # Get current metrics
        current_metrics = await realtime_monitor.get_current_metrics()

        return {
            "system_health": {
                "cpu_usage": current_metrics.get('cpu_usage', 0),
                "memory_usage": current_metrics.get('memory_usage', 0),
                "disk_usage": current_metrics.get('disk_usage', 0),
                "uptime_hours": current_metrics.get('uptime_hours', 0),
                "active_alerts": len(await realtime_monitor.get_alerts(limit=10)),
                "status": "operational"
            },
            "cpu_history": cpu_history,
            "memory_history": memory_history,
            "disk_history": disk_history,
            "alerts": await realtime_monitor.get_alerts(limit=10)
        }

    except Exception as e:
        logger.error(f"Error getting dashboard metrics: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving metrics")

@app.get("/api/dashboard/logs")
async def get_system_logs(
    limit: int = 50,
    level: str = None,
    search: str = None,
    current_user: dict = Depends(require_permission(Permission.VIEW_LOGS))
):
    """Get system logs"""
    try:
        db = await get_database()

        where_clause = {}
        if level:
            where_clause['level'] = level.upper()
        if search:
            where_clause['message'] = {'contains': search}

        logs = await db.systemlog.find_many(
            where=where_clause,
            take=limit,
            order_by={'timestamp': 'desc'},
            include={'user': True}
        )

        return {
            "logs": [
                {
                    "id": log.id,
                    "level": log.level,
                    "source": log.source,
                    "message": log.message,
                    "timestamp": log.timestamp.isoformat(),
                    "user": log.user.username if log.user else None,
                    "metadata": json.loads(log.metadata) if log.metadata else None
                } for log in logs
            ],
            "total": len(logs)
        }

    except Exception as e:
        logger.error(f"Error getting system logs: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving logs")

# Ticket management endpoints
@app.get("/api/tickets")
async def get_tickets(
    status: str = None,
    priority: str = None,
    search: str = None,
    limit: int = 50,
    offset: int = 0,
    current_user: dict = Depends(require_permission(Permission.READ_TICKET))
):
    """Get tickets with filtering"""
    try:
        db = await get_database()

        where_clause = {}
        if status and status != "all":
            where_clause['status'] = status.upper()
        if priority and priority != "all":
            where_clause['priority'] = priority.upper()
        if search:
            where_clause['OR'] = [
                {'title': {'contains': search}},
                {'description': {'contains': search}},
                {'category': {'contains': search}}
            ]

        # Apply role-based filtering
        if current_user['role'] == 'CUSTOMER':
            where_clause['OR'] = [
                {'createdBy': current_user['id']},
                {'assignedTo': current_user['id']}
            ]

        tickets = await db.ticket.find_many(
            where=where_clause,
            skip=offset,
            take=limit,
            order_by={'createdAt': 'desc'},
            include={
                'creator': True,
                'assignee': True,
                'comments': True
            }
        )

        # Filter tickets based on access rights
        filtered_tickets = rbac_service.filter_tickets_by_access(
            current_user['role'],
            current_user['id'],
            tickets
        )

        return [
            {
                "id": ticket.id,
                "title": ticket.title,
                "description": ticket.description,
                "priority": ticket.priority,
                "status": ticket.status,
                "category": ticket.category,
                "tags": json.loads(ticket.tags) if ticket.tags else [],
                "assignedTo": ticket.assignedTo,
                "createdBy": ticket.createdBy,
                "createdAt": ticket.createdAt.isoformat(),
                "updatedAt": ticket.updatedAt.isoformat(),
                "resolvedAt": ticket.resolvedAt.isoformat() if ticket.resolvedAt else None,
                "slaDeadline": ticket.slaDeadline.isoformat() if ticket.slaDeadline else None,
                "escalationLevel": ticket.escalationLevel,
                "creator": {
                    "username": ticket.creator.username,
                    "fullName": ticket.creator.fullName
                } if ticket.creator else None,
                "assignee": {
                    "username": ticket.assignee.username,
                    "fullName": ticket.assignee.fullName
                } if ticket.assignee else None,
                "commentCount": len(ticket.comments)
            } for ticket in filtered_tickets
        ]

    except Exception as e:
        logger.error(f"Error getting tickets: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving tickets")

@app.post("/api/tickets")
async def create_ticket(
    ticket_data: TicketCreate,
    current_user: dict = Depends(require_permission(Permission.CREATE_TICKET))
):
    """Create a new ticket with auto-triage"""
    try:
        db = await get_database()

        # Auto-triage the ticket
        triage_result = await auto_triage_service.triage_ticket(ticket_data.dict())

        # Create ticket
        ticket = await db.ticket.create(
            data={
                'title': ticket_data.title,
                'description': ticket_data.description,
                'priority': triage_result['priority'],
                'category': triage_result['category'],
                'tags': json.dumps(ticket_data.tags),
                'assignedTo': triage_result['assigned_to'],
                'createdBy': current_user['id'],
                'slaDeadline': triage_result['sla_deadline'],
                'escalationLevel': triage_result['escalation_level']
            }
        )

        # Create SLA event
        await db.slaevent.create(
            data={
                'ticketId': ticket.id,
                'eventType': 'created',
                'metadata': json.dumps({
                    'auto_triaged': triage_result['auto_triaged'],
                    'priority': triage_result['priority'],
                    'category': triage_result['category']
                })
            }
        )

        # Broadcast real-time update
        await manager.broadcast(json.dumps({
            "type": "ticket_created",
            "ticket": {
                "id": ticket.id,
                "title": ticket.title,
                "priority": ticket.priority,
                "status": ticket.status
            }
        }))

        return {
            "id": ticket.id,
            "title": ticket.title,
            "description": ticket.description,
            "priority": ticket.priority,
            "status": ticket.status,
            "category": ticket.category,
            "tags": ticket_data.tags,
            "assignedTo": ticket.assignedTo,
            "createdBy": ticket.createdBy,
            "createdAt": ticket.createdAt.isoformat(),
            "slaDeadline": ticket.slaDeadline.isoformat() if ticket.slaDeadline else None,
            "autoTriaged": triage_result['auto_triaged']
        }

    except Exception as e:
        logger.error(f"Error creating ticket: {e}")
        raise HTTPException(status_code=500, detail="Error creating ticket")

@app.put("/api/tickets/{ticket_id}")
async def update_ticket(
    ticket_id: str,
    ticket_data: TicketUpdate,
    current_user: dict = Depends(require_permission(Permission.UPDATE_TICKET))
):
    """Update a ticket"""
    try:
        db = await get_database()

        # Check if user can modify this ticket
        ticket = await db.ticket.find_unique(where={'id': ticket_id})
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        if not rbac_service.can_modify_ticket(
            current_user['role'],
            current_user['id'],
            ticket.createdBy,
            ticket.assignedTo
        ):
            raise HTTPException(status_code=403, detail="Cannot modify this ticket")

        # Prepare update data
        update_data = {}
        if ticket_data.title is not None:
            update_data['title'] = ticket_data.title
        if ticket_data.description is not None:
            update_data['description'] = ticket_data.description
        if ticket_data.priority is not None:
            update_data['priority'] = ticket_data.priority.upper()
        if ticket_data.status is not None:
            update_data['status'] = ticket_data.status.upper()
        if ticket_data.category is not None:
            update_data['category'] = ticket_data.category
        if ticket_data.assignedTo is not None:
            update_data['assignedTo'] = ticket_data.assignedTo
        if ticket_data.tags is not None:
            update_data['tags'] = json.dumps(ticket_data.tags)

        # Update ticket
        updated_ticket = await db.ticket.update(
            where={'id': ticket_id},
            data=update_data
        )

        # Create SLA event
        await db.slaevent.create(
            data={
                'ticketId': ticket_id,
                'eventType': 'updated',
                'metadata': json.dumps(update_data)
            }
        )

        # Broadcast real-time update
        await manager.broadcast(json.dumps({
            "type": "ticket_updated",
            "ticket": {
                "id": updated_ticket.id,
                "title": updated_ticket.title,
                "priority": updated_ticket.priority,
                "status": updated_ticket.status
            }
        }))

        return {
            "id": updated_ticket.id,
            "title": updated_ticket.title,
            "description": updated_ticket.description,
            "priority": updated_ticket.priority,
            "status": updated_ticket.status,
            "category": updated_ticket.category,
            "tags": json.loads(updated_ticket.tags) if updated_ticket.tags else [],
            "assignedTo": updated_ticket.assignedTo,
            "updatedAt": updated_ticket.updatedAt.isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating ticket: {e}")
        raise HTTPException(status_code=500, detail="Error updating ticket")

# Chatbot endpoints
@app.post("/api/chatbot/chat")
async def chat_with_bot(
    chat_data: ChatMessage,
    current_user: dict = Depends(require_permission(Permission.USE_CHATBOT))
):
    """Chat with AI-powered chatbot"""
    try:
        chatbot_service = ChatbotService()

        # Get or create session
        session_id = chat_data.sessionId
        if not session_id:
            session_id = f"session_{current_user['id']}_{int(datetime.now().timestamp())}"

        # Get AI response
        response = await chatbot_service.get_ai_response(
            chat_data.message,
            current_user['id'],
            session_id
        )

        return {
            "response": response['content'],
            "sessionId": session_id,
            "confidenceScore": response['confidence'],
            "wasEscalated": response['escalated'],
            "ticketId": response.get('ticket_id')
        }

    except Exception as e:
        logger.error(f"Error in chatbot: {e}")
        raise HTTPException(status_code=500, detail="Error processing chat message")

# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = None):
    """WebSocket for real-time updates"""
    user_id = None
    if token:
        user = await auth_service.get_current_user(token)
        if user:
            user_id = user['id']

    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back for testing
            await manager.send_personal_message(f"Echo: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)

# Analytics endpoints
@app.get("/api/analytics/tickets")
async def get_ticket_analytics(
    current_user: dict = Depends(require_permission(Permission.VIEW_ANALYTICS))
):
    """Get ticket analytics"""
    try:
        db = await get_database()

        # Get ticket counts by status
        status_counts = {}
        for status in ['OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED']:
            count = await db.ticket.count(where={'status': status})
            status_counts[status.lower()] = count

        # Get ticket counts by priority
        priority_counts = {}
        for priority in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']:
            count = await db.ticket.count(where={'priority': priority})
            priority_counts[priority.lower()] = count

        # Get category breakdown
        tickets = await db.ticket.find_many()
        category_counts = {}
        for ticket in tickets:
            category = ticket.category
            category_counts[category] = category_counts.get(category, 0) + 1

        # Get SLA metrics
        sla_metrics = await auto_triage_service.get_sla_metrics()

        return {
            "total_tickets": sum(status_counts.values()),
            "status_counts": status_counts,
            "priority_counts": priority_counts,
            "category_counts": category_counts,
            "sla_metrics": sla_metrics
        }

    except Exception as e:
        logger.error(f"Error getting ticket analytics: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving analytics")

if __name__ == "__main__":
    uvicorn.run(
        "main_dynamic:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )


