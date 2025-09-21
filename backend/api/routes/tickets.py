from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from database.connection import get_db
from database.models.ticket import Ticket, TicketPriority, TicketStatus, TicketCategory
from database.models.user import User, UserRole
from services.auth import get_current_active_user
from services.ticket_triage import TicketTriageService

router = APIRouter()

class TicketCreate(BaseModel):
    title: str
    description: str
    priority: Optional[TicketPriority] = None
    category: Optional[TicketCategory] = None

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TicketPriority] = None
    status: Optional[TicketStatus] = None
    category: Optional[TicketCategory] = None
    assigned_to: Optional[int] = None

class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: TicketPriority
    status: TicketStatus
    category: TicketCategory
    created_by: int
    assigned_to: Optional[int]
    auto_categorized: bool
    confidence_score: Optional[float]
    created_at: datetime
    updated_at: Optional[datetime]
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True

@router.post("/", response_model=TicketResponse)
async def create_ticket(
    ticket_data: TicketCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new ticket."""
    # Initialize triage service
    triage_service = TicketTriageService()

    # Auto-triage the ticket
    triage_result = triage_service.triage_ticket(
        title=ticket_data.title,
        description=ticket_data.description
    )

    # Create ticket
    db_ticket = Ticket(
        title=ticket_data.title,
        description=ticket_data.description,
        priority=ticket_data.priority or triage_result["priority"],
        category=ticket_data.category or triage_result["category"],
        created_by=current_user.id,
        auto_categorized=ticket_data.priority is None or ticket_data.category is None,
        confidence_score=triage_result["confidence_score"]
    )

    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)

    # If high priority, trigger immediate actions
    if db_ticket.priority in [TicketPriority.HIGH, TicketPriority.CRITICAL]:
        # This would trigger alerts, notifications, etc.
        pass

    return db_ticket

@router.get("/", response_model=List[TicketResponse])
async def get_tickets(
    skip: int = 0,
    limit: int = 100,
    status: Optional[TicketStatus] = None,
    priority: Optional[TicketPriority] = None,
    assigned_to: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get tickets with optional filtering."""
    query = db.query(Ticket)

    # Apply filters
    if status:
        query = query.filter(Ticket.status == status)
    if priority:
        query = query.filter(Ticket.priority == priority)
    if assigned_to:
        query = query.filter(Ticket.assigned_to == assigned_to)

    # Customers can only see their own tickets
    if current_user.role == UserRole.CUSTOMER:
        query = query.filter(Ticket.created_by == current_user.id)

    tickets = query.order_by(desc(Ticket.created_at)).offset(skip).limit(limit).all()
    return tickets

@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific ticket."""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Check permissions
    if (current_user.role == UserRole.CUSTOMER and
        ticket.created_by != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return ticket

@router.put("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: int,
    ticket_update: TicketUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a ticket."""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Check permissions
    if (current_user.role == UserRole.CUSTOMER and
        ticket.created_by != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Update fields
    update_data = ticket_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ticket, field, value)

    # Set resolved_at if status is resolved
    if ticket_update.status == TicketStatus.RESOLVED and not ticket.resolved_at:
        ticket.resolved_at = datetime.utcnow()

    db.commit()
    db.refresh(ticket)

    return ticket

@router.delete("/{ticket_id}")
async def delete_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a ticket (admin only)."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    db.delete(ticket)
    db.commit()

    return {"message": "Ticket deleted successfully"}

@router.get("/analytics/summary")
async def get_ticket_analytics(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get ticket analytics summary."""
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPPORT_AGENT]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Count tickets by status
    status_counts = db.query(
        Ticket.status,
        db.func.count(Ticket.id)
    ).group_by(Ticket.status).all()

    # Count tickets by priority
    priority_counts = db.query(
        Ticket.priority,
        db.func.count(Ticket.id)
    ).group_by(Ticket.priority).all()

    # Count tickets by category
    category_counts = db.query(
        Ticket.category,
        db.func.count(Ticket.id)
    ).group_by(Ticket.category).all()

    # Calculate average resolution time
    resolved_tickets = db.query(Ticket).filter(
        Ticket.status == TicketStatus.RESOLVED,
        Ticket.resolved_at.isnot(None)
    ).all()

    avg_resolution_time = 0
    if resolved_tickets:
        total_time = sum([
            (ticket.resolved_at - ticket.created_at).total_seconds()
            for ticket in resolved_tickets
        ])
        avg_resolution_time = total_time / len(resolved_tickets) / 3600  # in hours

    return {
        "status_counts": dict(status_counts),
        "priority_counts": dict(priority_counts),
        "category_counts": dict(category_counts),
        "total_tickets": db.query(Ticket).count(),
        "avg_resolution_time_hours": round(avg_resolution_time, 2)
    }

