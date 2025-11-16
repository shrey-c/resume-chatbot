"""
PDF Resume Parser using AI-powered extraction.

This module extracts resume information from PDF files and converts it
into structured Pydantic models. Uses LLM to intelligently parse sections.
"""

import re
from typing import Optional, List, Dict, Any
from datetime import datetime
import pdfplumber
from PyPDF2 import PdfReader
from app.models.schemas import (
    Resume, Experience, Education, Skill, Project,
    ContactInfo, SkillCategory
)
from app.core.config import settings
import httpx


class PDFResumeParser:
    """
    Intelligent PDF resume parser using LLM assistance.
    
    Extracts:
    - Contact information (name, email, phone, location, LinkedIn)
    - Professional summary
    - Work experience (with dates, descriptions, achievements)
    - Education (degrees, institutions, dates)
    - Skills (categorized)
    - Projects (with technologies and achievements)
    - Certifications
    - Languages
    - Awards/Honors
    """
    
    def __init__(self):
        self.ollama_base_url = settings.ollama_base_url
        self.ollama_model = settings.ollama_model
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract raw text from PDF file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text as string
        """
        text_parts = []
        
        try:
            # Try pdfplumber first (better formatting preservation)
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
        except Exception as e:
            print(f"pdfplumber failed: {e}, trying PyPDF2...")
            
            # Fallback to PyPDF2
            try:
                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
            except Exception as e2:
                raise ValueError(f"Failed to extract text from PDF: {e2}")
        
        return "\n\n".join(text_parts)
    
    async def parse_contact_info(self, text: str) -> ContactInfo:
        """Extract contact information using LLM."""
        
        prompt = f"""Extract contact information from this resume text. Return ONLY a JSON object with these exact fields:

{{"name": "Full Name", "email": "email@example.com", "phone": "+1234567890", "location": "City, Country", "linkedin": "linkedin.com/in/username", "github": "github.com/username", "website": ""}}

Resume text:
{text[:2000]}

Return ONLY the JSON object, no other text."""

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.ollama_base_url}/api/generate",
                    json={
                        "model": self.ollama_model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {"temperature": 0.1}
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                # Parse JSON from response
                import json
                json_text = result.get("response", "").strip()
                
                # Extract JSON object
                json_match = re.search(r'\{[^}]+\}', json_text, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group(0))
                    return ContactInfo(**data)
        except Exception as e:
            print(f"Error parsing contact info: {e}")
        
        # Fallback to regex extraction
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        phone_match = re.search(r'[\+\(]?[0-9][\d\s\-\(\)]{7,}', text)
        linkedin_match = re.search(r'linkedin\.com/in/[\w\-]+', text)
        
        return ContactInfo(
            name="Shreyansh Chheda",  # Default
            email=email_match.group(0) if email_match else "shreyansh.chheda@gmail.com",
            phone=phone_match.group(0).strip() if phone_match else "+91 9820477990",
            location="Pune, India",
            linkedin=linkedin_match.group(0) if linkedin_match else "linkedin.com/in/shreyansh-chheda",
            github="",
            website=""
        )
    
    async def parse_experience(self, text: str) -> List[Experience]:
        """Extract work experience using LLM."""
        
        prompt = f"""Extract ALL work experience entries from this resume. For EACH job, return a JSON object with:
- company: Company name
- position: Job title
- location: City, Country
- start_date: YYYY-MM format
- end_date: YYYY-MM or "Present"
- description: Brief description (1-2 sentences)
- achievements: Array of 3-5 specific achievements with metrics

Format as JSON array: [{{"company": "...", "position": "...", ...}}]

Resume text:
{text}

Return ONLY the JSON array, no other text."""

        try:
            async with httpx.AsyncClient(timeout=45.0) as client:
                response = await client.post(
                    f"{self.ollama_base_url}/api/generate",
                    json={
                        "model": self.ollama_model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {"temperature": 0.2}
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                import json
                json_text = result.get("response", "").strip()
                
                # Extract JSON array
                json_match = re.search(r'\[.*\]', json_text, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group(0))
                    experiences = []
                    for exp_data in data:
                        # Ensure achievements is a list
                        if isinstance(exp_data.get('achievements'), str):
                            exp_data['achievements'] = [exp_data['achievements']]
                        experiences.append(Experience(**exp_data))
                    return experiences
        except Exception as e:
            print(f"Error parsing experience: {e}")
        
        return []
    
    async def parse_education(self, text: str) -> List[Education]:
        """Extract education using LLM."""
        
        prompt = f"""Extract ALL education entries from this resume. For EACH degree, return a JSON object with:
