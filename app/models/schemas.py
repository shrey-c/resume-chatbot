from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional
from datetime import date
from enum import Enum


class SkillCategory(str, Enum):
    """Enumeration for skill categories."""
    AI_ML = "AI & Machine Learning"
    GENERATIVE_AI = "Generative AI"
    PROGRAMMING = "Programming"
    FRAMEWORKS = "Frameworks & Libraries"
    DATABASES = "Databases & Vector Stores"
    CLOUD_DEVOPS = "Cloud & DevOps"
    TOOLS = "Tools & Platforms"
    SOFT_SKILLS = "Soft Skills"
    OTHER = "Other"


class Skill(BaseModel):
    """Model for a skill."""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the skill")
    category: SkillCategory = Field(..., description="Category of the skill")
    proficiency: Optional[str] = Field(None, max_length=50, description="Proficiency level (e.g., Beginner, Intermediate, Expert)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Python",
                "category": "Programming",
                "proficiency": "Expert"
            }
        }
    )


class Experience(BaseModel):
    """Model for work experience."""
    company: str = Field(..., min_length=1, max_length=200, description="Company name")
    position: str = Field(..., min_length=1, max_length=200, description="Job position/title")
    location: Optional[str] = Field(None, max_length=200, description="Location of the job")
    start_date: str = Field(..., description="Start date (YYYY-MM or YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM or YYYY-MM-DD), None if current")
    description: str = Field(..., min_length=10, max_length=2000, description="Job description")
    achievements: List[str] = Field(default_factory=list, description="List of achievements")
    
    @field_validator('achievements')
    @classmethod
    def validate_achievements(cls, v):
        if len(v) > 20:
            raise ValueError("Too many achievements (max 20)")
        for achievement in v:
            if len(achievement) > 500:
                raise ValueError("Achievement description too long (max 500 characters)")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "company": "Tech Corp",
                "position": "Senior Software Engineer",
                "location": "San Francisco, CA",
                "start_date": "2020-01",
                "end_date": "2023-12",
                "description": "Led development of key features",
                "achievements": ["Improved performance by 50%", "Mentored 5 junior developers"]
            }
        }
    )


class Education(BaseModel):
    """Model for educational background."""
    institution: str = Field(..., min_length=1, max_length=200, description="Name of the institution")
    degree: str = Field(..., min_length=1, max_length=200, description="Degree obtained")
    field_of_study: str = Field(..., min_length=1, max_length=200, description="Field of study/major")
    location: Optional[str] = Field(None, max_length=200, description="Location of the institution")
    start_date: str = Field(..., description="Start date (YYYY-MM or YYYY)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM or YYYY), None if current")
    gpa: Optional[str] = Field(None, max_length=20, description="GPA or grade")
    honors: List[str] = Field(default_factory=list, description="Honors and awards")
    
    @field_validator('honors')
    @classmethod
    def validate_honors(cls, v):
        if len(v) > 10:
            raise ValueError("Too many honors (max 10)")
        for honor in v:
            if len(honor) > 200:
                raise ValueError("Honor description too long (max 200 characters)")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "institution": "University of Technology",
                "degree": "Bachelor of Science",
                "field_of_study": "Computer Science",
                "location": "Boston, MA",
                "start_date": "2016",
                "end_date": "2020"
            }
        }
    )


class Project(BaseModel):
    """Model for projects."""
    name: str = Field(..., min_length=1, max_length=200, description="Project name")
    description: str = Field(..., min_length=10, max_length=2000, description="Project description")
    technologies: List[str] = Field(..., min_length=1, description="Technologies used")
    url: Optional[str] = Field(None, max_length=500, description="Project URL or repository")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM or YYYY)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM or YYYY)")
    highlights: List[str] = Field(default_factory=list, description="Project highlights")
    
    @field_validator('technologies')
    @classmethod
    def validate_technologies(cls, v):
        if len(v) > 20:
            raise ValueError("Too many technologies (max 20)")
        for tech in v:
            if len(tech) > 100:
                raise ValueError("Technology name too long (max 100 characters)")
        return v
    
    @field_validator('highlights')
    @classmethod
    def validate_highlights(cls, v):
        if len(v) > 10:
            raise ValueError("Too many highlights (max 10)")
        for highlight in v:
            if len(highlight) > 500:
                raise ValueError("Highlight description too long (max 500 characters)")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Resume Chatbot",
                "description": "An intelligent chatbot for resume information",
                "technologies": ["Python", "FastAPI", "Ollama"],
                "url": "https://github.com/username/resume-chatbot",
                "start_date": "2024-01",
                "highlights": ["Built with AI", "Fully responsive design"]
            }
        }
    )


class Certification(BaseModel):
    """Model for certifications."""
    name: str = Field(..., min_length=1, max_length=200, description="Certification name")
    issuer: str = Field(..., min_length=1, max_length=200, description="Issuing organization")
    issue_date: str = Field(..., description="Issue date (YYYY-MM or YYYY)")
    credential_id: Optional[str] = Field(None, max_length=200, description="Credential ID")
    credential_url: Optional[str] = Field(None, max_length=500, description="Credential URL")
    skills: List[str] = Field(default_factory=list, description="Skills covered")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Deep Learning Specialization",
                "issuer": "Coursera",
                "issue_date": "2020-06",
                "credential_id": "LPM2R2FKSZMX",
                "skills": ["Deep Learning", "Neural Networks"]
            }
        }
    )


