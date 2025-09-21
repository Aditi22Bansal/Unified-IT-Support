from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, Float
from sqlalchemy.sql import func
from database.connection import Base
import enum

class AlertSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertStatus(str, enum.Enum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(Enum(AlertSeverity), nullable=False)
    status = Column(Enum(AlertStatus), default=AlertStatus.ACTIVE, nullable=False)

    # Alert source and context
    source = Column(String(100), nullable=False)  # system, application, service
    metric_name = Column(String(100), nullable=True)  # cpu_usage, memory_usage, etc.
    threshold_value = Column(Float, nullable=True)
    current_value = Column(Float, nullable=True)

    # Timestamps
    triggered_at = Column(DateTime(timezone=True), server_default=func.now())
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    # Notification status
    email_sent = Column(Boolean, default=False)
    slack_sent = Column(Boolean, default=False)

    # Additional metadata
    meta_data = Column(Text, nullable=True)  # JSON string for additional data

    def __repr__(self):
        return f"<Alert(id={self.id}, title='{self.title}', severity='{self.severity}', status='{self.status}')>"