- institution: University/College name
- degree: Degree type (e.g., "Bachelor of Technology")
- field_of_study: Major/Field (e.g., "Computer Science")
- location: City, Country
- start_date: YYYY-MM format
- end_date: YYYY-MM format
- gpa: GPA if mentioned, else null
- honors: Array of honors/awards, empty if none

Format as JSON array: [{{"institution": "...", "degree": "...", ...}}]

Resume text:
{text}

Return ONLY the JSON array, no other text."""

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.ollama_base_url}/api/generate",
                    json={
                        "model": self.ollama_model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {"temperature": 0.2}
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                import json
                json_text = result.get("response", "").strip()
                
                json_match = re.search(r'\[.*\]', json_text, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group(0))
                    return [Education(**edu_data) for edu_data in data]
        except Exception as e:
            print(f"Error parsing education: {e}")
        
        return []
    
    async def parse_skills(self, text: str) -> List[Skill]:
        """Extract and categorize skills using LLM."""
        
        prompt = f"""Extract ALL skills from this resume and categorize them. Return a JSON array of objects with:
- name: Skill name
- category: One of ["AI & Machine Learning", "Generative AI", "Programming", "Frameworks & Libraries", "Databases & Vector Stores", "Cloud & DevOps", "Tools & Platforms", "Soft Skills", "Other"]
- proficiency: One of ["Beginner", "Intermediate", "Advanced", "Expert"]

Categories:
- AI & Machine Learning: Machine Learning, Deep Learning, NLP, Neural Networks, XGBoost, etc.
- Generative AI: LLMs, GPT, RAG, LangChain, LangGraph, Prompt Engineering, etc.
- Programming: Python, Java, JavaScript, SQL, etc.
- Frameworks & Libraries: FastAPI, React, PyTorch, TensorFlow, Spring Boot, etc.
- Databases & Vector Stores: PostgreSQL, MongoDB, FAISS, ChromaDB, etc.
- Cloud & DevOps: Azure, AWS, Docker, Kubernetes, CI/CD, etc.
- Tools & Platforms: Git, PowerBI, VS Code, JIRA, etc.
- Soft Skills: Leadership, Communication, Problem Solving, etc.
- Other: Anything else

Format: [{{"name": "Python", "category": "Programming", "proficiency": "Expert"}}, ...]

Resume text:
{text}

Return ONLY the JSON array."""

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.ollama_base_url}/api/generate",
                    json={
                        "model": self.ollama_model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {"temperature": 0.3}
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                import json
                json_text = result.get("response", "").strip()
                
                json_match = re.search(r'\[.*\]', json_text, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group(0))
                    skills = []
                    for skill_data in data:
                        # Validate category
                        try:
                            skill_data['category'] = SkillCategory(skill_data['category'])
                            skills.append(Skill(**skill_data))
                        except ValueError:
                            skill_data['category'] = SkillCategory.OTHER
                            skills.append(Skill(**skill_data))
                    return skills
        except Exception as e:
            print(f"Error parsing skills: {e}")
        
        return []
    
    async def parse_projects(self, text: str) -> List[Project]:
        """Extract projects using LLM."""
        
        prompt = f"""Extract ALL projects from this resume. For EACH project, return a JSON object with:
- name: Project name
- description: 2-3 sentence description
- technologies: Array of technologies used
- url: Project URL or GitHub link (empty string if none)
- start_date: YYYY-MM format (empty if not mentioned)
- end_date: YYYY-MM format or empty for ongoing
- highlights: Array of 3-5 key achievements/impacts

Format as JSON array: [{{"name": "...", "description": "...", ...}}]

Resume text:
{text}

