from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List, Dict, Any
from pydantic import BaseModel

from database.connection import get_db
from database.models.system_metric import SystemMetric, SystemLog
from database.models.alert import Alert, AlertStatus
from database.models.ticket import Ticket, TicketStatus
from services.auth import get_current_active_user
from database.models.user import User

router = APIRouter()

class SystemHealthResponse(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    uptime_hours: float
    active_alerts: int
    open_tickets: int

class MetricDataPoint(BaseModel):
    timestamp: datetime
    value: float

class DashboardMetricsResponse(BaseModel):
    system_health: SystemHealthResponse
    cpu_history: List[MetricDataPoint]
    memory_history: List[MetricDataPoint]
    disk_history: List[MetricDataPoint]
    recent_alerts: List[Dict[str, Any]]
    recent_tickets: List[Dict[str, Any]]

@router.get("/health", response_model=SystemHealthResponse)
async def get_system_health(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current system health metrics."""
    # Get latest metrics
    latest_cpu = db.query(SystemMetric).filter(
        SystemMetric.metric_name == "cpu_usage"
    ).order_by(desc(SystemMetric.timestamp)).first()

    latest_memory = db.query(SystemMetric).filter(
        SystemMetric.metric_name == "memory_usage"
    ).order_by(desc(SystemMetric.timestamp)).first()

    latest_disk = db.query(SystemMetric).filter(
        SystemMetric.metric_name == "disk_usage"
    ).order_by(desc(SystemMetric.timestamp)).first()

    latest_uptime = db.query(SystemMetric).filter(
        SystemMetric.metric_name == "uptime_hours"
    ).order_by(desc(SystemMetric.timestamp)).first()

    # Count active alerts
    active_alerts = db.query(Alert).filter(
        Alert.status == AlertStatus.ACTIVE
    ).count()

    # Count open tickets
    open_tickets = db.query(Ticket).filter(
        Ticket.status.in_([TicketStatus.OPEN, TicketStatus.IN_PROGRESS])
    ).count()

    return SystemHealthResponse(
        cpu_usage=latest_cpu.metric_value if latest_cpu else 0.0,
        memory_usage=latest_memory.metric_value if latest_memory else 0.0,
        disk_usage=latest_disk.metric_value if latest_disk else 0.0,
        uptime_hours=latest_uptime.metric_value if latest_uptime else 0.0,
        active_alerts=active_alerts,
        open_tickets=open_tickets
    )

@router.get("/metrics", response_model=DashboardMetricsResponse)
async def get_dashboard_metrics(
    hours: int = 24,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive dashboard metrics."""
    # Calculate time range
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    # Get system health
    system_health = await get_system_health(current_user, db)

    # Get metric history
    cpu_history = db.query(SystemMetric).filter(
        SystemMetric.metric_name == "cpu_usage",
        SystemMetric.timestamp >= start_time
    ).order_by(SystemMetric.timestamp).all()

    memory_history = db.query(SystemMetric).filter(
        SystemMetric.metric_name == "memory_usage",
        SystemMetric.timestamp >= start_time
    ).order_by(SystemMetric.timestamp).all()

    disk_history = db.query(SystemMetric).filter(
        SystemMetric.metric_name == "disk_usage",
        SystemMetric.timestamp >= start_time
    ).order_by(SystemMetric.timestamp).all()

    # Get recent alerts
    recent_alerts = db.query(Alert).filter(
        Alert.timestamp >= start_time
    ).order_by(desc(Alert.timestamp)).limit(10).all()

    # Get recent tickets
    recent_tickets = db.query(Ticket).filter(
        Ticket.created_at >= start_time
    ).order_by(desc(Ticket.created_at)).limit(10).all()

    return DashboardMetricsResponse(
        system_health=system_health,
        cpu_history=[
            MetricDataPoint(timestamp=m.timestamp, value=m.metric_value)
            for m in cpu_history
        ],
        memory_history=[
            MetricDataPoint(timestamp=m.timestamp, value=m.metric_value)
            for m in memory_history
        ],
        disk_history=[
            MetricDataPoint(timestamp=m.timestamp, value=m.metric_value)
            for m in disk_history
        ],
        recent_alerts=[
            {
                "id": alert.id,
                "title": alert.title,
                "severity": alert.severity,
                "status": alert.status,
                "timestamp": alert.timestamp
            }
            for alert in recent_alerts
        ],
        recent_tickets=[
            {
                "id": ticket.id,
                "title": ticket.title,
                "priority": ticket.priority,
                "status": ticket.status,
                "created_at": ticket.created_at
            }
            for ticket in recent_tickets
        ]
    )

@router.get("/logs")
async def get_system_logs(
    level: str = None,
    source: str = None,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get system logs with optional filtering."""
    query = db.query(SystemLog)

    if level:
        query = query.filter(SystemLog.level == level.upper())

    if source:
        query = query.filter(SystemLog.source == source)

    logs = query.order_by(desc(SystemLog.timestamp)).limit(limit).all()

    return [
        {
            "id": log.id,
            "level": log.level,
            "message": log.message,
            "source": log.source,
            "hostname": log.hostname,
            "timestamp": log.timestamp,
            "metadata": log.metadata
        }
        for log in logs
    ]

