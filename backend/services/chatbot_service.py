"""
AI-powered chatbot service with OpenRouter integration
"""
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from database.prisma_client import get_database
import openai
import logging

logger = logging.getLogger(__name__)

class ChatbotService:
    def __init__(self):
        # Configure OpenRouter
        openai.api_key = "sk-or-v1-3122"  # Your OpenRouter API key
        openai.api_base = "https://openrouter.ai/api/v1"

        self.model = "openai/gpt-3.5-turbo"
        self.max_tokens = 1000
        self.temperature = 0.7

        # FAQ knowledge base
        self.faq_responses = {
            "password": "To reset your password, go to the login page and click 'Forgot Password'. You'll receive an email with reset instructions.",
            "login": "If you're having trouble logging in, make sure you're using the correct username and password. Check if Caps Lock is on.",
            "email": "For email issues, check your internet connection and try refreshing the page. If problems persist, contact IT support.",
            "network": "Network issues can be resolved by checking your internet connection, restarting your router, or contacting your ISP.",
            "software": "For software installation issues, ensure you have administrator privileges and sufficient disk space.",
            "hardware": "Hardware problems should be reported immediately. Include details about the device and error messages.",
            "account": "Account-related issues can be resolved by contacting the system administrator or IT support team.",
            "access": "If you're having access issues, verify your permissions with your manager or IT support.",
            "backup": "Regular backups are automatically performed. For manual backup requests, contact IT support.",
            "security": "Security concerns should be reported immediately to the IT security team."
        }

    async def get_ai_response(self, message: str, user_id: str, session_id: str) -> Dict:
        """Get AI response for user message"""
        try:
            # Check if message should be escalated
            escalation_needed = await self._should_escalate(message)

            if escalation_needed:
                return await self._escalate_to_human(message, user_id, session_id)

            # Get AI response
            ai_response = await self._get_openai_response(message)

            # Store conversation
            await self._store_conversation(session_id, message, ai_response, user_id)

            return {
                "content": ai_response,
                "confidence": 0.9,
                "escalated": False,
                "ticket_id": None
            }

        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            return {
                "content": "I apologize, but I'm having trouble processing your request right now. Please try again later or contact support.",
                "confidence": 0.0,
                "escalated": True,
                "ticket_id": None
            }

    async def _should_escalate(self, message: str) -> bool:
        """Determine if message should be escalated to human"""
        escalation_keywords = [
            "urgent", "emergency", "critical", "asap", "immediately",
            "not working", "broken", "error", "failed", "cannot access",
            "security", "breach", "hack", "virus", "malware",
            "data loss", "corrupted", "crash", "down"
        ]

        message_lower = message.lower()
        for keyword in escalation_keywords:
            if keyword in message_lower:
                return True

        return False

    async def _escalate_to_human(self, message: str, user_id: str, session_id: str) -> Dict:
        """Escalate message to human support"""
        try:
            db = await get_database()

            # Create ticket
            ticket = await db.ticket.create(
                data={
                    'title': f"Chatbot Escalation: {message[:50]}...",
                    'description': f"Escalated from chatbot session {session_id}:\n\n{message}",
                    'priority': 'HIGH',
                    'category': 'General',
                    'createdBy': user_id,
                    'status': 'OPEN'
                }
            )

            # Store escalation
            await self._store_conversation(
                session_id,
                message,
                f"I've escalated your request to human support. Ticket #{ticket.id} has been created.",
                user_id,
                escalated=True,
                ticket_id=ticket.id
            )

            return {
                "content": f"I've escalated your request to human support. A ticket has been created (#{ticket.id}) and our team will assist you shortly.",
                "confidence": 1.0,
                "escalated": True,
                "ticket_id": ticket.id
            }

        except Exception as e:
            logger.error(f"Error escalating to human: {e}")
            return {
                "content": "I've escalated your request to human support. Our team will assist you shortly.",
                "confidence": 1.0,
                "escalated": True,
                "ticket_id": None
            }

    async def _get_openai_response(self, message: str) -> str:
        """Get response from OpenAI via OpenRouter"""
        try:
            # Build context with FAQ knowledge
            context = self._build_context(message)

            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are an AI IT support assistant. Help users with common IT issues.

                        Context: {context}

                        Guidelines:
                        - Be helpful and professional
                        - Provide step-by-step solutions when possible
                        - Ask clarifying questions if needed
                        - If you can't help, suggest contacting human support
                        - Keep responses concise but informative
                        - Use markdown formatting for better readability
                        """
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error getting OpenAI response: {e}")
            return "I apologize, but I'm having trouble connecting to my AI service right now. Please try again later or contact support."

    def _build_context(self, message: str) -> str:
        """Build context from FAQ knowledge base"""
        message_lower = message.lower()
        relevant_faqs = []

        for keyword, response in self.faq_responses.items():
            if keyword in message_lower:
                relevant_faqs.append(f"Q: {keyword.title()}\nA: {response}")

        if relevant_faqs:
            return "Relevant FAQ information:\n" + "\n\n".join(relevant_faqs)

        return "No specific FAQ matches found."

    async def _store_conversation(self, session_id: str, user_message: str,
                                bot_response: str, user_id: str,
                                escalated: bool = False, ticket_id: str = None):
        """Store conversation in database"""
        try:
            db = await get_database()

            # Get or create session
            session = await db.chatbotsession.find_unique(where={'sessionId': session_id})
            if not session:
                session = await db.chatbotsession.create(
                    data={
                        'sessionId': session_id,
                        'userId': user_id,
                        'isActive': True
                    }
                )

            # Store user message
            await db.chatbotmessage.create(
                data={
                    'sessionId': session_id,
                    'content': user_message,
                    'isUser': True,
                    'wasEscalated': escalated,
                    'ticketId': ticket_id
                }
            )

            # Store bot response
            await db.chatbotmessage.create(
                data={
                    'sessionId': session_id,
                    'content': bot_response,
                    'isUser': False,
                    'confidence': 0.9 if not escalated else 1.0,
                    'wasEscalated': escalated,
                    'ticketId': ticket_id
                }
            )

        except Exception as e:
            logger.error(f"Error storing conversation: {e}")

    async def get_chat_history(self, session_id: str) -> List[Dict]:
        """Get chat history for a session"""
        try:
            db = await get_database()

            messages = await db.chatbotmessage.find_many(
                where={'sessionId': session_id},
                order_by={'createdAt': 'asc'}
            )

            return [
                {
                    "id": msg.id,
                    "content": msg.content,
                    "isUser": msg.isUser,
                    "confidence": msg.confidence,
                    "wasEscalated": msg.wasEscalated,
                    "ticketId": msg.ticketId,
                    "createdAt": msg.createdAt.isoformat()
                } for msg in messages
            ]

        except Exception as e:
            logger.error(f"Error getting chat history: {e}")
            return []

    async def get_chatbot_analytics(self) -> Dict:
        """Get chatbot analytics"""
        try:
            db = await get_database()

            # Get total messages
            total_messages = await db.chatbotmessage.count()
            user_messages = await db.chatbotmessage.count(where={'isUser': True})
            bot_messages = await db.chatbotmessage.count(where={'isUser': False})

            # Get escalation rate
            escalated_messages = await db.chatbotmessage.count(where={'wasEscalated': True})
            escalation_rate = (escalated_messages / user_messages * 100) if user_messages > 0 else 0

            # Get active sessions
            active_sessions = await db.chatbotsession.count(where={'isActive': True})

            # Get recent activity
            recent_messages = await db.chatbotmessage.find_many(
                take=10,
                order_by={'createdAt': 'desc'},
                include={'session': {'include': {'user': True}}}
            )

            return {
                "total_messages": total_messages,
                "user_messages": user_messages,
                "bot_messages": bot_messages,
                "escalation_rate": round(escalation_rate, 2),
                "active_sessions": active_sessions,
                "recent_messages": [
                    {
                        "id": msg.id,
                        "content": msg.content[:100] + "..." if len(msg.content) > 100 else msg.content,
                        "isUser": msg.isUser,
                        "wasEscalated": msg.wasEscalated,
                        "user": msg.session.user.username if msg.session.user else "Anonymous",
                        "createdAt": msg.createdAt.isoformat()
                    } for msg in recent_messages
                ]
            }

        except Exception as e:
            logger.error(f"Error getting chatbot analytics: {e}")
            return {}

    async def update_faq(self, question: str, answer: str, category: str = "General"):
        """Update FAQ knowledge base"""
        try:
            db = await get_database()

            # Check if FAQ exists
            existing_faq = await db.faq.find_first(where={'question': question})

            if existing_faq:
                # Update existing FAQ
                await db.faq.update(
                    where={'id': existing_faq.id},
                    data={
                        'answer': answer,
                        'category': category,
                        'updatedAt': datetime.now()
                    }
                )
            else:
                # Create new FAQ
                await db.faq.create(
                    data={
                        'question': question,
                        'answer': answer,
                        'category': category,
                        'isActive': True
                    }
                )

            # Update in-memory knowledge base
            self.faq_responses[question.lower()] = answer

            return True

        except Exception as e:
            logger.error(f"Error updating FAQ: {e}")
            return False

    async def get_faq_list(self) -> List[Dict]:
        """Get list of FAQs"""
        try:
            db = await get_database()

            faqs = await db.faq.find_many(
                where={'isActive': True},
                order_by={'createdAt': 'desc'}
            )

            return [
                {
                    "id": faq.id,
                    "question": faq.question,
                    "answer": faq.answer,
                    "category": faq.category,
                    "viewCount": faq.viewCount,
                    "helpfulCount": faq.helpfulCount,
                    "createdAt": faq.createdAt.isoformat()
                } for faq in faqs
            ]

        except Exception as e:
            logger.error(f"Error getting FAQ list: {e}")
            return []

# Global chatbot service instance
chatbot_service = ChatbotService()