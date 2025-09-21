"""
Auto-triage service for incident management and SLA tracking
"""
import re
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database.prisma_client import get_database
import logging

logger = logging.getLogger(__name__)

class AutoTriageService:
    def __init__(self):
        self.priority_keywords = {
            'CRITICAL': [
                'down', 'outage', 'critical', 'urgent', 'emergency', 'fatal',
                'system down', 'service unavailable', 'complete failure',
                'security breach', 'data loss', 'cannot access'
            ],
            'HIGH': [
                'slow', 'performance', 'timeout', 'error', 'failed',
                'not working', 'broken', 'issue', 'problem', 'bug',
                'login failed', 'access denied', 'connection error'
            ],
            'MEDIUM': [
                'question', 'help', 'how to', 'tutorial', 'guide',
                'feature request', 'enhancement', 'improvement',
                'configuration', 'setup', 'installation'
            ],
            'LOW': [
                'information', 'general', 'inquiry', 'question',
                'documentation', 'training', 'best practice'
            ]
        }

        self.category_keywords = {
            'Network': ['network', 'connection', 'internet', 'wifi', 'vpn', 'dns', 'ip'],
            'Hardware': ['computer', 'laptop', 'desktop', 'printer', 'scanner', 'hardware'],
            'Software': ['software', 'application', 'program', 'install', 'update', 'license'],
            'Email': ['email', 'outlook', 'mail', 'smtp', 'imap', 'exchange'],
            'Security': ['password', 'login', 'authentication', 'security', 'access', 'permission'],
            'Account': ['account', 'user', 'profile', 'registration', 'signup', 'login'],
            'Database': ['database', 'db', 'sql', 'query', 'data', 'backup'],
            'General': []  # Default category
        }

        self.sla_times = {
            'CRITICAL': 1,  # 1 hour
            'HIGH': 4,      # 4 hours
            'MEDIUM': 24,   # 24 hours
            'LOW': 72       # 72 hours
        }

    async def triage_ticket(self, ticket_data: Dict) -> Dict:
        """Auto-triage a new ticket"""
        try:
            title = ticket_data.get('title', '').lower()
            description = ticket_data.get('description', '').lower()
            content = f"{title} {description}"

            # Determine priority
            priority = await self._determine_priority(content)

            # Determine category
            category = await self._determine_category(content)

            # Calculate SLA deadline
            sla_deadline = datetime.now() + timedelta(hours=self.sla_times[priority])

            # Determine if escalation is needed
            escalation_level = await self._determine_escalation(content, priority)

            # Auto-assign if possible
            assigned_to = await self._auto_assign(priority, category)

            return {
                'priority': priority,
                'category': category,
                'sla_deadline': sla_deadline,
                'escalation_level': escalation_level,
                'assigned_to': assigned_to,
                'auto_triaged': True
            }

        except Exception as e:
            logger.error(f"Error in auto-triage: {e}")
            return {
                'priority': 'MEDIUM',
                'category': 'General',
                'sla_deadline': datetime.now() + timedelta(hours=24),
                'escalation_level': 0,
                'assigned_to': None,
                'auto_triaged': False
            }

    async def _determine_priority(self, content: str) -> str:
        """Determine ticket priority based on content"""
        content_lower = content.lower()

        # Check for critical keywords
        for keyword in self.priority_keywords['CRITICAL']:
            if keyword in content_lower:
                return 'CRITICAL'

        # Check for high priority keywords
        for keyword in self.priority_keywords['HIGH']:
            if keyword in content_lower:
                return 'HIGH'

        # Check for medium priority keywords
        for keyword in self.priority_keywords['MEDIUM']:
            if keyword in content_lower:
                return 'MEDIUM'

        # Default to low priority
        return 'LOW'

    async def _determine_category(self, content: str) -> str:
        """Determine ticket category based on content"""
        content_lower = content.lower()

        # Check each category
        for category, keywords in self.category_keywords.items():
            if category == 'General':
                continue
            for keyword in keywords:
                if keyword in content_lower:
                    return category

        return 'General'

    async def _determine_escalation(self, content: str, priority: str) -> int:
        """Determine escalation level"""
        escalation_keywords = [
            'escalate', 'manager', 'supervisor', 'urgent', 'immediate',
            'asap', 'right now', 'cannot wait'
        ]

        content_lower = content.lower()
        for keyword in escalation_keywords:
            if keyword in content_lower:
                return 1

        # High priority tickets get higher escalation
        if priority == 'CRITICAL':
            return 1
        elif priority == 'HIGH':
            return 0

        return 0

    async def _auto_assign(self, priority: str, category: str) -> Optional[str]:
        """Auto-assign ticket to available agent"""
        try:
            db = await get_database()

            # Find available agents (users with AGENT role)
            agents = await db.user.find_many(
                where={
                    'role': 'AGENT',
                    'isActive': True
                }
            )

            if not agents:
                return None

            # Simple round-robin assignment based on current workload
            # In a real system, you'd have more sophisticated logic
            for agent in agents:
                # Check current ticket count for this agent
                current_tickets = await db.ticket.count(
                    where={
                        'assignedTo': agent.id,
                        'status': {
                            'in': ['OPEN', 'IN_PROGRESS']
                        }
                    }
                )

                # Assign to agent with least tickets
                if current_tickets < 5:  # Max 5 tickets per agent
                    return agent.id

            return None

        except Exception as e:
            logger.error(f"Error in auto-assignment: {e}")
            return None

    async def check_sla_violations(self):
        """Check for SLA violations and escalate if needed"""
        try:
            db = await get_database()
            now = datetime.now()

            # Find tickets approaching or past SLA deadline
            violating_tickets = await db.ticket.find_many(
                where={
                    'status': {
                        'in': ['OPEN', 'IN_PROGRESS']
                    },
                    'slaDeadline': {
                        'lte': now
                    }
                }
            )

            for ticket in violating_tickets:
                await self._handle_sla_violation(ticket)

        except Exception as e:
            logger.error(f"Error checking SLA violations: {e}")

    async def _handle_sla_violation(self, ticket):
        """Handle SLA violation by escalating ticket"""
        try:
            db = await get_database()

            # Escalate the ticket
            new_escalation_level = ticket.escalationLevel + 1

            await db.ticket.update(
                where={'id': ticket.id},
                data={
                    'escalationLevel': new_escalation_level,
                    'priority': 'CRITICAL' if ticket.priority != 'CRITICAL' else ticket.priority
                }
            )

            # Create SLA event
            await db.slaevent.create(data={
                'ticketId': ticket.id,
                'eventType': 'escalated',
                'metadata': f'{"SLA violation - escalated to level " + str(new_escalation_level)}'
            })

            # Create alert
            await db.alert.create(data={
                'title': f"SLA Violation - Ticket #{ticket.id}",
                'message': f"Ticket '{ticket.title}' has violated SLA and been escalated",
                'severity': 'HIGH',
                'source': 'sla',
                'ticketId': ticket.id
            })

            logger.warning(f"SLA violation handled for ticket {ticket.id}")

        except Exception as e:
            logger.error(f"Error handling SLA violation: {e}")

    async def get_sla_metrics(self) -> Dict:
        """Get SLA performance metrics"""
        try:
            db = await get_database()
            now = datetime.now()
            last_30_days = now - timedelta(days=30)

            # Get all tickets from last 30 days
            tickets = await db.ticket.find_many(
                where={
                    'createdAt': {
                        'gte': last_30_days
                    }
                }
            )

            total_tickets = len(tickets)
            sla_violations = 0
            avg_resolution_time = 0

            resolved_tickets = [t for t in tickets if t.resolvedAt]

            if resolved_tickets:
                resolution_times = []
                for ticket in resolved_tickets:
                    if ticket.slaDeadline and ticket.resolvedAt:
                        if ticket.resolvedAt > ticket.slaDeadline:
                            sla_violations += 1

                        resolution_time = (ticket.resolvedAt - ticket.createdAt).total_seconds() / 3600
                        resolution_times.append(resolution_time)

                if resolution_times:
                    avg_resolution_time = sum(resolution_times) / len(resolution_times)

            sla_compliance = ((total_tickets - sla_violations) / total_tickets * 100) if total_tickets > 0 else 100

            return {
                'total_tickets': total_tickets,
                'sla_violations': sla_violations,
                'sla_compliance': round(sla_compliance, 2),
                'avg_resolution_time_hours': round(avg_resolution_time, 2)
            }

        except Exception as e:
            logger.error(f"Error getting SLA metrics: {e}")
            return {}

    async def start_sla_monitoring(self):
        """Start SLA monitoring task"""
        while True:
            try:
                await self.check_sla_violations()
                await asyncio.sleep(300)  # Check every 5 minutes
            except Exception as e:
                logger.error(f"Error in SLA monitoring: {e}")
                await asyncio.sleep(600)  # Wait longer on error

# Global auto-triage service instance
auto_triage_service = AutoTriageService()




