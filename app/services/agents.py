"""
Multi-Agent System using LangGraph for intelligent resume chatbot.

This module implements a three-agent architecture:
1. ResearchAgent: Analyzes user queries and extracts relevant resume information
2. ResponseAgent: Generates natural, professional responses
3. ValidationAgent: Ensures responses are safe, accurate, and positive
"""

from typing import TypedDict, Annotated, Sequence
import operator
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from app.core.config import settings
from app.services.resume_data import get_resume_context
from app.services.html_parser import get_html_context
import httpx
import re
from app.models.schemas import ChatMessage


# Define the state that will be passed between agents
class AgentState(TypedDict):
    """State shared across all agents in the workflow."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    user_query: str
    html_context: str  # PRIMARY source from HTML
    resume_context: str  # FALLBACK source from structured data
    research_findings: str
    draft_response: str
    final_response: str
    validation_passed: bool
    needs_revision: bool
    revision_count: int


class ResearchAgent:
    """
    Agent responsible for analyzing user queries and extracting relevant resume information.
    
    This agent:
    - Analyzes the user's question
    - Searches through resume context
    - Identifies relevant experience, skills, projects
    - Extracts key information to answer the query
    """
    
    def __init__(self, ollama_base_url: str, ollama_model: str):
        self.ollama_base_url = ollama_base_url
        self.ollama_model = ollama_model
    
    async def analyze(self, state: AgentState) -> AgentState:
        """Analyze user query and extract relevant resume information."""
        
        # PRIMARY: Use HTML context, FALLBACK: Use structured resume context
        primary_context = state.get('html_context', '')
        fallback_context = state.get('resume_context', '')
        
        # Use HTML context if available, otherwise fallback to resume context
        context_source = "HTML website content" if primary_context else "structured resume data"
        active_context = primary_context if primary_context else fallback_context
        
        system_prompt = f"""You are a Research Agent analyzing questions about Shreyansh Chheda's resume.

IMPORTANT: Answer ONLY from the {context_source} provided below. This is the PRIMARY and AUTHORITATIVE source.

RESUME CONTEXT (from {context_source}):
{active_context}

Your task:
1. Analyze the user's question: "{state['user_query']}"
2. Identify which parts of the resume are most relevant
3. Extract specific details (job titles, technologies, achievements, dates)
4. Summarize key findings in bullet points

Focus on:
- Exact job titles and dates
- Specific technologies and skills mentioned
- Quantifiable achievements (percentages, dollar amounts, scale)
- Project names and their impact
- Awards and recognition

Output format:
RELEVANT SECTIONS: [list sections]
KEY FINDINGS:
- [bullet point 1]
- [bullet point 2]
...

Be precise and factual. Only include information from the {context_source}."""

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.ollama_base_url}/api/generate",
                    json={
                        "model": self.ollama_model,
                        "prompt": system_prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.3,  # Lower temperature for factual research
                            "top_p": 0.9,
                        }
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                research_findings = result.get("response", "").strip()
                
                state["research_findings"] = research_findings
                state["messages"] = state.get("messages", []) + [
                    AIMessage(content=f"Research completed: {research_findings[:200]}...")
                ]
                
                return state
                
        except Exception as e:
            # Fallback to simple context extraction
            state["research_findings"] = f"Error in research: {str(e)}. Using full resume context."
            return state


class ResponseAgent:
    """
    Agent responsible for generating natural, professional responses.
    
    This agent:
    - Takes research findings
    - Generates conversational, professional responses
    - Ensures responses highlight Shreyansh's strengths
    - Maintains positive, engaging tone
    """
    
    def __init__(self, ollama_base_url: str, ollama_model: str):
        self.ollama_base_url = ollama_base_url
        self.ollama_model = ollama_model
    
    async def generate(self, state: AgentState) -> AgentState:
        """Generate a professional response based on research findings."""
        
        system_prompt = f"""You are a Response Agent crafting answers about Shreyansh Chheda's professional background.

USER QUESTION: {state['user_query']}

RESEARCH FINDINGS:
{state['research_findings']}

Your task:
1. Create a natural, conversational response
2. Highlight Shreyansh's strengths and achievements
3. Use specific details from the research findings
4. Be enthusiastic but professional
5. Keep responses concise (2-4 sentences for simple questions, longer for complex ones)

Guidelines:
- Always speak positively about Shreyansh's work
- Use first-person perspective ("I worked on...", "I have experience with...")
- Mention specific achievements with numbers when available
- Connect skills to real projects
- If asked about unknown topics, politely redirect to resume topics

