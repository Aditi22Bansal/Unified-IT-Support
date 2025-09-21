import re
from typing import Dict, Any
from database.models.ticket import TicketPriority, TicketCategory

class TicketTriageService:
    """Service for automatically triaging tickets based on content analysis."""

    def __init__(self):
        # Define keywords and patterns for each category and priority
        self.priority_keywords = {
            TicketPriority.CRITICAL: [
                "down", "outage", "critical", "emergency", "urgent", "broken",
                "not working", "failed", "error", "crash", "fatal"
            ],
            TicketPriority.HIGH: [
                "slow", "performance", "issue", "problem", "bug", "not responding",
                "timeout", "connection", "access", "login", "authentication"
            ],
            TicketPriority.MEDIUM: [
                "request", "help", "question", "information", "guidance",
                "how to", "tutorial", "documentation"
            ],
            TicketPriority.LOW: [
                "password", "reset", "change", "update", "modify", "preference",
                "setting", "configuration"
            ]
        }

        self.category_keywords = {
            TicketCategory.SYSTEM_DOWN: [
                "down", "outage", "offline", "unavailable", "not accessible",
                "server down", "service down", "system down"
            ],
            TicketCategory.PERFORMANCE_ISSUE: [
                "slow", "performance", "lag", "timeout", "response time",
                "bottleneck", "optimization"
            ],
            TicketCategory.PASSWORD_RESET: [
                "password", "reset", "forgot", "locked", "unlock", "change password"
            ],
            TicketCategory.SOFTWARE_INSTALLATION: [
                "install", "installation", "setup", "configure", "deploy",
                "software", "application", "program"
            ],
            TicketCategory.HARDWARE_ISSUE: [
                "hardware", "device", "printer", "scanner", "monitor",
                "keyboard", "mouse", "physical"
            ],
            TicketCategory.NETWORK_ISSUE: [
                "network", "connection", "wifi", "ethernet", "internet",
                "connectivity", "dns", "ip", "vpn"
            ]
        }

    def triage_ticket(self, title: str, description: str) -> Dict[str, Any]:
        """
        Analyze ticket content and determine priority and category.

        Args:
            title: Ticket title
            description: Ticket description

        Returns:
            Dict containing priority, category, and confidence score
        """
        # Combine title and description for analysis
        content = f"{title} {description}".lower()

        # Determine priority
        priority = self._determine_priority(content)

        # Determine category
        category = self._determine_category(content)

        # Calculate confidence score
        confidence_score = self._calculate_confidence(content, priority, category)

        return {
            "priority": priority,
            "category": category,
            "confidence_score": confidence_score
        }

    def _determine_priority(self, content: str) -> TicketPriority:
        """Determine ticket priority based on content analysis."""
        # Check for critical keywords
        for keyword in self.priority_keywords[TicketPriority.CRITICAL]:
            if keyword in content:
                return TicketPriority.CRITICAL

        # Check for high priority keywords
        for keyword in self.priority_keywords[TicketPriority.HIGH]:
            if keyword in content:
                return TicketPriority.HIGH

        # Check for low priority keywords
        for keyword in self.priority_keywords[TicketPriority.LOW]:
            if keyword in content:
                return TicketPriority.LOW

        # Default to medium priority
        return TicketPriority.MEDIUM

    def _determine_category(self, content: str) -> TicketCategory:
        """Determine ticket category based on content analysis."""
        category_scores = {}

        # Score each category based on keyword matches
        for category, keywords in self.category_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in content:
                    score += 1
            category_scores[category] = score

        # Return category with highest score, or OTHER if no matches
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            if category_scores[best_category] > 0:
                return best_category

        return TicketCategory.OTHER

    def _calculate_confidence(self, content: str, priority: TicketPriority, category: TicketCategory) -> float:
        """Calculate confidence score for the triage decision."""
        confidence = 0.5  # Base confidence

        # Increase confidence based on keyword matches
        priority_keywords = self.priority_keywords.get(priority, [])
        category_keywords = self.category_keywords.get(category, [])

        # Count keyword matches
        priority_matches = sum(1 for keyword in priority_keywords if keyword in content)
        category_matches = sum(1 for keyword in category_keywords if keyword in content)

        # Calculate confidence based on matches
        if priority_matches > 0:
            confidence += min(0.3, priority_matches * 0.1)

        if category_matches > 0:
            confidence += min(0.2, category_matches * 0.05)

        # Ensure confidence is between 0 and 1
        return min(1.0, max(0.0, confidence))

