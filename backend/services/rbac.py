"""
Role-Based Access Control (RBAC) service
"""
from enum import Enum
from typing import List, Dict, Optional
from database.prisma_client import get_database
import logging

logger = logging.getLogger(__name__)

class Permission(Enum):
    # User management
    CREATE_USER = "create_user"
    READ_USER = "read_user"
    UPDATE_USER = "update_user"
    DELETE_USER = "delete_user"

    # Ticket management
    CREATE_TICKET = "create_ticket"
    READ_TICKET = "read_ticket"
    UPDATE_TICKET = "update_ticket"
    DELETE_TICKET = "delete_ticket"
    ASSIGN_TICKET = "assign_ticket"
    ESCALATE_TICKET = "escalate_ticket"

    # System monitoring
    VIEW_METRICS = "view_metrics"
    VIEW_LOGS = "view_logs"
    VIEW_ALERTS = "view_alerts"
    MANAGE_ALERTS = "manage_alerts"

    # Chatbot
    USE_CHATBOT = "use_chatbot"
    MANAGE_FAQ = "manage_faq"
    VIEW_CHATBOT_ANALYTICS = "view_chatbot_analytics"

    # System administration
    MANAGE_SYSTEM = "manage_system"
    VIEW_ANALYTICS = "view_analytics"
    MANAGE_CONFIGURATION = "manage_configuration"

