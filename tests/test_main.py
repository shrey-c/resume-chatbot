"""Integration tests for main.py endpoints."""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from fastapi.testclient import TestClient
from main import app
from app.models import Resume, ContactInfo


client = TestClient(app)


class TestMainEndpoints:
    """Tests for main.py endpoint handlers."""
    
    def test_root_endpoint(self):
        """Test root endpoint serves HTML."""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_admin_page_endpoint(self):
        """Test admin page endpoint."""
        response = client.get("/admin")
        assert response.status_code == 200
    
    def test_health_endpoint_structure(self):
        """Test health endpoint returns correct structure."""
        with patch('main.agentic_chatbot') as mock_chatbot:
            mock_chatbot.check_health = AsyncMock(return_value=True)
            
            response = client.get("/api/health")
            
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
            assert "ollama_available" in data
            assert "ollama_model" in data
            assert "agentic_system" in data
    
    def test_resume_endpoint_success(self):
        """Test resume endpoint returns valid data."""
        response = client.get("/api/resume")
        
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "contact" in data
        assert "experience" in data
        assert "skills" in data
    
    def test_admin_login_endpoint(self):
        """Test admin login endpoint."""
        response = client.post(
            "/api/admin/login",
            json={"username": "admin", "password": "Shreyansh@2025"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
    
    def test_admin_login_invalid_credentials(self):
        """Test admin login with invalid credentials."""
        response = client.post(
            "/api/admin/login",
            json={"username": "wrong", "password": "wrong"}
        )
        
        assert response.status_code == 401
    
    def test_admin_verify_with_valid_token(self):
        """Test admin verify endpoint with valid token."""
        # First get a valid token
        login_response = client.post(
            "/api/admin/login",
            json={"username": "admin", "password": "Shreyansh@2025"}
        )
        token = login_response.json()["access_token"]
        
        # Use token to verify
        response = client.get(
            "/api/admin/verify",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["authenticated"] is True
        assert data["username"] == "admin"
    
    def test_admin_verify_without_token(self):
        """Test admin verify endpoint without token."""
        response = client.get("/api/admin/verify")
        
        # FastAPI returns 403 when no credentials provided
        assert response.status_code in [401, 403]
    
    def test_admin_verify_with_invalid_token(self):
        """Test admin verify endpoint with invalid token."""
        response = client.get(
            "/api/admin/verify",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == 401


class TestChatEndpointIntegration:
    """Integration tests for chat endpoint."""
    
    def test_chat_with_valid_message(self):
        """Test chat endpoint with valid message."""
        with patch('main.agentic_chatbot') as mock_chatbot:
            mock_chatbot.check_health = AsyncMock(return_value=True)
            mock_chatbot.chat = AsyncMock(return_value="Test response from AI")
            
            response = client.post(
                "/api/chat",
                json={"message": "What are your skills?"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert len(data["response"]) > 0
    
    def test_chat_when_ollama_unavailable(self):
        """Test chat endpoint when Ollama is unavailable."""
        with patch('main.agentic_chatbot') as mock_chatbot:
            mock_chatbot.check_health = AsyncMock(return_value=False)
            
            response = client.post(
                "/api/chat",
                json={"message": "Test message"}
            )
            
            assert response.status_code == 503


class TestAdminUploadEndpoint:
    """Tests for admin upload endpoint."""
    
    def test_upload_without_auth(self):
        """Test upload endpoint requires authentication."""
        response = client.post(
            "/api/admin/upload-resume",
            files={"file": ("test.pdf", b"fake pdf content", "application/pdf")}
        )
        
        # FastAPI returns 403 when no credentials provided
        assert response.status_code in [401, 403]
    
    def test_upload_non_pdf_file(self):
        """Test upload endpoint rejects non-PDF files."""
        # Get valid token first
        login_response = client.post(
            "/api/admin/login",
            json={"username": "admin", "password": "Shreyansh@2025"}
        )
        token = login_response.json()["access_token"]
        
        response = client.post(
            "/api/admin/upload-resume",
            files={"file": ("test.txt", b"not a pdf", "text/plain")},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 400
        assert "Only PDF files are allowed" in response.json()["detail"]


class TestErrorHandling:
    """Tests for error handling in main.py."""
    
    def test_404_endpoint(self):
        """Test 404 for non-existent endpoint."""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_method_not_allowed(self):
        """Test method not allowed error."""
        response = client.put("/api/health")
        assert response.status_code == 405
    
    def test_chat_with_agentic_system_not_initialized(self):
        """Test chat when agentic system is not initialized."""
        with patch('main.agentic_chatbot', None):
            response = client.post(
                "/api/chat",
                json={"message": "Test message"}
            )
            
            assert response.status_code == 503
            assert "not initialized" in response.json()["detail"]
    
    def test_chat_validation_error(self):
        """Test chat with validation error from agentic system."""
        with patch('main.agentic_chatbot') as mock_chatbot:
            mock_chatbot.check_health = AsyncMock(return_value=True)
            mock_chatbot.chat = AsyncMock(side_effect=ValueError("Validation failed"))
            
            response = client.post(
                "/api/chat",
                json={"message": "Test message"}
            )
            
            assert response.status_code == 400
            assert "Validation failed" in response.json()["detail"]
    
    def test_chat_general_exception(self):
        """Test chat with general exception."""
        with patch('main.agentic_chatbot') as mock_chatbot:
            mock_chatbot.check_health = AsyncMock(return_value=True)
            mock_chatbot.chat = AsyncMock(side_effect=Exception("Unknown error"))
            
            response = client.post(
                "/api/chat",
                json={"message": "Test message"}
            )
            
            assert response.status_code == 500
    
    def test_resume_endpoint_exception(self):
        """Test resume endpoint with exception."""
        with patch('main.get_current_resume', side_effect=Exception("Database error")):
            response = client.get("/api/resume")
            
            assert response.status_code == 500
            assert "Failed to fetch resume data" in response.json()["detail"]


class TestAdminUploadFlow:
    """Comprehensive tests for admin upload flow."""
    
    def test_upload_with_valid_pdf(self):
        """Test successful PDF upload and parsing."""
        # Get valid token
        login_response = client.post(
            "/api/admin/login",
            json={"username": "admin", "password": "Shreyansh@2025"}
        )
        token = login_response.json()["access_token"]
        
        # Mock PDF parser
        with patch('main.get_pdf_parser') as mock_parser_getter:
            mock_parser = Mock()
            mock_resume = Mock()
            mock_resume.contact_info.name = "Test User"
            mock_resume.contact_info.email = "test@example.com"
            mock_resume.experience = []
            mock_resume.education = []
            mock_resume.skills = []
            mock_resume.projects = []
            
            mock_parser.parse_resume = AsyncMock(return_value=mock_resume)
            mock_parser_getter.return_value = mock_parser
            
            with patch('main.update_resume_data'):
                response = client.post(
                    "/api/admin/upload-resume",
                    files={"file": ("resume.pdf", b"fake pdf content", "application/pdf")},
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["success"] is True
                assert "resume" in data
    
    def test_upload_pdf_parsing_error(self):
        """Test upload with PDF parsing validation error."""
        # Get valid token
        login_response = client.post(
            "/api/admin/login",
            json={"username": "admin", "password": "Shreyansh@2025"}
        )
        token = login_response.json()["access_token"]
        
        with patch('main.get_pdf_parser') as mock_parser_getter:
            mock_parser = Mock()
            mock_parser.parse_resume = AsyncMock(side_effect=ValueError("Invalid PDF format"))
            mock_parser_getter.return_value = mock_parser
            
            response = client.post(
                "/api/admin/upload-resume",
                files={"file": ("resume.pdf", b"fake pdf content", "application/pdf")},
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 400
            assert "Invalid PDF format" in response.json()["detail"]
    
    def test_upload_pdf_general_error(self):
        """Test upload with general processing error."""
        # Get valid token
        login_response = client.post(
            "/api/admin/login",
            json={"username": "admin", "password": "Shreyansh@2025"}
        )
        token = login_response.json()["access_token"]
        
        with patch('main.get_pdf_parser') as mock_parser_getter:
            mock_parser = Mock()
            mock_parser.parse_resume = AsyncMock(side_effect=Exception("Processing failed"))
            mock_parser_getter.return_value = mock_parser
            
            response = client.post(
                "/api/admin/upload-resume",
                files={"file": ("resume.pdf", b"fake pdf content", "application/pdf")},
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 500
            assert "Failed to process resume" in response.json()["detail"]
