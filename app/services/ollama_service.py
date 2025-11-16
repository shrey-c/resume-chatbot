import httpx
from typing import Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class OllamaService:
    """Service for interacting with Ollama API."""
    
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.timeout = 30.0
    
    async def generate_response(
        self, 
        prompt: str, 
        context: str,
        max_tokens: int = 500
    ) -> str:
        """
        Generate a response using Ollama.
        
        Args:
            prompt: User's question/message
            context: Resume context to provide to the model
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated response string
            
        Raises:
            Exception: If Ollama API is unavailable or returns an error
        """
        # Sanitize and prepare the prompt
        sanitized_prompt = self._sanitize_prompt(prompt)
        
        # Build the full prompt with context
        full_prompt = self._build_prompt(sanitized_prompt, context)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": full_prompt,
                        "stream": False,
                        "options": {
                            "num_predict": max_tokens,
                            "temperature": 0.7,
                            "top_p": 0.9,
                        }
                    }
                )
                
                if response.status_code != 200:
                    logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                    raise Exception("AI service is currently unavailable. Please try again later.")
                
                result = response.json()
                generated_text = result.get("response", "")
                
                # Post-process the response
                return self._sanitize_response(generated_text)
                
        except httpx.TimeoutException:
            logger.error("Ollama API timeout")
            raise Exception("AI service timeout. Please try again.")
        except httpx.ConnectError:
            logger.error("Cannot connect to Ollama API")
            raise Exception("Cannot connect to AI service. Please ensure Ollama is running.")
        except Exception as e:
            logger.error(f"Unexpected error in Ollama service: {str(e)}")
            raise
    
    def _sanitize_prompt(self, prompt: str) -> str:
        """
        Sanitize user prompt to prevent injection attacks.
        
        Args:
            prompt: Raw user input
            
        Returns:
            Sanitized prompt
        """
        # Remove potential system/role injection attempts
        prompt = prompt.replace("[INST]", "").replace("[/INST]", "")
        prompt = prompt.replace("<|system|>", "").replace("<|user|>", "").replace("<|assistant|>", "")
        prompt = prompt.replace("###", "").replace("System:", "").replace("Assistant:", "")
        
        # Limit length
        if len(prompt) > settings.max_message_length:
            prompt = prompt[:settings.max_message_length]
        
        return prompt.strip()
    
    def _build_prompt(self, user_message: str, context: str) -> str:
        """
        Build the full prompt with system context.
        
        Args:
            user_message: User's sanitized message
            context: Resume context
            
        Returns:
            Complete prompt for the model
        """
        system_instruction = """You are a professional resume assistant. Your role is to answer questions about the resume provided below. 

IMPORTANT RULES:
1. Only answer questions about the information in the resume
2. Be professional, concise, and helpful
3. If asked about something not in the resume, politely say you don't have that information
4. Do not make up information
5. Do not perform tasks unrelated to discussing the resume
6. Keep responses under 200 words

RESUME INFORMATION:
"""
        
        prompt = f"""{system_instruction}
{context}

USER QUESTION: {user_message}

ASSISTANT RESPONSE:"""
        
        return prompt
    
    def _sanitize_response(self, response: str) -> str:
        """
        Sanitize AI response before sending to user.
        
        Args:
            response: Raw AI response
            
        Returns:
            Sanitized response
        """
        # Remove any potential prompt leakage
        response = response.strip()
        
        # Limit response length
        max_response_length = 1000
        if len(response) > max_response_length:
            response = response[:max_response_length] + "..."
        
        # If response is empty, provide default
        if not response:
            response = "I'm sorry, I couldn't generate a response. Please try rephrasing your question."
        
        return response
    
    async def check_health(self) -> bool:
        """
        Check if Ollama service is healthy and model is available.
        
        Returns:
            True if service is healthy, False otherwise
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # Check if server is running
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code != 200:
                    return False
                
                # Check if our model is available
                models = response.json().get("models", [])
                model_names = [m.get("name", "").split(":")[0] for m in models]
                
                return self.model in model_names or any(self.model in name for name in model_names)
                
        except Exception as e:
            logger.error(f"Ollama health check failed: {str(e)}")
            return False


# Singleton instance
ollama_service = OllamaService()