class RBACService:
    def __init__(self):
        self.role_permissions = {
            'ADMIN': [
                # All permissions
                Permission.CREATE_USER,
                Permission.READ_USER,
                Permission.UPDATE_USER,
                Permission.DELETE_USER,
                Permission.CREATE_TICKET,
                Permission.READ_TICKET,
                Permission.UPDATE_TICKET,
                Permission.DELETE_TICKET,
                Permission.ASSIGN_TICKET,
                Permission.ESCALATE_TICKET,
                Permission.VIEW_METRICS,
                Permission.VIEW_LOGS,
                Permission.VIEW_ALERTS,
                Permission.MANAGE_ALERTS,
                Permission.USE_CHATBOT,
                Permission.MANAGE_FAQ,
                Permission.VIEW_CHATBOT_ANALYTICS,
                Permission.MANAGE_SYSTEM,
                Permission.VIEW_ANALYTICS,
                Permission.MANAGE_CONFIGURATION,
            ],
            'AGENT': [
                # Ticket management
                Permission.CREATE_TICKET,
                Permission.READ_TICKET,
                Permission.UPDATE_TICKET,
                Permission.ASSIGN_TICKET,
                Permission.ESCALATE_TICKET,
                # Monitoring
                Permission.VIEW_METRICS,
                Permission.VIEW_LOGS,
                Permission.VIEW_ALERTS,
                Permission.MANAGE_ALERTS,
                # Chatbot
                Permission.USE_CHATBOT,
                Permission.MANAGE_FAQ,
                Permission.VIEW_CHATBOT_ANALYTICS,
                # Analytics
                Permission.VIEW_ANALYTICS,
            ],
            'CUSTOMER': [
                # Basic ticket operations
                Permission.CREATE_TICKET,
                Permission.READ_TICKET,
                # Chatbot
                Permission.USE_CHATBOT,
            ]
        }

    def has_permission(self, user_role: str, permission: Permission) -> bool:
        """Check if user role has specific permission"""
        if user_role not in self.role_permissions:
            return False

        return permission in self.role_permissions[user_role]

    def get_user_permissions(self, user_role: str) -> List[Permission]:
        """Get all permissions for a user role"""
        return self.role_permissions.get(user_role, [])

    def can_access_ticket(self, user_role: str, user_id: str, ticket_creator: str, ticket_assignee: Optional[str] = None) -> bool:
        """Check if user can access a specific ticket"""
        if user_role == 'ADMIN':
            return True

        if user_role == 'AGENT':
            return True  # Agents can see all tickets

        if user_role == 'CUSTOMER':
            return user_id == ticket_creator or user_id == ticket_assignee

        return False

    def can_modify_ticket(self, user_role: str, user_id: str, ticket_creator: str, ticket_assignee: Optional[str] = None) -> bool:
        """Check if user can modify a specific ticket"""
        if user_role == 'ADMIN':
            return True

        if user_role == 'AGENT':
            return True  # Agents can modify all tickets

        if user_role == 'CUSTOMER':
            return user_id == ticket_creator  # Customers can only modify their own tickets

        return False

    def can_access_dashboard_section(self, user_role: str, section: str) -> bool:
        """Check if user can access specific dashboard section"""
        section_permissions = {
            'operations': [Permission.VIEW_METRICS, Permission.VIEW_LOGS, Permission.VIEW_ALERTS],
            'tickets': [Permission.READ_TICKET],
            'chatbot': [Permission.USE_CHATBOT],
            'analytics': [Permission.VIEW_ANALYTICS],
            'users': [Permission.READ_USER],
            'system': [Permission.MANAGE_SYSTEM]
        }

        required_permissions = section_permissions.get(section, [])
        if not required_permissions:
            return False

        return all(self.has_permission(user_role, perm) for perm in required_permissions)

    def get_accessible_dashboard_sections(self, user_role: str) -> List[str]:
        """Get list of dashboard sections user can access"""
        sections = ['operations', 'tickets', 'chatbot', 'analytics', 'users', 'system']
        return [section for section in sections if self.can_access_dashboard_section(user_role, section)]

    def filter_tickets_by_access(self, user_role: str, user_id: str, tickets: List[Dict]) -> List[Dict]:
        """Filter tickets based on user access rights"""
        if user_role == 'ADMIN' or user_role == 'AGENT':
            return tickets  # Admins and agents can see all tickets

        if user_role == 'CUSTOMER':
            return [
                ticket for ticket in tickets
                if ticket.get('createdBy') == user_id or ticket.get('assignedTo') == user_id
            ]

        return []

    def get_role_hierarchy(self) -> Dict[str, int]:
        """Get role hierarchy (higher number = more privileges)"""
        return {
            'CUSTOMER': 1,
            'AGENT': 2,
            'ADMIN': 3
        }

    def can_escalate_ticket(self, user_role: str) -> bool:
        """Check if user can escalate tickets"""
        return self.has_permission(user_role, Permission.ESCALATE_TICKET)

    def can_assign_ticket(self, user_role: str) -> bool:
        """Check if user can assign tickets"""
        return self.has_permission(user_role, Permission.ASSIGN_TICKET)

    def can_manage_users(self, user_role: str) -> bool:
        """Check if user can manage other users"""
        return self.has_permission(user_role, Permission.CREATE_USER)

    def can_view_system_metrics(self, user_role: str) -> bool:
        """Check if user can view system metrics"""
        return self.has_permission(user_role, Permission.VIEW_METRICS)

    def can_manage_system(self, user_role: str) -> bool:
        """Check if user can manage system settings"""
        return self.has_permission(user_role, Permission.MANAGE_SYSTEM)

    async def get_user_context(self, user_id: str) -> Dict:
        """Get user context with role and permissions"""
        try:
            db = await get_database()
            user = await db.user.find_unique(
                where={'id': user_id},
                include={
                    'tickets': True,
                    'assignedTickets': True
                }
            )

            if not user:
                return None

            permissions = self.get_user_permissions(user.role)
            accessible_sections = self.get_accessible_dashboard_sections(user.role)

            return {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'fullName': user.fullName,
                'role': user.role,
                'isActive': user.isActive,
                'permissions': [p.value for p in permissions],
                'accessible_sections': accessible_sections,
                'ticket_count': len(user.tickets),
                'assigned_ticket_count': len(user.assignedTickets)
            }

        except Exception as e:
            logger.error(f"Error getting user context: {e}")
            return None

# Global RBAC service instance
rbac_service = RBACService()




