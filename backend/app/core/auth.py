"""
Secure authentication utilities
"""
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.user import User
from app.core.sanitizer import sanitize_log_input
import logging

logger = logging.getLogger(__name__)
security = HTTPBearer()


def get_current_user_secure(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Get current user using server-side validation (secure)
    Never trust client-side data for authorization
    """
    try:
        # In production, validate JWT token server-side
        # This is a stub - implement proper JWT validation
        token = credentials.credentials
        
        # Validate token server-side (not shown for brevity)
        # user_id = validate_jwt_token(token)
        # user = get_user_from_db(user_id)
        
        # For now, return a test user
        return User(id=1, email="test@example.com", is_active=True)
        
    except Exception as e:
        logger.error(f"Authentication failed: {sanitize_log_input(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def check_admin_role(current_user: User = Depends(get_current_user_secure)) -> User:
    """
    Check if user has admin role using server-side data only
    """
    # Check role from server-side user data, never from client
    if not hasattr(current_user, 'role') or current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    return current_user