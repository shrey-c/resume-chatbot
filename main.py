from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
import logging
import shutil
from pathlib import Path

from app.models import ChatMessage, ChatResponse, Resume
from app.services import (
    update_resume_data, 
    get_current_resume,
    get_pdf_parser,
    AgenticChatbot
)
from app.core import settings, LoginRequest, TokenResponse, login_admin, get_current_admin

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.debug else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize agentic chatbot
agentic_chatbot = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    global agentic_chatbot
    
    # Startup
    logger.info("Starting Resume Chatbot API...")
    
    # Initialize agentic chatbot
    agentic_chatbot = AgenticChatbot()
    logger.info("Agentic multi-agent system initialized")
    
    # Check Ollama service health
    is_healthy = await agentic_chatbot.check_health()
    if not is_healthy:
        logger.warning(
            f"Ollama service is not available at {settings.ollama_base_url}. "
            f"Please ensure Ollama is running and model '{settings.ollama_model}' is installed."
        )
    else:
        logger.info(f"Ollama service is healthy. Using model: {settings.ollama_model}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Resume Chatbot API...")


# Initialize FastAPI app
app = FastAPI(
    title="Resume Chatbot API",
    description="An AI-powered chatbot for resume information",
    version="1.0.0",
    lifespan=lifespan
)

# Add rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Serve the main HTML page."""
    return FileResponse("static/index.html")


@app.get("/admin")
async def admin_page():
    """Serve the admin portal page."""
    return FileResponse("static/admin.html")


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns service status and Ollama availability.
    """
    global agentic_chatbot
    ollama_healthy = await agentic_chatbot.check_health() if agentic_chatbot else False
    
    return {
        "status": "healthy",
        "ollama_available": ollama_healthy,
        "ollama_model": settings.ollama_model,
        "agentic_system": "enabled"
    }


@app.get("/api/resume", response_model=Resume)
async def get_resume():
    """
    Get complete resume data (may be updated via admin portal).
    
    Returns:
        Resume object with all information
    """
    try:
        resume = get_current_resume()  # Use potentially updated resume
        return resume
    except Exception as e:
        logger.error(f"Error fetching resume data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch resume data")


@app.post("/api/chat", response_model=ChatResponse)
@limiter.limit(f"{settings.max_requests_per_minute}/minute")
async def chat(message: ChatMessage, request: Request):
    """
    Chat endpoint using multi-agent LangGraph system.
    
    Args:
        message: ChatMessage with user's question
        request: FastAPI Request object (used by rate limiter)
        
    Returns:
        ChatResponse with AI-generated answer from agentic system
        
    Raises:
        HTTPException: If Ollama service is unavailable or other errors occur
    """
    global agentic_chatbot
    
    try:
        # Check if Ollama is available
        if not agentic_chatbot:
            raise HTTPException(
                status_code=503,
                detail="Agentic system not initialized"
            )
        
        is_healthy = await agentic_chatbot.check_health()
        if not is_healthy:
            raise HTTPException(
                status_code=503,
                detail=f"AI service is currently unavailable. Please ensure Ollama is running with model '{settings.ollama_model}'"
            )
        
        # Use agentic chatbot for response (runs through LangGraph workflow)
        response_text = await agentic_chatbot.chat(message.message)
        
        return ChatResponse(response=response_text)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except ValueError as e:
        # Validation errors (e.g., from prompt injection detection)
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Other errors
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request. Please try again."
        )


# ============================================================================
# ADMIN PORTAL ENDPOINTS
# ============================================================================

@app.post("/api/admin/login", response_model=TokenResponse)
async def admin_login(login_request: LoginRequest):
    """
    Admin login endpoint.
    
    Authenticates admin user and returns JWT token.
    
    Args:
        login_request: Username and password
        
    Returns:
        TokenResponse with JWT access token
        
    Raises:
        HTTPException: If credentials are invalid
    """
    try:
        token_response = login_admin(
            username=login_request.username,
            password=login_request.password
        )
        logger.info(f"Admin login successful for user: {login_request.username}")
        return token_response
    except HTTPException:
        logger.warning(f"Failed login attempt for user: {login_request.username}")
        raise


@app.post("/api/admin/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    admin_user: str = Depends(get_current_admin)
):
    """
    Upload and process resume PDF.
    
    Protected endpoint - requires admin authentication.
    
    Args:
        file: PDF file upload
        admin_user: Current authenticated admin (from dependency)
        
    Returns:
        Success message with parsed resume data
        
    Raises:
        HTTPException: If file is invalid or processing fails
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
    
    # Create uploads directory
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    
    # Save uploaded file
    file_path = upload_dir / f"resume_{admin_user}_{file.filename}"
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Resume PDF uploaded: {file_path}")
        
        # Parse PDF using AI
        parser = get_pdf_parser()
        resume = await parser.parse_resume(str(file_path))
        
        logger.info(f"Resume parsed successfully: {resume.contact_info.name}")
        
        # Update resume_data.py with new data
        update_resume_data(resume)
        
        logger.info("Resume data updated successfully")
        
        # Clean up uploaded file (optional - keep for backup)
        # file_path.unlink()
        
        return {
            "success": True,
            "message": "Resume uploaded and processed successfully",
            "resume": {
                "name": resume.contact_info.name,
                "email": resume.contact_info.email,
                "experience_count": len(resume.experience),
                "education_count": len(resume.education),
                "skills_count": len(resume.skills),
                "projects_count": len(resume.projects)
            }
        }
        
    except ValueError as e:
        logger.error(f"Validation error processing resume: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing resume: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process resume: {str(e)}"
        )
    finally:
        await file.close()


@app.get("/api/admin/verify")
async def verify_admin(admin_user: str = Depends(get_current_admin)):
    """
    Verify admin token is valid.
    
    Protected endpoint - requires admin authentication.
    
    Args:
        admin_user: Current authenticated admin (from dependency)
        
    Returns:
        Admin user info
    """
    return {
        "authenticated": True,
        "username": admin_user
    }


# ============================================================================
# ERROR HANDLERS
# ============================================================================


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unexpected errors."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )


# Mount static files (will be created next)
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception:
    # Static directory might not exist yet
    logger.warning("Static directory not found. Will be created when running the app.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
