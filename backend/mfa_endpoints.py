"""
Multi-Factor Authentication API Endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
import tempfile

router = APIRouter(prefix="/api/mfa", tags=["MFA"])

# Pydantic models
class MFASetupRequest(BaseModel):
    user_id: str
    user_email: str

class MFAVerifyRequest(BaseModel):
    user_id: str
    token: str

class EmailVerificationRequest(BaseModel):
    user_id: str
    user_email: str

class EmailCodeVerifyRequest(BaseModel):
    user_id: str
    code: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

# Import services
from services.enhanced_auth_service import enhanced_auth_service
from services.mfa_service import mfa_service

@router.post("/setup")
async def setup_mfa(request: MFASetupRequest):
    """Setup MFA for user"""
    try:
        result = enhanced_auth_service.setup_mfa(request.user_id, request.user_email)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to setup MFA: {str(e)}"
        )

@router.get("/qr-code/{user_id}")
async def get_qr_code(user_id: str):
    """Get QR code for MFA setup"""
    try:
        # In production, store QR codes in a secure location
        qr_path = f"temp_qr_{user_id}.png"

        if os.path.exists(qr_path):
            return FileResponse(qr_path, media_type="image/png")
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="QR code not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get QR code: {str(e)}"
        )

@router.post("/verify-setup")
async def verify_mfa_setup(request: MFAVerifyRequest):
    """Verify MFA setup with token"""
    try:
        result = enhanced_auth_service.verify_mfa_setup(request.user_id, request.token)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify MFA setup: {str(e)}"
        )

@router.post("/send-email-verification")
async def send_email_verification(request: EmailVerificationRequest):
    """Send verification email"""
    try:
        result = enhanced_auth_service.send_verification_email(request.user_id, request.user_email)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send verification email: {str(e)}"
        )

@router.post("/verify-email-code")
async def verify_email_code(request: EmailCodeVerifyRequest):
    """Verify email verification code"""
    try:
        result = enhanced_auth_service.verify_email_code(request.user_id, request.code)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify email code: {str(e)}"
        )

@router.get("/status/{user_id}")
async def get_mfa_status(user_id: str):
    """Get user's MFA status"""
    try:
        result = enhanced_auth_service.get_user_mfa_status(user_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get MFA status: {str(e)}"
        )

@router.post("/refresh-token")
async def refresh_token(request: RefreshTokenRequest):
    """Refresh access token"""
    try:
        result = enhanced_auth_service.refresh_access_token(request.refresh_token)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to refresh token: {str(e)}"
        )

@router.post("/disable/{user_id}")
async def disable_mfa(user_id: str):
    """Disable MFA for user"""
    try:
        mfa_service.disable_mfa(user_id)
        return {
            'success': True,
            'message': 'MFA disabled successfully'
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to disable MFA: {str(e)}"
        )


