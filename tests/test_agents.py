"""Tests for multi-agent system."""
import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from app.services.agents import (
    AgenticChatbot,
    ResearchAgent,
    ResponseAgent,
    ValidationAgent,
    AgentState
)
from app.core.config import settings


class TestAgentState:
    """Tests for AgentState TypedDict."""
    
    def test_agent_state_structure(self):
        """Test AgentState has required keys."""
        state: AgentState = {
            "messages": [],
            "user_query": "test query",
            "resume_context": "context",
            "research_findings": "",
            "draft_response": "",
            "final_response": "",
            "validation_passed": False,
            "needs_revision": False,
            "revision_count": 0
        }
        
        assert "user_query" in state
        assert "resume_context" in state
        assert "validation_passed" in state


class TestResearchAgent:
    """Tests for Research Agent."""
    
    def test_research_agent_initialization(self):
        """Test Research Agent initialization."""
        agent = ResearchAgent(settings.ollama_base_url, settings.ollama_model)
        
        assert agent.ollama_base_url == settings.ollama_base_url
        assert agent.ollama_model == settings.ollama_model
    
    @pytest.mark.asyncio
    async def test_research_agent_analyze_success(self):
        """Test successful research analysis."""
        agent = ResearchAgent(settings.ollama_base_url, settings.ollama_model)
        
        state: AgentState = {
            "messages": [],
            "user_query": "What are your skills?",
            "resume_context": "Python, FastAPI, Machine Learning",
            "research_findings": "",
            "draft_response": "",
            "final_response": "",
            "validation_passed": False,
            "needs_revision": False,
            "revision_count": 0
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {
                "response": "KEY FINDINGS:\n- Python expertise\n- FastAPI experience"
            }
            mock_response.raise_for_status = Mock()
            
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=mock_response
            )
            
            result = await agent.analyze(state)
            
            assert "research_findings" in result
            assert len(result["research_findings"]) > 0


class TestResponseAgent:
    """Tests for Response Agent."""
    
    def test_response_agent_initialization(self):
        """Test Response Agent initialization."""
        agent = ResponseAgent(settings.ollama_base_url, settings.ollama_model)
        
        assert agent.ollama_base_url == settings.ollama_base_url
        assert agent.ollama_model == settings.ollama_model


class TestValidationAgent:
    """Tests for Validation Agent."""
    
    def test_validation_agent_initialization(self):
        """Test Validation Agent initialization."""
        agent = ValidationAgent(settings.ollama_base_url, settings.ollama_model)
        
        assert agent.ollama_base_url == settings.ollama_base_url
        assert agent.ollama_model == settings.ollama_model
        assert len(agent.negative_patterns) > 0
        assert len(agent.inappropriate_patterns) > 0
    
    def test_validate_good_response(self):
        """Test validation of good response."""
        agent = ValidationAgent(settings.ollama_base_url, settings.ollama_model)
        
        state: AgentState = {
            "messages": [],
            "user_query": "test",
            "resume_context": "context",
            "research_findings": "",
            "draft_response": "I have extensive experience with Python and ML at Telstra.",
            "final_response": "",
            "validation_passed": False,
            "needs_revision": False,
            "revision_count": 0
        }
        
        result = agent.validate(state)
        
        assert result["validation_passed"] is True
        assert result["needs_revision"] is False
    
    def test_validate_response_with_negative_language(self):
        """Test validation fails for negative language."""
        agent = ValidationAgent(settings.ollama_base_url, settings.ollama_model)
        
        state: AgentState = {
            "messages": [],
            "user_query": "test",
            "resume_context": "context",
            "research_findings": "",
            "draft_response": "I have poor skills and failed at everything.",
            "final_response": "",
            "validation_passed": False,
            "needs_revision": False,
            "revision_count": 0
        }
        
        result = agent.validate(state)
        
        assert result["validation_passed"] is False
        assert result["needs_revision"] is True
    
    def test_validate_response_too_short(self):
        """Test validation fails for too short response."""
        agent = ValidationAgent(settings.ollama_base_url, settings.ollama_model)
        
        state: AgentState = {
            "messages": [],
            "user_query": "test",
            "resume_context": "context",
            "research_findings": "",
            "draft_response": "Yes.",
            "final_response": "",
            "validation_passed": False,
            "needs_revision": False,
            "revision_count": 0
        }
        
        result = agent.validate(state)
        
        assert result["validation_passed"] is False
        assert result["needs_revision"] is True


class TestAgenticChatbot:
    """Tests for main Agentic Chatbot."""
    
    def test_agentic_chatbot_initialization(self):
        """Test Agentic Chatbot initialization."""
        chatbot = AgenticChatbot()
        
        assert chatbot.ollama_base_url == settings.ollama_base_url
        assert chatbot.ollama_model == settings.ollama_model
        assert chatbot.research_agent is not None
        assert chatbot.response_agent is not None
        assert chatbot.validation_agent is not None
        assert chatbot.graph is not None
    
    @pytest.mark.asyncio
    async def test_check_health_success(self):
        """Test health check succeeds."""
        chatbot = AgenticChatbot()
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.status_code = 200
            
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response
            )
            
            is_healthy = await chatbot.check_health()
            assert is_healthy is True
    
    @pytest.mark.asyncio
    async def test_check_health_failure(self):
        """Test health check fails."""
        chatbot = AgenticChatbot()
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                side_effect=Exception("Connection failed")
            )
            
            is_healthy = await chatbot.check_health()
            assert is_healthy is False
    
    def test_safe_fallback_experience_query(self):
        """Test safe fallback for experience queries."""
        chatbot = AgenticChatbot()
        
        response = chatbot._safe_fallback("Tell me about your work experience")
        
        assert "Telstra" in response
        assert "ML Engineer" in response or "experience" in response.lower()
    
    def test_safe_fallback_skills_query(self):
        """Test safe fallback for skills queries."""
        chatbot = AgenticChatbot()
        
        response = chatbot._safe_fallback("What are your skills?")
        
        assert "Python" in response or "GenAI" in response or "skill" in response.lower()
    
    def test_safe_fallback_projects_query(self):
        """Test safe fallback for projects queries."""
        chatbot = AgenticChatbot()
        
        response = chatbot._safe_fallback("Tell me about your projects")
        
        assert "AskTelstra" in response or "project" in response.lower()
    
    def test_safe_fallback_education_query(self):
        """Test safe fallback for education queries."""
        chatbot = AgenticChatbot()
        
        response = chatbot._safe_fallback("Where did you study?")
        
        assert "VJTI" in response or "education" in response.lower() or "degree" in response.lower()
    
    def test_safe_fallback_generic_query(self):
        """Test safe fallback for generic queries."""
        chatbot = AgenticChatbot()
        
        response = chatbot._safe_fallback("Hello")
        
        assert len(response) > 0
        assert "experience" in response.lower() or "background" in response.lower()