Return ONLY the JSON array."""

        try:
            async with httpx.AsyncClient(timeout=40.0) as client:
                response = await client.post(
                    f"{self.ollama_base_url}/api/generate",
                    json={
                        "model": self.ollama_model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {"temperature": 0.3}
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                import json
                json_text = result.get("response", "").strip()
                
                json_match = re.search(r'\[.*\]', json_text, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group(0))
                    return [Project(**proj_data) for proj_data in data]
        except Exception as e:
            print(f"Error parsing projects: {e}")
        
        return []
    
    async def parse_summary(self, text: str) -> str:
        """Extract professional summary using LLM."""
        
        prompt = f"""Extract the professional summary or objective from this resume. 
If there's a summary section, return it. If not, create a 2-3 sentence summary based on the resume content.

Resume text (first 1000 chars):
{text[:1000]}

Return ONLY the summary text, no additional commentary."""

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                response = await client.post(
                    f"{self.ollama_base_url}/api/generate",
                    json={
                        "model": self.ollama_model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {"temperature": 0.5}
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                summary = result.get("response", "").strip()
                # Clean up any meta-commentary
                summary = re.sub(r'^(Here is|Here\'s|Summary:)', '', summary, flags=re.IGNORECASE).strip()
                return summary
        except Exception as e:
            print(f"Error parsing summary: {e}")
            return "Experienced professional with expertise in AI/ML and software engineering."
    
    def extract_simple_list(self, text: str, section_name: str) -> List[str]:
        """Extract simple lists like certifications, languages, awards."""
        
        # Find section
        pattern = rf"{section_name}[:\s]+(.+?)(?=\n[A-Z][A-Z\s]+:|$)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        
        if not match:
            return []
        
        section_text = match.group(1)
        
        # Handle None case
        if not section_text:
            return []
        
        # Split by common delimiters
        items = re.split(r'\n[-•*]|\n\d+\.|\n', section_text)
        items = [item.strip() for item in items if item.strip() and len(item.strip()) > 3]
        
        return items[:10]  # Limit to 10 items
    
    async def parse_resume(self, pdf_path: str) -> Resume:
        """
        Main method to parse a PDF resume into a Resume object.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Resume object with all extracted information
        """
        
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        
        if not text or len(text) < 100:
            raise ValueError("Could not extract sufficient text from PDF")
        
        # Parse all sections in parallel-ish (async)
        contact = await self.parse_contact_info(text)
        summary = await self.parse_summary(text)
        experience = await self.parse_experience(text)
        education = await self.parse_education(text)
        skills = await self.parse_skills(text)
        projects = await self.parse_projects(text)
        
        # Extract simple lists
        certifications = self.extract_simple_list(text, "CERTIFICATIONS?|CERTIFICATES?")
        languages = self.extract_simple_list(text, "LANGUAGES?")
        
        # Extract name and title from first few lines
        lines = text.split('\n')
        name = "Shreyansh Chheda"  # Default fallback
        title = "Software Engineer"  # Default fallback
        
        # Try to extract name from first non-empty line
        for line in lines[:5]:
            line = line.strip()
            if line and len(line) > 3 and not '@' in line and not 'http' in line.lower():
                # Check if it looks like a name (2-4 words, each capitalized)
                words = line.split()
                if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w):
                    name = line
                    break
        
        # Try to extract title (usually second non-empty line or has keywords)
        title_keywords = ['engineer', 'developer', 'scientist', 'analyst', 'manager', 'designer', 'architect']
        for line in lines[:10]:
            line = line.strip()
            if line and any(keyword in line.lower() for keyword in title_keywords):
                title = line
                break
        
        # Build Resume object with correct field names
        resume = Resume(
            name=name,
            title=title,
            summary=summary,
            contact=contact,
            experience=experience,
            education=education,
            skills=skills,
            projects=projects,
            certifications=certifications if certifications else [],
            languages=languages if languages else []
        )
        
        return resume


# Singleton instance
_parser_instance: Optional[PDFResumeParser] = None


def get_pdf_parser() -> PDFResumeParser:
    """Get singleton PDF parser instance."""
    global _parser_instance
    if _parser_instance is None:
        _parser_instance = PDFResumeParser()
    return _parser_instance
