"""
Authentication service with JWT tokens and password hashing
"""
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from database.prisma_client import get_database
from services.rbac import rbac_service
import logging

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = "your-secret-key-change-in-production"  # Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthService:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)

    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None

    async def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with username and password"""
        try:
            db = await get_database()
            user = await db.user.find_unique(
                where={'username': username}
            )

            if not user:
                return None

            if not self.verify_password(password, user.password):
                return None

            if not user.isActive:
                return None

            # Get user context with permissions
            user_context = await rbac_service.get_user_context(user.id)
            return user_context

        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return None

    async def register_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Register a new user"""
        try:
            db = await get_database()

            # Check if user already exists
            existing_user = await db.user.find_first(
                where={
                    'OR': [
                        {'username': user_data['username']},
                        {'email': user_data['email']}
                    ]
                }
            )

            if existing_user:
                return None

            # Hash password
            hashed_password = self.get_password_hash(user_data['password'])

            # Create user
            user = await db.user.create(
                data={
                    'username': user_data['username'],
                    'email': user_data['email'],
                    'fullName': user_data['fullName'],
                    'password': hashed_password,
                    'role': user_data.get('role', 'CUSTOMER'),
                    'isActive': True
                }
            )

            # Get user context
            user_context = await rbac_service.get_user_context(user.id)
            return user_context

        except Exception as e:
            logger.error(f"Error registering user: {e}")
            return None

    async def get_current_user(self, token: str) -> Optional[Dict[str, Any]]:
        """Get current user from token"""
        try:
            payload = self.verify_token(token)
            if not payload:
                return None

            user_id = payload.get('sub')
            if not user_id:
                return None

            user_context = await rbac_service.get_user_context(user_id)
            return user_context

        except Exception as e:
            logger.error(f"Error getting current user: {e}")
            return None

    async def refresh_token(self, token: str) -> Optional[str]:
        """Refresh access token"""
        try:
            payload = self.verify_token(token)
            if not payload:
                return None

            user_id = payload.get('sub')
            if not user_id:
                return None

            # Create new token
            new_token = self.create_access_token(
                data={"sub": user_id, "type": "access"}
            )
            return new_token

        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            return None

    async def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        """Change user password"""
        try:
            db = await get_database()
            user = await db.user.find_unique(where={'id': user_id})

            if not user:
                return False

            if not self.verify_password(old_password, user.password):
                return False

            # Update password
            hashed_password = self.get_password_hash(new_password)
            await db.user.update(
                where={'id': user_id},
                data={'password': hashed_password}
            )

            return True

        except Exception as e:
            logger.error(f"Error changing password: {e}")
            return False

    async def reset_password(self, email: str) -> bool:
        """Initiate password reset"""
        try:
            db = await get_database()
            user = await db.user.find_unique(where={'email': email})

            if not user:
                return False

            # Generate reset token (in production, send email)
            reset_token = secrets.token_urlsafe(32)
            # Store reset token in database or cache
            # For now, just log it
            logger.info(f"Password reset token for {email}: {reset_token}")

            return True

        except Exception as e:
            logger.error(f"Error resetting password: {e}")
            return False

    async def update_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update user profile"""
        try:
            db = await get_database()

            # Remove password from update data
            update_data = {k: v for k, v in profile_data.items() if k != 'password'}

            user = await db.user.update(
                where={'id': user_id},
                data=update_data
            )

            # Get updated user context
            user_context = await rbac_service.get_user_context(user.id)
            return user_context

        except Exception as e:
            logger.error(f"Error updating user profile: {e}")
            return None

    async def deactivate_user(self, user_id: str) -> bool:
        """Deactivate user account"""
        try:
            db = await get_database()
            await db.user.update(
                where={'id': user_id},
                data={'isActive': False}
            )
            return True

        except Exception as e:
            logger.error(f"Error deactivating user: {e}")
            return False

    async def get_user_statistics(self, user_id: str) -> Dict[str, Any]:
        """Get user statistics"""
        try:
            db = await get_database()

            # Get ticket counts
            created_tickets = await db.ticket.count(
                where={'createdBy': user_id}
            )

            assigned_tickets = await db.ticket.count(
                where={'assignedTo': user_id}
            )

            resolved_tickets = await db.ticket.count(
                where={
                    'assignedTo': user_id,
                    'status': 'RESOLVED'
                }
            )

            # Get recent activity
            recent_tickets = await db.ticket.find_many(
                where={'createdBy': user_id},
                take=5,
                order_by={'createdAt': 'desc'}
            )

            return {
                'created_tickets': created_tickets,
                'assigned_tickets': assigned_tickets,
                'resolved_tickets': resolved_tickets,
                'recent_tickets': recent_tickets
            }

        except Exception as e:
            logger.error(f"Error getting user statistics: {e}")
            return {}

# Global auth service instance
auth_service = AuthService()


