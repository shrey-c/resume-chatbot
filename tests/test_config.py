"""Tests for configuration module."""
import pytest
from app.core.config import Settings, settings


class TestSettings:
    """Tests for Settings configuration."""
    
    def test_settings_defaults(self):
        """Test default settings values."""
        assert settings.ollama_base_url == "http://localhost:11434"
        assert settings.max_requests_per_minute == 10
        assert settings.max_message_length == 500
        assert settings.admin_username == "admin"
    
    def test_settings_ollama_model(self):
        """Test Ollama model configuration."""
        assert settings.ollama_model is not None
        assert isinstance(settings.ollama_model, str)
    
    def test_settings_allowed_origins(self):
        """Test CORS allowed origins."""
        assert isinstance(settings.allowed_origins, list)
        assert len(settings.allowed_origins) >= 2
        assert "http://localhost:8000" in settings.allowed_origins
    
    def test_settings_security_keys(self):
        """Test security-related settings exist."""
        assert settings.admin_password_hash is not None
        assert settings.admin_secret_key is not None
    
    def test_settings_debug_mode(self):
        """Test debug mode setting."""
        assert isinstance(settings.debug, bool)
    
    def test_settings_rate_limiting(self):
        """Test rate limiting configuration."""
        assert settings.max_requests_per_minute > 0
        assert settings.max_requests_per_minute <= 100
    
    def test_settings_message_length(self):
        """Test message length limit."""
        assert settings.max_message_length == 500
        assert settings.max_message_length > 0
