# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication

All API endpoints (except auth endpoints) require authentication via JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### Authentication

#### POST /api/auth/register
Register a new user.

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "full_name": "string",
  "role": "customer" | "support_agent" | "admin"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "string",
  "email": "string",
  "full_name": "string",
  "role": "string",
  "is_active": true,
  "created_at": "2023-01-01T00:00:00Z"
}
```

#### POST /api/auth/login
Login with username and password.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

#### GET /api/auth/me
Get current user information.

**Response:**
```json
{
  "id": 1,
  "username": "string",
  "email": "string",
  "full_name": "string",
  "role": "string",
  "is_active": true,
  "created_at": "2023-01-01T00:00:00Z"
}
```

### Dashboard

#### GET /api/dashboard/health
Get current system health metrics.

**Response:**
```json
{
  "cpu_usage": 45.2,
  "memory_usage": 67.8,
  "disk_usage": 23.1,
  "uptime_hours": 72.5,
  "active_alerts": 2,
  "open_tickets": 5
}
```

#### GET /api/dashboard/metrics
Get comprehensive dashboard metrics.

**Query Parameters:**
- `hours` (optional): Number of hours of historical data (default: 24)

**Response:**
```json
{
  "system_health": {
    "cpu_usage": 45.2,
    "memory_usage": 67.8,
    "disk_usage": 23.1,
    "uptime_hours": 72.5,
    "active_alerts": 2,
    "open_tickets": 5
  },
  "cpu_history": [
    {
      "timestamp": "2023-01-01T00:00:00Z",
      "value": 45.2
    }
  ],
  "memory_history": [...],
  "disk_history": [...],
  "recent_alerts": [...],
  "recent_tickets": [...]
}
```

#### GET /api/dashboard/logs
Get system logs with optional filtering.

**Query Parameters:**
- `level` (optional): Log level filter
- `source` (optional): Log source filter
- `limit` (optional): Maximum number of logs (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "level": "INFO",
    "message": "System health check completed",
    "source": "health_monitor",
    "hostname": "server-01",
    "timestamp": "2023-01-01T00:00:00Z",
    "metadata": "{}"
  }
]
```

### Tickets

#### GET /api/tickets
Get tickets with optional filtering.

**Query Parameters:**
- `skip` (optional): Number of tickets to skip (default: 0)
- `limit` (optional): Maximum number of tickets (default: 100)
- `status` (optional): Filter by status
- `priority` (optional): Filter by priority
- `assigned_to` (optional): Filter by assignee

**Response:**
```json
[
  {
    "id": 1,
    "title": "Server down",
    "description": "Production server is not responding",
    "priority": "critical",
    "status": "open",
    "category": "system_down",
    "created_by": 1,
    "assigned_to": null,
    "auto_categorized": true,
    "confidence_score": 0.95,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "resolved_at": null
  }
]
```

#### POST /api/tickets
Create a new ticket.

**Request Body:**
```json
{
  "title": "string",
  "description": "string",
  "priority": "low" | "medium" | "high" | "critical",
  "category": "system_down" | "performance_issue" | "password_reset" | "software_installation" | "hardware_issue" | "network_issue" | "other"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "string",
  "description": "string",
  "priority": "medium",
  "status": "open",
  "category": "other",
  "created_by": 1,
  "assigned_to": null,
  "auto_categorized": true,
  "confidence_score": 0.75,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "resolved_at": null
}
```

#### GET /api/tickets/{ticket_id}
Get a specific ticket.

**Response:**
```json
{
  "id": 1,
  "title": "string",
  "description": "string",
  "priority": "medium",
  "status": "open",
  "category": "other",
  "created_by": 1,
  "assigned_to": null,
  "auto_categorized": true,
  "confidence_score": 0.75,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "resolved_at": null
}
```

#### PUT /api/tickets/{ticket_id}
Update a ticket.

