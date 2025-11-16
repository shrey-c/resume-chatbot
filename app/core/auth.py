"""
Authentication system for admin portal.

Implements JWT-based authentication with secure password hashing.
Only the admin user (configured via environment variables) can access
the admin portal to upload resume PDFs.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from app.core.config import settings


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = settings.admin_secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# HTTP Bearer security
security = HTTPBearer()


class LoginRequest(BaseModel):
    """Login request model."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES * 60  # seconds


class TokenData(BaseModel):
    """Token payload data."""
    username: Optional[str] = None
    exp: Optional[datetime] = None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)


def authenticate_admin(username: str, password: str) -> bool:
    """
    Authenticate admin user.
    
    Credentials are stored in environment variables:
    - ADMIN_USERNAME
    - ADMIN_PASSWORD_HASH (bcrypt hash)
    
    Args:
        username: Username to authenticate
        password: Plain password to verify
        
    Returns:
        True if authentication successful, False otherwise
    """
    if username != settings.admin_username:
        return False
    
    # Verify password against hash from environment
    return verify_password(password, settings.admin_password_hash)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token.
    
    Args:
        data: Data to encode in token
        expires_delta: Token expiration time
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """
    Verify and decode JWT token.
    
    Args:
        token: JWT token to verify
        
    Returns:
        TokenData with username
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        exp: int = payload.get("exp")
        
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(
            username=username,
            exp=datetime.fromtimestamp(exp) if exp else None
        )
        
        return token_data
        
    except JWTError:
        raise credentials_exception


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> str:
    """
    Dependency to get current authenticated admin user.
    
    Used in protected routes to ensure user is authenticated.
    
    Args:
        credentials: HTTP Bearer credentials from request
        
    Returns:
        Username of authenticated admin
        
    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    token_data = verify_token(token)
    
    # Verify it's the admin user
    if token_data.username != settings.admin_username:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )
    
    return token_data.username


def login_admin(username: str, password: str) -> TokenResponse:
    """
    Login admin user and return JWT token.
    
    Args:
        username: Admin username
        password: Admin password
        
    Returns:
        TokenResponse with access token
        
    Raises:
        HTTPException: If credentials are invalid
    """
    if not authenticate_admin(username, password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return TokenResponse(access_token=access_token)


# Utility function to generate password hash for initial setup
def generate_password_hash(password: str) -> str:
    """
    Generate bcrypt hash for a password.
    
    Use this to generate the ADMIN_PASSWORD_HASH for .env file.
    
    Example:
        >>> from auth import generate_password_hash
        >>> hash = generate_password_hash("your-secure-password")
        >>> print(hash)
    
    Args:
        password: Plain password
        
    Returns:
        Bcrypt hash string
    """
    return get_password_hash(password)
