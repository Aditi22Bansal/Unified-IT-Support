from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base

class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    tags = Column(Text, nullable=True)  # JSON string of tags
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<FAQ(id={self.id}, question='{self.question[:50]}...', category='{self.category}')>"

class ChatbotLog(Base):
    __tablename__ = "chatbot_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String(100), nullable=False)
    user_query = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=True)
    confidence_score = Column(Float, nullable=True)
    was_escalated = Column(Boolean, default=False)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="chatbot_logs")
    ticket = relationship("Ticket", back_populates="chatbot_logs")

    def __repr__(self):
        return f"<ChatbotLog(id={self.id}, query='{self.user_query[:50]}...', escalated={self.was_escalated})>"

