"""
Simple chatbot service without Prisma dependencies
"""
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class SimpleChatbotService:
    def __init__(self):
        self.responses = {
            "hello": "Hello! How can I help you today?",
            "help": "I can help you with IT support issues. Please describe your problem.",
            "password": "For password reset, please contact your system administrator or use the password reset feature.",
            "email": "For email issues, please check your internet connection and try again.",
            "slow": "For performance issues, please restart your application and check for updates.",
            "error": "I understand you're experiencing an error. Can you provide more details about what happened?"
        }

    async def process_message(self, message: str, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Process a chatbot message and return a response"""
        try:
            message_lower = message.lower()

            # Simple keyword matching
            for keyword, response in self.responses.items():
                if keyword in message_lower:
                    return {
                        "response": response,
                        "confidence": 0.8,
                        "escalated": False
                    }

            # Default response
            return {
                "response": "I understand you need help. Let me connect you with a support agent.",
                "confidence": 0.3,
                "escalated": True
            }

        except Exception as e:
            logger.error(f"Error processing chatbot message: {e}")
            return {
                "response": "I'm sorry, I encountered an error. Please try again or contact support.",
                "confidence": 0.0,
                "escalated": True
            }

# Global service instance
chatbot_service = SimpleChatbotService()
