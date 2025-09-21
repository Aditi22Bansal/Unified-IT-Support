from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import uuid

from database.connection import get_db
from database.models.user import User
from database.models.chatbot import FAQ, ChatbotLog
from database.models.ticket import Ticket, TicketPriority, TicketCategory
from services.auth import get_current_active_user
from services.simple_chatbot_service import chatbot_service

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    confidence_score: Optional[float] = None
    was_escalated: bool = False
    ticket_id: Optional[int] = None

class FAQCreate(BaseModel):
    question: str
    answer: str
    category: str
    tags: Optional[List[str]] = None

class FAQResponse(BaseModel):
    id: int
    question: str
    answer: str
    category: str
    tags: Optional[List[str]] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(
    chat_message: ChatMessage,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Chat with the AI-powered FAQ bot."""
    # Generate session ID if not provided
    session_id = chat_message.session_id or str(uuid.uuid4())

# Use simple chatbot service

    # Get bot response
    response = await chatbot_service.process_message(
        message=chat_message.message,
        user_id=current_user.id
    )

    return response

@router.get("/faqs", response_model=List[FAQResponse])
async def get_faqs(
    category: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get FAQ entries with optional filtering."""
    query = db.query(FAQ).filter(FAQ.is_active == True)

    if category:
        query = query.filter(FAQ.category == category)

    if search:
        query = query.filter(
            FAQ.question.contains(search) | FAQ.answer.contains(search)
        )

    faqs = query.order_by(FAQ.category, FAQ.question).all()

    # Convert tags from JSON string to list
    result = []
    for faq in faqs:
        faq_dict = {
            "id": faq.id,
            "question": faq.question,
            "answer": faq.answer,
            "category": faq.category,
            "tags": faq.tags.split(",") if faq.tags else [],
            "is_active": faq.is_active,
            "created_at": faq.created_at
        }
        result.append(faq_dict)

    return result

@router.post("/faqs", response_model=FAQResponse)
async def create_faq(
    faq_data: FAQCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new FAQ entry (admin/support agent only)."""
    if current_user.role not in ["admin", "support_agent"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Create FAQ
    faq = FAQ(
        question=faq_data.question,
        answer=faq_data.answer,
        category=faq_data.category,
        tags=",".join(faq_data.tags) if faq_data.tags else None
    )

    db.add(faq)
    db.commit()
    db.refresh(faq)

    return {
        "id": faq.id,
        "question": faq.question,
        "answer": faq.answer,
        "category": faq.category,
        "tags": faq.tags.split(",") if faq.tags else [],
        "is_active": faq.is_active,
        "created_at": faq.created_at
    }

@router.get("/analytics")
async def get_chatbot_analytics(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get chatbot analytics (admin/support agent only)."""
    if current_user.role not in ["admin", "support_agent"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Get total queries
    total_queries = db.query(ChatbotLog).count()

    # Get escalated queries
    escalated_queries = db.query(ChatbotLog).filter(
        ChatbotLog.was_escalated == True
    ).count()

    # Get average confidence score
    avg_confidence = db.query(db.func.avg(ChatbotLog.confidence_score)).filter(
        ChatbotLog.confidence_score.isnot(None)
    ).scalar() or 0

    # Get most common queries
    common_queries = db.query(
        ChatbotLog.user_query,
        db.func.count(ChatbotLog.id)
    ).group_by(ChatbotLog.user_query).order_by(
        db.func.count(ChatbotLog.id).desc()
    ).limit(10).all()

    # Get escalation rate
    escalation_rate = (escalated_queries / total_queries * 100) if total_queries > 0 else 0

    return {
        "total_queries": total_queries,
        "escalated_queries": escalated_queries,
        "escalation_rate": round(escalation_rate, 2),
        "avg_confidence_score": round(avg_confidence, 2),
        "common_queries": [
            {"query": query, "count": count}
            for query, count in common_queries
        ]
    }

@router.get("/logs")
async def get_chatbot_logs(
    session_id: Optional[str] = None,
    escalated_only: bool = False,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get chatbot conversation logs (admin/support agent only)."""
    if current_user.role not in ["admin", "support_agent"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    query = db.query(ChatbotLog)

    if session_id:
        query = query.filter(ChatbotLog.session_id == session_id)

    if escalated_only:
        query = query.filter(ChatbotLog.was_escalated == True)

    logs = query.order_by(ChatbotLog.created_at.desc()).limit(limit).all()

    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "session_id": log.session_id,
            "user_query": log.user_query,
            "bot_response": log.bot_response,
            "confidence_score": log.confidence_score,
            "was_escalated": log.was_escalated,
            "ticket_id": log.ticket_id,
            "response_time_ms": log.response_time_ms,
            "created_at": log.created_at
        }
        for log in logs
    ]

