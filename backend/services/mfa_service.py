"""
Multi-Factor Authentication Service
Supports TOTP, SMS, and Email verification
"""
import pyotp
import qrcode
import secrets
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import json
import os

class MFAService:
    def __init__(self):
        self.totp_secrets = {}  # In production, store in database
        self.verification_codes = {}  # In production, use Redis or database
        self.smtp_config = {
            'host': os.getenv('SMTP_HOST', 'smtp.gmail.com'),
            'port': int(os.getenv('SMTP_PORT', 587)),
            'username': os.getenv('SMTP_USER', ''),
            'password': os.getenv('SMTP_PASSWORD', '')
        }

    def generate_totp_secret(self, user_id: str) -> str:
        """Generate a TOTP secret for a user"""
        secret = pyotp.random_base32()
        self.totp_secrets[user_id] = secret
        return secret

    def generate_totp_qr_code(self, user_id: str, user_email: str, app_name: str = "IT Support Pro") -> str:
        """Generate QR code for TOTP setup"""
        if user_id not in self.totp_secrets:
            self.generate_totp_secret(user_id)

        secret = self.totp_secrets[user_id]
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user_email,
            issuer_name=app_name
        )

        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)

        # Create QR code image
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Save QR code
        qr_path = f"temp_qr_{user_id}.png"
        qr_img.save(qr_path)

        return qr_path

    def verify_totp(self, user_id: str, token: str) -> bool:
        """Verify TOTP token"""
        if user_id not in self.totp_secrets:
            return False

        secret = self.totp_secrets[user_id]
        totp = pyotp.TOTP(secret)

        # Allow 30-second window for clock drift
        return totp.verify(token, valid_window=1)

    def generate_verification_code(self, user_id: str, method: str = "email") -> str:
        """Generate a 6-digit verification code"""
        code = str(secrets.randbelow(900000) + 100000)  # 6-digit code

        self.verification_codes[user_id] = {
            'code': code,
            'method': method,
            'timestamp': time.time(),
            'attempts': 0,
            'verified': False
        }

        return code

    def send_email_verification(self, user_email: str, code: str) -> bool:
        """Send verification code via email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_config['username']
            msg['To'] = user_email
            msg['Subject'] = "IT Support Pro - Verification Code"

            body = f"""
            <html>
            <body>
                <h2>Your Verification Code</h2>
                <p>Your verification code is: <strong style="font-size: 24px; color: #2563eb;">{code}</strong></p>
                <p>This code will expire in 10 minutes.</p>
                <p>If you didn't request this code, please ignore this email.</p>
                <br>
                <p>Best regards,<br>IT Support Pro Team</p>
            </body>
            </html>
            """

            msg.attach(MIMEText(body, 'html'))

            server = smtplib.SMTP(self.smtp_config['host'], self.smtp_config['port'])
            server.starttls()
            server.login(self.smtp_config['username'], self.smtp_config['password'])
            server.send_message(msg)
            server.quit()

            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def send_sms_verification(self, phone_number: str, code: str) -> bool:
        """Send verification code via SMS (mock implementation)"""
        # In production, integrate with SMS service like Twilio
        print(f"SMS to {phone_number}: Your verification code is {code}")
        return True

    def verify_code(self, user_id: str, code: str) -> Dict[str, Any]:
        """Verify the provided code"""
        if user_id not in self.verification_codes:
            return {'success': False, 'message': 'No verification code found'}

        verification_data = self.verification_codes[user_id]

        # Check if code has expired (10 minutes)
        if time.time() - verification_data['timestamp'] > 600:
            del self.verification_codes[user_id]
            return {'success': False, 'message': 'Verification code expired'}

        # Check attempts (max 3)
        if verification_data['attempts'] >= 3:
            del self.verification_codes[user_id]
            return {'success': False, 'message': 'Too many failed attempts'}

        # Verify code
        if verification_data['code'] == code:
            verification_data['verified'] = True
            verification_data['verified_at'] = time.time()
            return {'success': True, 'message': 'Code verified successfully'}
        else:
            verification_data['attempts'] += 1
            remaining_attempts = 3 - verification_data['attempts']
            return {
                'success': False,
                'message': f'Invalid code. {remaining_attempts} attempts remaining'
            }

    def is_verified(self, user_id: str) -> bool:
        """Check if user's verification is complete"""
        if user_id not in self.verification_codes:
            return False

        return self.verification_codes[user_id].get('verified', False)

    def cleanup_expired_codes(self):
        """Clean up expired verification codes"""
        current_time = time.time()
        expired_users = []

        for user_id, data in self.verification_codes.items():
            if current_time - data['timestamp'] > 600:  # 10 minutes
                expired_users.append(user_id)

        for user_id in expired_users:
            del self.verification_codes[user_id]

    def get_mfa_status(self, user_id: str) -> Dict[str, Any]:
        """Get MFA status for a user"""
        totp_enabled = user_id in self.totp_secrets
        email_verified = self.is_verified(user_id)

        return {
            'totp_enabled': totp_enabled,
            'email_verified': email_verified,
            'mfa_required': totp_enabled or email_verified,
            'methods': {
                'totp': totp_enabled,
                'email': email_verified
            }
        }

    def disable_mfa(self, user_id: str):
        """Disable MFA for a user"""
        if user_id in self.totp_secrets:
            del self.totp_secrets[user_id]
        if user_id in self.verification_codes:
            del self.verification_codes[user_id]

# Global MFA service instance
mfa_service = MFAService()


