from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Ollama Configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama2"
    
    # Security Settings
    max_requests_per_minute: int = 10
    max_message_length: int = 500
    allowed_origins: List[str] = ["http://localhost:8000", "http://127.0.0.1:8000"]
    
    # Admin Authentication
    admin_username: str = "admin"
    admin_password_hash: str = ""  # Set via environment variable
    admin_secret_key: str = ""  # JWT secret key - MUST be set in production
    
    # Application Settings
    debug: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
