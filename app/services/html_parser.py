"""
HTML Parser Service for extracting resume context from static HTML.

This service prioritizes HTML content over structured resume data,
ensuring the chatbot answers questions based on the actual website content.
"""

from pathlib import Path
from bs4 import BeautifulSoup
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class HTMLResumeParser:
    """Parse and extract resume information from HTML file."""
    
    def __init__(self, html_path: str = "static/index.html"):
        """Initialize parser with path to HTML file."""
        self.html_path = Path(html_path)
        self.soup = None
        self._load_html()
    
    def _load_html(self):
        """Load and parse HTML file."""
        try:
            with open(self.html_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.soup = BeautifulSoup(content, 'html.parser')
                logger.info(f"Successfully loaded HTML from {self.html_path}")
        except Exception as e:
            logger.error(f"Failed to load HTML: {e}")
            self.soup = None
    
    def get_full_context(self) -> str:
        """
        Extract complete resume context from HTML.
        This is the PRIMARY source for chatbot responses.
        
        Prioritizes static data section if available, otherwise falls back to dynamic sections.
        """
        if not self.soup:
            return ""
        
        sections = []
        
        # PRIORITY: Check for static resume data section (pre-rendered for parsing)
        static_data = self.soup.find('div', id='resume-static-data')
        if static_data:
            # Extract text from static data section
            intro = static_data.find('div', id='static-intro')
            if intro:
                sections.append(f"=== INTRODUCTION ===\n{intro.get_text(strip=False)}")
            
            experience = static_data.find('div', id='static-experience')
            if experience:
                sections.append(f"\n=== PROFESSIONAL EXPERIENCE ===\n{experience.get_text(strip=False)}")
            
            education = static_data.find('div', id='static-education')
            if education:
                sections.append(f"\n=== EDUCATION ===\n{education.get_text(strip=False)}")
            
            skills = static_data.find('div', id='static-skills')
            if skills:
                sections.append(f"\n=== SKILLS ===\n{skills.get_text(strip=False)}")
            
            projects = static_data.find('div', id='static-projects')
            if projects:
                sections.append(f"\n=== PROJECTS ===\n{projects.get_text(strip=False)}")
            
            certs = static_data.find('div', id='static-certifications')
            if certs:
                sections.append(f"\n=== CERTIFICATIONS ===\n{certs.get_text(strip=False)}")
            
            awards = static_data.find('div', id='static-awards')
            if awards:
                sections.append(f"\n=== AWARDS & RECOGNITION ===\n{awards.get_text(strip=False)}")
            
            interests = static_data.find('div', id='static-interests')
            if interests:
                sections.append(f"\n=== INTERESTS ===\n{interests.get_text(strip=False)}")
            
            if sections:
                return "\n".join(sections)
        
        # FALLBACK: Extract from dynamic sections (less reliable)
        # Extract header/intro
        intro = self._extract_intro()
        if intro:
            sections.append(f"=== INTRODUCTION ===\n{intro}")
        
        # Extract experience
        experience = self._extract_experience()
        if experience:
            sections.append(f"\n=== PROFESSIONAL EXPERIENCE ===\n{experience}")
        
        # Extract education
        education = self._extract_education()
        if education:
            sections.append(f"\n=== EDUCATION ===\n{education}")
        
        # Extract skills
        skills = self._extract_skills()
        if skills:
            sections.append(f"\n=== SKILLS ===\n{skills}")
        
        # Extract projects
        projects = self._extract_projects()
        if projects:
            sections.append(f"\n=== PROJECTS ===\n{projects}")
        
        # Extract certifications
        certifications = self._extract_certifications()
        if certifications:
            sections.append(f"\n=== CERTIFICATIONS ===\n{certifications}")
        
        # Extract awards
        awards = self._extract_awards()
        if awards:
            sections.append(f"\n=== AWARDS & RECOGNITION ===\n{awards}")
        
        # Extract interests
        interests = self._extract_interests()
        if interests:
            sections.append(f"\n=== INTERESTS ===\n{interests}")
        
        return "\n".join(sections)
    
    def _extract_intro(self) -> str:
        """Extract introduction section."""
        intro_parts = []
        
        # Get name from title
        title = self.soup.find('title')
        if title:
            intro_parts.append(title.get_text().strip())
        
        # Get intro text
        intro_section = self.soup.find('div', id='intro')
        if intro_section:
            # Get the main description
            intro_text = intro_section.find('p')
            if intro_text:
                intro_parts.append(intro_text.get_text().strip())
        
        return "\n".join(intro_parts)
    
    def _extract_experience(self) -> str:
        """Extract work experience section."""
        experience_list = []
        
        # Find experience section by id
        exp_section = self.soup.find('section', id='experience')
        if not exp_section:
            return ""
        
        # Find all job entries (they should be rendered by JavaScript)
        # For server-side rendering, look for the structure
        jobs_container = exp_section.find('div', id='experience-list')
        if jobs_container:
            # Look for job article elements
            for job in jobs_container.find_all('article', class_='job'):
                job_info = []
                
                title = job.find('h3')
                if title:
                    job_info.append(f"Position: {title.get_text().strip()}")
                
                company = job.find('h4')
                if company:
                    job_info.append(f"Company: {company.get_text().strip()}")
                
                dates = job.find('p', class_='dates')
                if dates:
                    job_info.append(f"Duration: {dates.get_text().strip()}")
                
                # Get description list
                desc_list = job.find('ul')
                if desc_list:
                    responsibilities = [li.get_text().strip() for li in desc_list.find_all('li')]
                    if responsibilities:
                        job_info.append("Responsibilities:")
                        job_info.extend([f"  - {resp}" for resp in responsibilities])
                
                if job_info:
                    experience_list.append("\n".join(job_info))
        
        return "\n\n".join(experience_list) if experience_list else ""
    
    def _extract_education(self) -> str:
        """Extract education section."""
        education_parts = []
        
        edu_section = self.soup.find('section', id='education')
        if edu_section:
            edu_container = edu_section.find('div', id='education-list')
            if edu_container:
                for edu in edu_container.find_all('div', class_='education-item'):
                    edu_info = []
                    
                    degree = edu.find('h3')
                    if degree:
                        edu_info.append(degree.get_text().strip())
                    
                    institution = edu.find('h4')
                    if institution:
                        edu_info.append(institution.get_text().strip())
                    
                    dates = edu.find('p', class_='dates')
                    if dates:
                        edu_info.append(dates.get_text().strip())
                    
                    if edu_info:
                        education_parts.append(" | ".join(edu_info))
        
        return "\n".join(education_parts) if education_parts else ""
    
    def _extract_skills(self) -> str:
        """Extract skills section."""
        skills_by_category = {}
        
        skills_section = self.soup.find('section', id='skills')
        if skills_section:
            categories = skills_section.find_all('div', class_='skill-category')
            for category in categories:
                cat_name = category.find('h3')
                if cat_name:
                    cat_name_text = cat_name.get_text().strip()
                    
                    skills_list = []
                    skill_items = category.find_all('span', class_='skill-item')
                    for skill in skill_items:
                        skill_text = skill.get_text().strip()
                        # Extract proficiency if available
                        proficiency_span = skill.find('span', class_='proficiency')
                        if proficiency_span:
                            skill_text = skill_text.replace(proficiency_span.get_text(), '').strip()
                        skills_list.append(skill_text)
                    
                    if skills_list:
                        skills_by_category[cat_name_text] = skills_list
        
        # Format skills by category
        formatted_skills = []
        for category, skills in skills_by_category.items():
            formatted_skills.append(f"{category}:")
            formatted_skills.append(", ".join(skills))
            formatted_skills.append("")
        
        return "\n".join(formatted_skills)
    
    def _extract_projects(self) -> str:
        """Extract projects section."""
        projects_list = []
        
        projects_section = self.soup.find('section', id='projects')
        if projects_section:
            project_items = projects_section.find_all('article', class_='project')
            for project in project_items:
                project_info = []
                
                name = project.find('h3')
                if name:
                    project_info.append(f"Project: {name.get_text().strip()}")
                
                desc = project.find('p', class_='description')
                if desc:
                    project_info.append(f"Description: {desc.get_text().strip()}")
                
                tech = project.find('p', class_='technologies')
                if tech:
                    project_info.append(f"Technologies: {tech.get_text().strip()}")
                
                if project_info:
                    projects_list.append("\n".join(project_info))
        
        return "\n\n".join(projects_list) if projects_list else ""
    
    def _extract_certifications(self) -> str:
        """Extract certifications section."""
        cert_list = []
        
        cert_section = self.soup.find('section', id='certifications')
        if cert_section:
            certs = cert_section.find_all('div', class_='cert-card')
            for cert in certs:
                cert_info = []
                
                name = cert.find('h4')
                if name:
                    cert_info.append(name.get_text().strip())
                
                issuer = cert.find('p', class_='cert-issuer')
                if issuer:
                    cert_info.append(f"Issuer: {issuer.get_text().strip()}")
                
                date = cert.find('p', class_='cert-date')
                if date:
                    cert_info.append(f"Date: {date.get_text().strip()}")
                
                if cert_info:
                    cert_list.append(" | ".join(cert_info))
        
        return "\n".join(cert_list) if cert_list else ""
    
    def _extract_awards(self) -> str:
        """Extract awards section."""
        awards_list = []
        
        awards_section = self.soup.find('section', id='awards')
        if awards_section:
            award_items = awards_section.find_all('div', class_='award-card')
            for award in award_items:
                award_info = []
                
                title = award.find('h4')
                if title:
                    award_info.append(title.get_text().strip())
                
                issuer = award.find('p', class_='award-issuer')
                if issuer:
                    award_info.append(f"Issuer: {issuer.get_text().strip()}")
                
                date = award.find('p', class_='award-date')
                if date:
                    award_info.append(f"Date: {date.get_text().strip()}")
                
                desc = award.find('p', class_='award-description')
                if desc:
                    award_info.append(f"Description: {desc.get_text().strip()}")
                
                if award_info:
                    awards_list.append("\n".join(award_info))
        
        return "\n\n".join(awards_list) if awards_list else ""
    
    def _extract_interests(self) -> str:
        """Extract interests section."""
        interests_list = []
        
        interests_section = self.soup.find('section', id='interests')
        if interests_section:
            interest_items = interests_section.find_all('div', class_='interest-card')
            for interest in interest_items:
                name = interest.find('h4')
                desc = interest.find('p')
                
                if name:
                    interest_text = name.get_text().strip()
                    if desc:
                        interest_text += f": {desc.get_text().strip()}"
                    interests_list.append(interest_text)
        
        return "\n".join(interests_list) if interests_list else ""


# Global instance
_html_parser = None


def get_html_context() -> str:
    """
    Get resume context from HTML file.
    This is the PRIMARY source for chatbot responses.
    """
    global _html_parser
    
    if _html_parser is None:
        _html_parser = HTMLResumeParser()
    
    return _html_parser.get_full_context()


def reload_html_context():
    """Reload HTML context (useful after updates)."""
    global _html_parser
    _html_parser = HTMLResumeParser()
