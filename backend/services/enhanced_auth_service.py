"""
Enhanced Authentication Service with MFA and E2E Encryption
"""
import jwt
import time
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from services.encryption_service import encryption_service, SENSITIVE_FIELDS
from services.mfa_service import mfa_service
import os

class EnhancedAuthService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = os.getenv("JWT_SECRET", "your-super-secret-jwt-key")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.refresh_token_expire_days = 7

    def hash_password(self, password: str) -> str:
        """Hash password with bcrypt"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)

        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_refresh_token(self, data: dict) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.JWTError:
            return None

    def encrypt_user_data(self, user_data: dict) -> dict:
        """Encrypt sensitive user data"""
        return encryption_service.encrypt_sensitive_fields(user_data, SENSITIVE_FIELDS)

    def decrypt_user_data(self, user_data: dict) -> dict:
        """Decrypt sensitive user data"""
        return encryption_service.decrypt_sensitive_fields(user_data, SENSITIVE_FIELDS)

    def register_user(self, user_data: dict) -> Dict[str, Any]:
        """Register new user with encryption"""
        # Hash password
        hashed_password = self.hash_password(user_data['password'])
        user_data['password'] = hashed_password

        # Encrypt sensitive data
        encrypted_user_data = self.encrypt_user_data(user_data)

        # Generate user ID
        user_id = f"user_{int(time.time())}_{secrets.token_hex(8)}"
        encrypted_user_data['user_id'] = user_id
        encrypted_user_data['created_at'] = datetime.utcnow().isoformat()
        encrypted_user_data['mfa_enabled'] = False

        return {
            'success': True,
            'user_id': user_id,
            'user_data': encrypted_user_data,
            'message': 'User registered successfully'
        }

    def authenticate_user(self, username: str, password: str, mfa_code: Optional[str] = None) -> Dict[str, Any]:
        """Authenticate user with optional MFA"""
        # In production, fetch from database
        # For demo, using mock data
        mock_users = {
            'admin': {
                'user_id': 'admin_001',
                'username': 'admin',
                'password': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.5K2O',  # admin123
                'email': 'admin@itsupport.com',
                'role': 'admin',
                'mfa_enabled': True
            },
            'agent': {
                'user_id': 'agent_001',
                'username': 'agent',
                'password': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.5K2O',  # agent123
                'email': 'agent@itsupport.com',
                'role': 'agent',
                'mfa_enabled': True
            },
            'customer': {
                'user_id': 'customer_001',
                'username': 'customer',
                'password': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.5K2O',  # customer123
                'email': 'customer@itsupport.com',
                'role': 'customer',
                'mfa_enabled': False
            }
        }

        if username not in mock_users:
            return {'success': False, 'message': 'Invalid credentials'}

        user = mock_users[username]

        # Verify password
        if not self.verify_password(password, user['password']):
            return {'success': False, 'message': 'Invalid credentials'}

        # Check MFA if enabled
        if user.get('mfa_enabled', False):
            if not mfa_code:
                return {
                    'success': False,
                    'message': 'MFA required',
                    'mfa_required': True,
                    'user_id': user['user_id']
                }

            # Verify MFA code
            if not mfa_service.verify_totp(user['user_id'], mfa_code):
                return {'success': False, 'message': 'Invalid MFA code'}

        # Create tokens
        token_data = {
            'user_id': user['user_id'],
            'username': user['username'],
            'role': user['role'],
            'mfa_verified': True
        }

        access_token = self.create_access_token(token_data)
        refresh_token = self.create_refresh_token(token_data)

        return {
            'success': True,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'user_id': user['user_id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role'],
                'mfa_enabled': user['mfa_enabled']
            }
        }

    def setup_mfa(self, user_id: str, user_email: str) -> Dict[str, Any]:
        """Setup MFA for user"""
        # Generate TOTP secret
        secret = mfa_service.generate_totp_secret(user_id)

        # Generate QR code
        qr_path = mfa_service.generate_totp_qr_code(user_id, user_email)

        return {
            'success': True,
            'secret': secret,
            'qr_code_path': qr_path,
            'message': 'MFA setup initiated. Scan QR code with authenticator app.'
        }

    def verify_mfa_setup(self, user_id: str, token: str) -> Dict[str, Any]:
        """Verify MFA setup with token"""
        if mfa_service.verify_totp(user_id, token):
            return {
                'success': True,
                'message': 'MFA setup completed successfully'
            }
        else:
            return {
                'success': False,
                'message': 'Invalid token. Please try again.'
            }

    def send_verification_email(self, user_id: str, user_email: str) -> Dict[str, Any]:
        """Send verification email"""
        code = mfa_service.generate_verification_code(user_id, 'email')

        if mfa_service.send_email_verification(user_email, code):
            return {
                'success': True,
                'message': 'Verification email sent'
            }
        else:
            return {
                'success': False,
                'message': 'Failed to send verification email'
            }

    def verify_email_code(self, user_id: str, code: str) -> Dict[str, Any]:
        """Verify email verification code"""
        result = mfa_service.verify_code(user_id, code)
        return result

    def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token using refresh token"""
        payload = self.verify_token(refresh_token)

        if not payload or payload.get('type') != 'refresh':
            return {'success': False, 'message': 'Invalid refresh token'}

        # Create new access token
        token_data = {
            'user_id': payload['user_id'],
            'username': payload['username'],
            'role': payload['role'],
            'mfa_verified': True
        }

        access_token = self.create_access_token(token_data)

        return {
            'success': True,
            'access_token': access_token
        }

    def get_user_mfa_status(self, user_id: str) -> Dict[str, Any]:
        """Get user's MFA status"""
        return mfa_service.get_mfa_status(user_id)

# Global enhanced auth service instance
enhanced_auth_service = EnhancedAuthService()
