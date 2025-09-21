from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base
import enum

class TicketPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TicketStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class TicketCategory(str, enum.Enum):
    SYSTEM_DOWN = "system_down"
    PERFORMANCE_ISSUE = "performance_issue"
    PASSWORD_RESET = "password_reset"
    SOFTWARE_INSTALLATION = "software_installation"
    HARDWARE_ISSUE = "hardware_issue"
    NETWORK_ISSUE = "network_issue"
    OTHER = "other"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(Enum(TicketPriority), default=TicketPriority.MEDIUM, nullable=False)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN, nullable=False)
    category = Column(Enum(TicketCategory), default=TicketCategory.OTHER, nullable=False)

    # Foreign keys
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    # Auto-triage fields
    auto_categorized = Column(Boolean, default=False)
    confidence_score = Column(Float, nullable=True)

    # Relationships
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_tickets")
    assignee = relationship("User", foreign_keys=[assigned_to], back_populates="assigned_tickets")

    def __repr__(self):
        return f"<Ticket(id={self.id}, title='{self.title}', priority='{self.priority}', status='{self.status}')>"

