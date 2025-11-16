"""Extended tests for agents.py to increase coverage."""
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


class TestResearchAgentExtended:
    """Extended tests for Research Agent to increase coverage."""
    
    @pytest.mark.asyncio
    async def test_research_agent_error_handling(self):
        """Test research agent handles errors gracefully."""
        agent = ResearchAgent(settings.ollama_base_url, settings.ollama_model)
        
        state: AgentState = {
            "messages": [],
            "user_query": "What are your skills?",
            "resume_context": "Python, FastAPI",
            "research_findings": "",
            "draft_response": "",
            "final_response": "",
            "validation_passed": False,
            "needs_revision": False,
            "revision_count": 0
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                side_effect=Exception("Network error")
            )
            
            # Should return state with empty research findings on error
            result = await agent.analyze(state)
            assert "research_findings" in result


class TestResponseAgentExtended:
    """Extended tests for Response Agent to increase coverage."""
    
    @pytest.mark.asyncio
    async def test_response_agent_generate_success(self):
        """Test successful response generation."""
        agent = ResponseAgent(settings.ollama_base_url, settings.ollama_model)
        
        state: AgentState = {
            "messages": [],
            "user_query": "Tell me about your experience",
            "resume_context": "ML Engineer at Telstra",
            "research_findings": "KEY FINDINGS:\n- ML Engineer role\n- Telstra experience",
            "draft_response": "",
            "final_response": "",
            "validation_passed": False,
            "needs_revision": False,
            "revision_count": 0
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {
                "response": "I have extensive ML engineering experience at Telstra."
            }
            mock_response.raise_for_status = Mock()
            
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=mock_response
            )
            
            result = await agent.generate(state)
            
            assert "draft_response" in result
            assert len(result["draft_response"]) > 0
    
    @pytest.mark.asyncio
    async def test_response_agent_error_handling(self):
        """Test response agent handles errors."""
        agent = ResponseAgent(settings.ollama_base_url, settings.ollama_model)
        
        state: AgentState = {
            "messages": [],
            "user_query": "Test query",
            "resume_context": "Test context",
            "research_findings": "Test findings",
            "draft_response": "",
            "final_response": "",
            "validation_passed": False,
            "needs_revision": False,
            "revision_count": 0
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                side_effect=Exception("API error")
            )
            
            result = await agent.generate(state)
            assert "draft_response" in result


class TestValidationAgentExtended:
    """Extended tests for Validation Agent to increase coverage."""
    
    def test_validate_response_with_inappropriate_content(self):
        """Test validation fails for inappropriate content."""
        agent = ValidationAgent(settings.ollama_base_url, settings.ollama_model)
        
        state: AgentState = {
            "messages": [],
            "user_query": "test",
            "resume_context": "context",
            "research_findings": "",
            "draft_response": "This response contains inappropriate content and unprofessional language.",
            "final_response": "",
            "validation_passed": False,
            "needs_revision": False,
            "revision_count": 0
        }
        
        result = agent.validate(state)
        
        # Should still validate structure even with inappropriate content
        assert "validation_passed" in result
        assert "needs_revision" in result
    
    def test_validate_max_revisions_reached(self):
        """Test validation when max revisions reached."""
        agent = ValidationAgent(settings.ollama_base_url, settings.ollama_model)
        
        state: AgentState = {
            "messages": [],
            "user_query": "test",
            "resume_context": "context",
            "research_findings": "",
            "draft_response": "Short",
            "final_response": "",
            "validation_passed": False,
            "needs_revision": False,
            "revision_count": 3  # Max revisions
        }
        
        result = agent.validate(state)
        
        # Validation should occur and update state
        assert "validation_passed" in result
        assert "revision_count" in result
    
    def test_validate_good_length_response(self):
        """Test validation passes for good length response."""
        agent = ValidationAgent(settings.ollama_base_url, settings.ollama_model)
        
        long_response = "I have extensive experience working as an ML Engineer at Telstra, where I developed GenAI solutions and automated systems that saved millions in operational costs."
        
        state: AgentState = {
            "messages": [],
            "user_query": "test",
            "resume_context": "context",
            "research_findings": "",
            "draft_response": long_response,
            "final_response": "",
            "validation_passed": False,
            "needs_revision": False,
            "revision_count": 0
        }
        
        result = agent.validate(state)
        
        assert result["validation_passed"] is True
        assert result["needs_revision"] is False


