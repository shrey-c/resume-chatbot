import pytest
from app.services.resume_data import get_resume_data, get_resume_context
from app.models import Resume


class TestResumeData:
    """Tests for resume data functions."""
    
    def test_get_resume_data_returns_valid_resume(self):
        """Test that get_resume_data returns a valid Resume object."""
        resume = get_resume_data()
        
        assert isinstance(resume, Resume)
        assert len(resume.name) > 0
        assert len(resume.title) > 0
        assert len(resume.summary) > 0
    
    def test_resume_data_structure(self):
        """Test that resume data has expected structure."""
        resume = get_resume_data()
        
        # Check required fields
        assert hasattr(resume, 'name')
        assert hasattr(resume, 'title')
        assert hasattr(resume, 'summary')
        assert hasattr(resume, 'contact')
        assert hasattr(resume, 'experience')
        assert hasattr(resume, 'education')
        assert hasattr(resume, 'skills')
        assert hasattr(resume, 'projects')
    
    def test_resume_contact_info(self):
        """Test that contact information is present."""
        resume = get_resume_data()
        
        assert resume.contact is not None
        # At least one contact method should be present
        has_contact = any([
            resume.contact.email,
            resume.contact.phone,
            resume.contact.linkedin,
            resume.contact.github
        ])
        assert has_contact
    
    def test_get_resume_context_returns_string(self):
        """Test that get_resume_context returns a formatted string."""
        context = get_resume_context()
        
        assert isinstance(context, str)
        assert len(context) > 0
    
    def test_resume_context_contains_key_info(self):
        """Test that resume context contains key information."""
        context = get_resume_context()
        resume = get_resume_data()
        
        # Should contain name and title
        assert resume.name in context
        assert resume.title in context
        
        # Should contain section headers
        assert "Summary" in context or "summary" in context.lower()
    
    def test_resume_context_includes_experience(self):
        """Test that context includes experience if present."""
        resume = get_resume_data()
        context = get_resume_context()
        
        if resume.experience and len(resume.experience) > 0:
            assert "Experience" in context or "experience" in context.lower()
            # Should include company name
            assert resume.experience[0].company in context
    
    def test_resume_context_includes_education(self):
        """Test that context includes education if present."""
        resume = get_resume_data()
        context = get_resume_context()
        
        if resume.education and len(resume.education) > 0:
            assert "Education" in context or "education" in context.lower()
            # Should include institution name
            assert resume.education[0].institution in context
    
    def test_resume_context_includes_skills(self):
        """Test that context includes skills if present."""
        resume = get_resume_data()
        context = get_resume_context()
        
        if resume.skills and len(resume.skills) > 0:
            assert "Skills" in context or "skills" in context.lower()
            # Should include at least one skill name
            assert resume.skills[0].name in context
    
    def test_resume_context_includes_projects(self):
        """Test that context includes projects if present."""
        resume = get_resume_data()
        context = get_resume_context()
        
        if resume.projects and len(resume.projects) > 0:
            assert "Projects" in context or "projects" in context.lower()
            # Should include project name
            assert resume.projects[0].name in context
    
    def test_resume_context_length_reasonable(self):
        """Test that resume context length is reasonable for AI processing."""
        context = get_resume_context()
        
        # Context should be substantial but not too long
        assert len(context) > 100  # At least some content
        assert len(context) < 50000  # Not excessively long
    
    def test_resume_validation_passes(self):
        """Test that resume data passes Pydantic validation."""
        # This will raise ValidationError if invalid
        resume = get_resume_data()
        
        # Verify it's a valid Pydantic model
        assert resume.model_dump() is not None
        assert isinstance(resume.model_dump(), dict)
    
    def test_resume_data_no_sensitive_defaults(self):
        """Test that resume doesn't contain placeholder sensitive data."""
        resume = get_resume_data()
        
        # Check that it's been customized (not all defaults)
        # This is a soft check to reminder users to update the data
        if resume.contact.email:
            # Email should exist and be valid
            assert "@" in resume.contact.email
            assert "." in resume.contact.email
    
    def test_experience_has_descriptions(self):
        """Test that experiences have descriptions."""
        resume = get_resume_data()
        
        for exp in resume.experience:
            assert len(exp.description) >= 10  # Meaningful description
    
    def test_education_has_required_fields(self):
        """Test that education entries have required fields."""
        resume = get_resume_data()
        
        for edu in resume.education:
            assert len(edu.institution) > 0
            assert len(edu.degree) > 0
            assert len(edu.field_of_study) > 0
    
    def test_projects_have_technologies(self):
        """Test that projects list technologies."""
        resume = get_resume_data()
        
        for proj in resume.projects:
            assert len(proj.technologies) > 0  # At least one technology
    
    def test_skills_have_categories(self):
        """Test that skills are properly categorized."""
        resume = get_resume_data()
        
        for skill in resume.skills:
            assert skill.category is not None
            assert len(skill.name) > 0