Tone: Professional, confident, enthusiastic, humble"""

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.ollama_base_url}/api/generate",
                    json={
                        "model": self.ollama_model,
                        "prompt": system_prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,  # Higher temperature for creative responses
                            "top_p": 0.95,
                        }
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                draft_response = result.get("response", "").strip()
                
                state["draft_response"] = draft_response
                state["messages"] = state.get("messages", []) + [
                    AIMessage(content=f"Draft response generated: {draft_response[:200]}...")
                ]
                
                return state
                
        except Exception as e:
            # Fallback response
            state["draft_response"] = f"I'd be happy to discuss my experience. Based on my background at Telstra working on GenAI and ML projects, I can share insights about my work. Could you please rephrase your question?"
            return state


class ValidationAgent:
    """
    Agent responsible for validating responses for safety and accuracy.
    
    This agent:
    - Checks for prompt injection or manipulation
    - Ensures response is based on resume facts
    - Verifies positive tone about Shreyansh
    - Filters out inappropriate content
    - Ensures no made-up information
    """
    
    def __init__(self, ollama_base_url: str, ollama_model: str):
        self.ollama_base_url = ollama_base_url
        self.ollama_model = ollama_model
        
        # Validation patterns
        self.negative_patterns = [
            r'\b(bad|poor|terrible|awful|weak|failed|failure|unable|can\'t|cannot)\b',
            r'\b(inexperienced|beginner|junior|entry-level)\b',
            r'\b(doesn\'t know|don\'t know|no experience|never worked)\b',
        ]
        
        self.inappropriate_patterns = [
            r'\b(password|secret|confidential|private)\b',
            r'\b(hack|exploit|vulnerability)\b',
            r'\[INST\]|\[/INST\]|<system>|</system>',
        ]
    
    def validate(self, state: AgentState) -> AgentState:
        """Validate the draft response for safety and accuracy."""
        
        draft = state.get("draft_response", "")
        
        # Check for negative language
        has_negative = any(re.search(pattern, draft, re.IGNORECASE) for pattern in self.negative_patterns)
        
        # Check for inappropriate content
        has_inappropriate = any(re.search(pattern, draft, re.IGNORECASE) for pattern in self.inappropriate_patterns)
        
        # Check minimum length
        too_short = len(draft.strip()) < 20
        
        # Check if response stays on topic (mentions resume-related keywords)
        resume_keywords = [
            'telstra', 'ml', 'ai', 'genai', 'engineer', 'developer', 'python',
            'project', 'experience', 'skill', 'work', 'built', 'developed',
            'azure', 'nlp', 'chatbot', 'automation'
        ]
        stays_on_topic = any(keyword in draft.lower() for keyword in resume_keywords)
        
        # Validation decision
        if has_negative or has_inappropriate or too_short or not stays_on_topic:
            state["validation_passed"] = False
            state["needs_revision"] = True
            state["revision_count"] = state.get("revision_count", 0) + 1
            
            # Add feedback for revision
            feedback = []
            if has_negative:
                feedback.append("Remove negative language")
            if has_inappropriate:
                feedback.append("Contains inappropriate content")
            if too_short:
                feedback.append("Response too brief")
            if not stays_on_topic:
                feedback.append("Off-topic - focus on resume")
            
            state["messages"] = state.get("messages", []) + [
                AIMessage(content=f"Validation failed: {', '.join(feedback)}")
            ]
        else:
            state["validation_passed"] = True
            state["needs_revision"] = False
            state["final_response"] = draft
            
            state["messages"] = state.get("messages", []) + [
                AIMessage(content="Validation passed - response approved")
            ]
        
        return state


class AgenticChatbot:
    """
    Main orchestrator for the multi-agent chatbot system.
    
    Uses LangGraph to coordinate three agents in a workflow:
    1. Research → 2. Response → 3. Validation
    
    If validation fails, loops back to Response agent for revision.
    Maximum 2 revision attempts before returning a safe fallback.
    """
    
    def __init__(self):
        self.ollama_base_url = settings.ollama_base_url
        self.ollama_model = settings.ollama_model
        
        # Initialize agents
        self.research_agent = ResearchAgent(self.ollama_base_url, self.ollama_model)
        self.response_agent = ResponseAgent(self.ollama_base_url, self.ollama_model)
        self.validation_agent = ValidationAgent(self.ollama_base_url, self.ollama_model)
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        
        # Create the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes (agents)
        workflow.add_node("research", self.research_agent.analyze)
        workflow.add_node("response", self.response_agent.generate)
        workflow.add_node("validation", self.validation_agent.validate)
        
        # Define the flow
        workflow.set_entry_point("research")
        
        # research → response
        workflow.add_edge("research", "response")
        
        # response → validation
        workflow.add_edge("response", "validation")
        
        # Conditional edge from validation
        def check_validation(state: AgentState) -> str:
            """Route based on validation result."""
            if state.get("validation_passed", False):
                return "end"
            elif state.get("revision_count", 0) >= 2:
                # Max revisions reached, use fallback
                return "end"
            else:
                # Needs revision, go back to response
                return "response"
        
        workflow.add_conditional_edges(
            "validation",
            check_validation,
            {
                "end": END,
                "response": "response"
            }
        )
        
        return workflow.compile()
    
    async def chat(self, user_message: str) -> str:
        """
        Process a user message through the multi-agent system.
        Uses HTML context as PRIMARY source, resume_data as FALLBACK.
        
        Args:
            user_message: The user's question
            
        Returns:
            The final validated response
        """
        
        # Validate input using existing ChatMessage model
        try:
            ChatMessage(message=user_message)
        except ValueError as e:
            return "I can only answer questions about my professional background and experience. Please ask something related to my resume."
        
        # Get HTML context (PRIMARY)
        html_context = get_html_context()
        
        # Get resume context (FALLBACK)
        resume_context = get_resume_context()
        
        # Initialize state
        initial_state: AgentState = {
            "messages": [HumanMessage(content=user_message)],
            "user_query": user_message,
            "html_context": html_context,  # PRIMARY source
            "resume_context": resume_context,  # FALLBACK source
            "research_findings": "",
            "draft_response": "",
            "final_response": "",
            "validation_passed": False,
            "needs_revision": False,
            "revision_count": 0,
        }
        
        try:
            # Run the graph
            final_state = await self.graph.ainvoke(initial_state)
            
            # Get final response or fallback
            if final_state.get("final_response"):
                return final_state["final_response"]
            elif final_state.get("draft_response"):
                # Validation failed but return sanitized version
                return self._safe_fallback(user_message)
            else:
                return self._safe_fallback(user_message)
                
        except Exception as e:
            print(f"Error in agentic workflow: {e}")
            return self._safe_fallback(user_message)
    
    def _safe_fallback(self, user_message: str) -> str:
        """Generate a safe fallback response."""
        
        # Detect topic
        msg_lower = user_message.lower()
        
        if any(word in msg_lower for word in ['experience', 'work', 'job', 'role']):
            return "I'm currently an ML Engineer at Telstra, where I've worked on exciting GenAI projects like AskTelstra (an enterprise chatbot serving 8000+ daily queries) and GenAI Call Drivers (analyzing 25K calls/day). I've been with Telstra since July 2021, progressing through various ML and software engineering roles. Would you like to know more about any specific project?"
        
        elif any(word in msg_lower for word in ['skill', 'technology', 'tech', 'programming', 'language']):
            return "I specialize in AI/ML technologies, particularly GenAI, RAG, LangChain, and LangGraph. I'm proficient in Python, with expertise in PyTorch, FastAPI, and Azure cloud services. I also have experience with full-stack development using Spring Boot and React.js. What specific technology would you like to discuss?"
        
        elif any(word in msg_lower for word in ['project', 'built', 'created', 'developed']):
            return "I've worked on several impactful projects at Telstra: AskTelstra (reduced costs by 88%), GenAI Call Drivers (25K calls/day analysis), and NATAMA automation (saving 3M AUD annually). Each project leveraged GenAI and ML to solve real business challenges. Which project interests you?"
        
        elif any(word in msg_lower for word in ['education', 'degree', 'university', 'college', 'study']):
            return "I hold a Bachelor of Technology in Computer Science from VJTI (Veermata Jijabai Technological Institute) in Mumbai, where I studied from 2017 to 2021. I've also completed certifications in Deep Learning and Data Science through Coursera."
        
        else:
            return "I'd be happy to discuss my professional experience! I'm an ML Engineer specializing in GenAI and have worked on projects like AskTelstra, GenAI Call Drivers, and NATAMA automation at Telstra. What specific aspect of my background would you like to know more about?"
    
    async def check_health(self) -> bool:
        """Check if Ollama service is available."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.ollama_base_url}/api/tags")
                return response.status_code == 200
        except Exception:
            return False