**Request Body:**
```json
{
  "title": "string",
  "description": "string",
  "priority": "low" | "medium" | "high" | "critical",
  "status": "open" | "in_progress" | "resolved" | "closed" | "cancelled",
  "category": "system_down" | "performance_issue" | "password_reset" | "software_installation" | "hardware_issue" | "network_issue" | "other",
  "assigned_to": 1
}
```

**Response:**
```json
{
  "id": 1,
  "title": "string",
  "description": "string",
  "priority": "medium",
  "status": "in_progress",
  "category": "other",
  "created_by": 1,
  "assigned_to": 2,
  "auto_categorized": true,
  "confidence_score": 0.75,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T01:00:00Z",
  "resolved_at": null
}
```

#### DELETE /api/tickets/{ticket_id}
Delete a ticket (admin only).

**Response:**
```json
{
  "message": "Ticket deleted successfully"
}
```

#### GET /api/tickets/analytics/summary
Get ticket analytics summary.

**Response:**
```json
{
  "status_counts": {
    "open": 5,
    "in_progress": 3,
    "resolved": 12,
    "closed": 8
  },
  "priority_counts": {
    "low": 8,
    "medium": 12,
    "high": 5,
    "critical": 3
  },
  "category_counts": {
    "system_down": 2,
    "performance_issue": 5,
    "password_reset": 8,
    "other": 13
  },
  "total_tickets": 28,
  "avg_resolution_time_hours": 4.5
}
```

### Chatbot

#### POST /api/chatbot/chat
Send a message to the chatbot.

**Request Body:**
```json
{
  "message": "string",
  "session_id": "string" // optional
}
```

**Response:**
```json
{
  "response": "string",
  "session_id": "string",
  "confidence_score": 0.85,
  "was_escalated": false,
  "ticket_id": null
}
```

#### GET /api/chatbot/faqs
Get FAQ entries with optional filtering.

**Query Parameters:**
- `category` (optional): Filter by category
- `search` (optional): Search in questions and answers

**Response:**
```json
[
  {
    "id": 1,
    "question": "How do I reset my password?",
    "answer": "You can reset your password by clicking 'Forgot Password' on the login page.",
    "category": "Authentication",
    "tags": ["password", "reset", "login"],
    "is_active": true,
    "created_at": "2023-01-01T00:00:00Z"
  }
]
```

#### POST /api/chatbot/faqs
Create a new FAQ entry (admin/support agent only).

**Request Body:**
```json
{
  "question": "string",
  "answer": "string",
  "category": "string",
  "tags": ["string"] // optional
}
```

**Response:**
```json
{
  "id": 1,
  "question": "string",
  "answer": "string",
  "category": "string",
  "tags": ["string"],
  "is_active": true,
  "created_at": "2023-01-01T00:00:00Z"
}
```

#### GET /api/chatbot/analytics
Get chatbot analytics (admin/support agent only).

**Response:**
```json
{
  "total_queries": 150,
  "escalated_queries": 25,
  "escalation_rate": 16.67,
  "avg_confidence_score": 0.82,
  "common_queries": [
    {
      "query": "How do I reset my password?",
      "count": 15
    }
  ]
}
```

#### GET /api/chatbot/logs
Get chatbot conversation logs (admin/support agent only).

**Query Parameters:**
- `session_id` (optional): Filter by session ID
- `escalated_only` (optional): Show only escalated queries
- `limit` (optional): Maximum number of logs (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "session_id": "string",
    "user_query": "How do I reset my password?",
    "bot_response": "You can reset your password by...",
    "confidence_score": 0.85,
    "was_escalated": false,
    "ticket_id": null,
    "response_time_ms": 1200,
    "created_at": "2023-01-01T00:00:00Z"
  }
]
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

API endpoints are rate limited to prevent abuse. Rate limits are configurable and may vary by endpoint.

## WebSocket Support

Real-time updates are available via WebSocket connections for:
- System metrics updates
- New alerts
- Ticket status changes
- Chatbot messages

WebSocket endpoint: `ws://localhost:8000/ws`

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