class Award(BaseModel):
    """Model for awards and recognition."""
    title: str = Field(..., min_length=1, max_length=200, description="Award title")
    issuer: str = Field(..., min_length=1, max_length=200, description="Issuing organization")
    date: str = Field(..., description="Award date (YYYY-MM or YYYY)")
    description: Optional[str] = Field(None, max_length=500, description="Award description")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Employee of the Month",
                "issuer": "Tech Corp",
                "date": "2023-06",
                "description": "Recognized for outstanding performance"
            }
        }
    )


class Interest(BaseModel):
    """Model for hobbies and interests."""
    name: str = Field(..., min_length=1, max_length=100, description="Interest name")
    description: Optional[str] = Field(None, max_length=500, description="Interest description")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Photography",
                "description": "Landscape and nature photography enthusiast"
            }
        }
    )


class ContactInfo(BaseModel):
    """Model for contact information."""
    email: Optional[str] = Field(None, max_length=200, description="Email address")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")
    linkedin: Optional[str] = Field(None, max_length=200, description="LinkedIn profile URL")
    github: Optional[str] = Field(None, max_length=200, description="GitHub profile URL")
    website: Optional[str] = Field(None, max_length=200, description="Personal website URL")
    location: Optional[str] = Field(None, max_length=200, description="Current location")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "shreyansh@example.com",
                "phone": "+1-234-567-8900",
                "linkedin": "https://linkedin.com/in/shreyansh",
                "github": "https://github.com/shreyansh",
                "location": "San Francisco, CA"
            }
        }
    )


class Resume(BaseModel):
    """Complete resume model."""
    name: str = Field(..., min_length=1, max_length=200, description="Full name")
    title: str = Field(..., min_length=1, max_length=200, description="Professional title")
    summary: str = Field(..., min_length=10, max_length=2000, description="Professional summary")
    contact: ContactInfo = Field(..., description="Contact information")
    experience: List[Experience] = Field(default_factory=list, description="Work experience")
    education: List[Education] = Field(default_factory=list, description="Educational background")
    skills: List[Skill] = Field(default_factory=list, description="Skills")
    projects: List[Project] = Field(default_factory=list, description="Projects")
    certifications: List[Certification] = Field(default_factory=list, description="Certifications")
    awards: List[Award] = Field(default_factory=list, description="Awards and recognition")
    languages: List[str] = Field(default_factory=list, description="Languages spoken")
    interests: List[Interest] = Field(default_factory=list, description="Hobbies and interests")
    
    @field_validator('experience')
    @classmethod
    def validate_experience(cls, v):
        if len(v) > 20:
            raise ValueError("Too many experience entries (max 20)")
        return v
    
    @field_validator('education')
    @classmethod
    def validate_education(cls, v):
        if len(v) > 10:
            raise ValueError("Too many education entries (max 10)")
        return v
    
    @field_validator('skills')
    @classmethod
    def validate_skills(cls, v):
        if len(v) > 150:
            raise ValueError("Too many skills (max 150)")
        return v
    
    @field_validator('projects')
    @classmethod
    def validate_projects(cls, v):
        if len(v) > 20:
            raise ValueError("Too many projects (max 20)")
        return v
    
    @field_validator('certifications')
    @classmethod
    def validate_certifications(cls, v):
        if len(v) > 20:
            raise ValueError("Too many certifications (max 20)")
        return v
    
    @field_validator('awards')
    @classmethod
    def validate_awards(cls, v):
        if len(v) > 20:
            raise ValueError("Too many awards (max 20)")
        return v
    
    @field_validator('languages')
    @classmethod
    def validate_languages(cls, v):
        if len(v) > 10:
            raise ValueError("Too many languages (max 10)")
        for lang in v:
            if len(lang) > 100:
                raise ValueError("Language entry too long (max 100 characters)")
        return v
    
    @field_validator('interests')
    @classmethod
    def validate_interests(cls, v):
        if len(v) > 15:
            raise ValueError("Too many interests (max 15)")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Shreyansh",
                "title": "Full Stack Developer",
                "summary": "Experienced developer with expertise in AI and web technologies",
                "contact": {
                    "email": "shreyansh@example.com",
                    "github": "https://github.com/shreyansh"
                },
                "experience": [],
                "education": [],
                "skills": [],
                "projects": [],
                "certifications": [],
                "languages": ["English", "Hindi"]
            }
        }
    )


class ChatMessage(BaseModel):
    """Model for chat messages."""
    message: str = Field(..., min_length=1, max_length=500, description="User message")
    
    @field_validator('message')
    @classmethod
    def validate_message(cls, v):
        # Basic prompt injection detection
        dangerous_patterns = [
            "ignore previous",
            "ignore all previous",
            "disregard",
            "forget everything",
            "new instructions",
            "system:",
            "assistant:",
            "you are now",
            "act as",
            "pretend to be",
            "roleplay"
        ]
        
        v_lower = v.lower()
        for pattern in dangerous_patterns:
            if pattern in v_lower:
                raise ValueError("Message contains potentially unsafe content")
        
        return v.strip()
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Tell me about your experience"
            }
        }
    )


class ChatResponse(BaseModel):
    """Model for chat responses."""
    response: str = Field(..., description="AI generated response")
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "response": "I have experience in software development..."
            }
        }
    )
