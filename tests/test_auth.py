"""Tests for authentication module."""
import pytest
from datetime import datetime, timedelta
from jose import jwt
from app.core.auth import (
    verify_password,
    get_password_hash,
    authenticate_admin,
    create_access_token,
    verify_token,
    login_admin,
    generate_password_hash,
    TokenData,
    SECRET_KEY,
    ALGORITHM
)
from app.core.config import settings
from fastapi import HTTPException


class TestPasswordHashing:
    """Tests for password hashing functions."""
    
    def test_get_password_hash(self):
        """Test password hash generation."""
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 50  # Bcrypt hashes are long
    
    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "test_password_123"
        wrong_password = "wrong_password"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_generate_password_hash(self):
        """Test public password hash generation function."""
        password = "my_secure_password"
        hashed = generate_password_hash(password)
        
        assert hashed is not None
        assert verify_password(password, hashed) is True


class TestAuthentication:
    """Tests for authentication functions."""
    
    def test_authenticate_admin_success(self):
        """Test successful admin authentication."""
        # Use the actual credentials from settings
        result = authenticate_admin(settings.admin_username, "Shreyansh@2025")
        assert result is True
    
    def test_authenticate_admin_wrong_username(self):
        """Test authentication fails with wrong username."""
        result = authenticate_admin("wrong_user", "Shreyansh@2025")
        assert result is False
    
    def test_authenticate_admin_wrong_password(self):
        """Test authentication fails with wrong password."""
        result = authenticate_admin(settings.admin_username, "wrong_password")
        assert result is False


class TestJWTTokens:
    """Tests for JWT token operations."""
    
    def test_create_access_token(self):
        """Test JWT token creation."""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 50
    
    def test_create_access_token_with_expiry(self):
        """Test JWT token creation with custom expiry."""
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=30)
        token = create_access_token(data, expires_delta)
        
        # Just verify the token is valid and contains expected data
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == "testuser"
        assert "exp" in payload
    
    def test_verify_token_valid(self):
        """Test verification of valid token."""
        data = {"sub": "admin"}
        token = create_access_token(data)
        
        token_data = verify_token(token)
        
        assert token_data.username == "admin"
        assert token_data.exp is not None
    
    def test_verify_token_invalid(self):
        """Test verification of invalid token."""
        invalid_token = "invalid.token.here"
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(invalid_token)
        
        assert exc_info.value.status_code == 401
        assert "Could not validate credentials" in exc_info.value.detail
    
    def test_verify_token_expired(self):
        """Test verification of expired token."""
        data = {"sub": "admin"}
        # Create token that expired 1 hour ago
        expires_delta = timedelta(hours=-1)
        token = create_access_token(data, expires_delta)
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(token)
        
        assert exc_info.value.status_code == 401


class TestLoginFlow:
    """Tests for complete login flow."""
    
    def test_login_admin_success(self):
        """Test successful admin login."""
        response = login_admin(settings.admin_username, "Shreyansh@2025")
        
        assert response.access_token is not None
        assert response.token_type == "bearer"
        assert response.expires_in == 3600  # 60 minutes
    
    def test_login_admin_wrong_credentials(self):
        """Test login fails with wrong credentials."""
        with pytest.raises(HTTPException) as exc_info:
            login_admin("wrong_user", "wrong_pass")
        
        assert exc_info.value.status_code == 401
        assert "Incorrect username or password" in exc_info.value.detail
    
    def test_login_admin_wrong_password(self):
        """Test login fails with wrong password."""
        with pytest.raises(HTTPException) as exc_info:
            login_admin(settings.admin_username, "wrong_password")
        
        assert exc_info.value.status_code == 401


class TestTokenData:
    """Tests for TokenData model."""
    
    def test_token_data_creation(self):
        """Test TokenData model creation."""
        exp_time = datetime.utcnow() + timedelta(hours=1)
        token_data = TokenData(username="admin", exp=exp_time)
        
        assert token_data.username == "admin"
        assert token_data.exp == exp_time
    
    def test_token_data_optional_fields(self):
        """Test TokenData with optional fields."""
        token_data = TokenData()
        
        assert token_data.username is None
        assert token_data.exp is None