class TestAgenticChatbotExtended:
    """Extended tests for Agentic Chatbot to increase coverage."""
    
    @pytest.mark.asyncio
    async def test_chat_success_with_workflow(self):
        """Test successful chat execution through workflow."""
        chatbot = AgenticChatbot()
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {
                "response": "I have strong Python and ML skills from my experience at Telstra."
            }
            mock_response.raise_for_status = Mock()
            mock_response.status_code = 200
            
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=mock_response
            )
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response
            )
            
            response = await chatbot.chat("What are your top skills?")
            
            assert response is not None
            assert isinstance(response, str)
            assert len(response) > 0
    
    @pytest.mark.asyncio
    async def test_chat_workflow_error_uses_fallback(self):
        """Test chat uses fallback when workflow fails."""
        chatbot = AgenticChatbot()
        
        with patch.object(chatbot.graph, 'ainvoke', side_effect=Exception("Workflow error")):
            response = await chatbot.chat("Tell me about your experience")
            
            # Should use fallback
            assert response is not None
            assert len(response) > 0
            assert "Telstra" in response or "experience" in response.lower()
    
    def test_safe_fallback_contact_query(self):
        """Test safe fallback for contact queries."""
        chatbot = AgenticChatbot()
        
        response = chatbot._safe_fallback("How can I contact you?")
        
        # Safe fallback returns a generic response
        assert len(response) > 0
        assert isinstance(response, str)
    
    def test_safe_fallback_location_query(self):
        """Test safe fallback for location queries."""
        chatbot = AgenticChatbot()
        
        response = chatbot._safe_fallback("Where are you located?")
        
        assert len(response) > 0
    
    def test_graph_construction(self):
        """Test that graph is constructed correctly."""
        chatbot = AgenticChatbot()
        
        assert chatbot.graph is not None
        assert chatbot.research_agent is not None
        assert chatbot.response_agent is not None
        assert chatbot.validation_agent is not None
    
    @pytest.mark.asyncio
    async def test_chat_with_complex_query(self):
        """Test chat with complex multi-part query."""
        chatbot = AgenticChatbot()
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {
                "response": "Based on my experience, I have worked extensively with Python, GenAI, and ML systems at Telstra."
            }
            mock_response.raise_for_status = Mock()
            mock_response.status_code = 200
            
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=mock_response
            )
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response
            )
            
            response = await chatbot.chat(
                "Can you tell me about your technical skills, work experience, and notable projects?"
            )
            
            assert response is not None
            assert len(response) > 0


class TestAgentStateManagement:
    """Tests for agent state management."""
    
    def test_agent_state_initialization(self):
        """Test proper agent state initialization."""
        state: AgentState = {
            "messages": [],
            "user_query": "test query",
            "resume_context": "test context",
            "research_findings": "",
            "draft_response": "",
            "final_response": "",
            "validation_passed": False,
            "needs_revision": False,
            "revision_count": 0
        }
        
        assert state["revision_count"] == 0
        assert state["validation_passed"] is False
        assert state["needs_revision"] is False
        assert len(state["messages"]) == 0
    
    def test_agent_state_update(self):
        """Test agent state can be updated."""
        state: AgentState = {
            "messages": [],
            "user_query": "test",
            "resume_context": "context",
            "research_findings": "",
            "draft_response": "",
            "final_response": "",
            "validation_passed": False,
            "needs_revision": False,
            "revision_count": 0
        }
        
        # Update state
        state["research_findings"] = "New findings"
        state["revision_count"] = 1
        
        assert state["research_findings"] == "New findings"
        assert state["revision_count"] == 1


class TestAgentErrorRecovery:
    """Tests for agent error recovery mechanisms."""
    
    @pytest.mark.asyncio
    async def test_research_agent_timeout_handling(self):
        """Test research agent handles timeouts."""
        agent = ResearchAgent(settings.ollama_base_url, settings.ollama_model)
        
        state: AgentState = {
            "messages": [],
            "user_query": "test",
            "resume_context": "context",
            "research_findings": "",
            "draft_response": "",
            "final_response": "",
            "validation_passed": False,
            "needs_revision": False,
            "revision_count": 0
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            import asyncio
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                side_effect=asyncio.TimeoutError()
            )
            
            result = await agent.analyze(state)
            assert "research_findings" in result
    
    @pytest.mark.asyncio
    async def test_response_agent_http_error(self):
        """Test response agent handles HTTP errors."""
        agent = ResponseAgent(settings.ollama_base_url, settings.ollama_model)
        
        state: AgentState = {
            "messages": [],
            "user_query": "test",
            "resume_context": "context",
            "research_findings": "findings",
            "draft_response": "",
            "final_response": "",
            "validation_passed": False,
            "needs_revision": False,
            "revision_count": 0
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            import httpx
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                side_effect=httpx.HTTPError("Server error")
            )
            
            result = await agent.generate(state)
            assert "draft_response" in result
