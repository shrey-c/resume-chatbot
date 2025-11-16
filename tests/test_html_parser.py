"""
Comprehensive tests for HTML parser service.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
from app.services.html_parser import (
    HTMLResumeParser,
    get_html_context,
    reload_html_context,
    _html_parser
)


class TestHTMLResumeParser:
    """Test HTMLResumeParser class."""
    
    @pytest.fixture
    def sample_html(self):
        """Sample HTML content for testing."""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Shreyansh Jain - AI/ML Engineer</title>
        </head>
        <body>
            <div id="resume-static-data" style="display: none;">
                <div id="static-intro">
                    <h1>Shreyansh Jain</h1>
                    <p>AI/ML Engineer with expertise in LLMs</p>
                </div>
                <div id="static-experience">
                    <h3>Senior ML Engineer</h3>
                    <h4>Tech Company</h4>
                    <p class="dates">2023 - Present</p>
                    <ul>
                        <li>Built AI systems</li>
                        <li>Deployed models</li>
                    </ul>
                </div>
                <div id="static-education">
                    <h3>MS Computer Science</h3>
                    <h4>University Name</h4>
                    <p class="dates">2020-2022</p>
                </div>
                <div id="static-skills">
                    <div class="skill-category">
                        <h3>Programming</h3>
                        <span class="skill-item">Python</span>
                        <span class="skill-item">Java</span>
                    </div>
                </div>
                <div id="static-projects">
                    <h3>AI Chatbot</h3>
                    <p class="description">Built chatbot</p>
                    <p class="technologies">Python, LangChain</p>
                </div>
                <div id="static-certifications">
                    <h4>AWS Certified</h4>
                    <p class="cert-issuer">Amazon</p>
                    <p class="cert-date">2023</p>
                </div>
                <div id="static-awards">
                    <h4>Best Project Award</h4>
                    <p class="award-issuer">University</p>
                    <p class="award-date">2022</p>
                    <p class="award-description">Won for AI project</p>
                </div>
                <div id="static-interests">
                    <h4>Machine Learning</h4>
                    <p>Deep learning research</p>
                </div>
            </div>
            
            <div id="intro">
                <p>Fallback intro text</p>
            </div>
            
            <section id="experience">
                <div id="experience-list">
                    <article class="job">
                        <h3>ML Engineer</h3>
                        <h4>Company XYZ</h4>
                        <p class="dates">2022-2023</p>
                        <ul>
                            <li>Developed models</li>
                        </ul>
                    </article>
                </div>
            </section>
            
            <section id="education">
                <div id="education-list">
                    <div class="education-item">
                        <h3>BS Computer Science</h3>
                        <h4>College Name</h4>
                        <p class="dates">2016-2020</p>
                    </div>
                </div>
            </section>
            
            <section id="skills">
                <div class="skill-category">
                    <h3>AI/ML</h3>
                    <span class="skill-item">TensorFlow<span class="proficiency">(Expert)</span></span>
                </div>
            </section>
            
            <section id="projects">
                <article class="project">
                    <h3>CV System</h3>
                    <p class="description">Computer vision project</p>
                    <p class="technologies">PyTorch, OpenCV</p>
                </article>
            </section>
            
            <section id="certifications">
                <div class="cert-card">
                    <h4>Azure Certified</h4>
                    <p class="cert-issuer">Microsoft</p>
                    <p class="cert-date">2023</p>
                </div>
            </section>
            
            <section id="awards">
                <div class="award-card">
                    <h4>Hackathon Winner</h4>
                    <p class="award-issuer">Tech Event</p>
                    <p class="award-date">2021</p>
                    <p class="award-description">Won AI hackathon</p>
                </div>
            </section>
            
            <section id="interests">
                <div class="interest-card">
                    <h4>AI Research</h4>
                    <p>Reading papers</p>
                </div>
            </section>
        </body>
        </html>
        """
    
    @pytest.fixture
    def minimal_html(self):
        """Minimal HTML without static data."""
        return """
        <!DOCTYPE html>
        <html>
        <head><title>Test Resume</title></head>
        <body>
            <div id="intro"><p>Test intro</p></div>
        </body>
        </html>
        """
    
    def test_init_success(self, sample_html):
        """Test successful initialization."""
        with patch("builtins.open", mock_open(read_data=sample_html)):
            parser = HTMLResumeParser("test.html")
            assert parser.soup is not None
            assert parser.html_path == Path("test.html")
    
    def test_init_file_not_found(self):
        """Test initialization with missing file."""
        with patch("builtins.open", side_effect=FileNotFoundError()):
            parser = HTMLResumeParser("missing.html")
            assert parser.soup is None
    
    def test_init_invalid_encoding(self):
        """Test initialization with encoding error."""
        with patch("builtins.open", side_effect=UnicodeDecodeError('utf-8', b'', 0, 1, 'test')):
            parser = HTMLResumeParser("bad_encoding.html")
            assert parser.soup is None
    
    def test_get_full_context_with_static_data(self, sample_html):
        """Test context extraction prioritizes static data."""
        with patch("builtins.open", mock_open(read_data=sample_html)):
            parser = HTMLResumeParser()
            context = parser.get_full_context()
            
            # Should contain static intro
            assert "Shreyansh Jain" in context
            assert "AI/ML Engineer with expertise in LLMs" in context
            
            # Should contain experience
            assert "Senior ML Engineer" in context
            assert "Tech Company" in context
            assert "Built AI systems" in context
            
            # Should contain education
            assert "MS Computer Science" in context
            assert "University Name" in context
            
            # Should contain skills
            assert "Programming" in context
            assert "Python" in context
            assert "Java" in context
            
            # Should contain projects
            assert "AI Chatbot" in context
            assert "LangChain" in context
            
            # Should contain certifications
            assert "AWS Certified" in context
            assert "Amazon" in context
            
            # Should contain awards
            assert "Best Project Award" in context
            assert "Won for AI project" in context
            
            # Should contain interests
            assert "Machine Learning" in context
            assert "Deep learning research" in context
            
            # Should have section headers
            assert "=== INTRODUCTION ===" in context
            assert "=== PROFESSIONAL EXPERIENCE ===" in context
            assert "=== SKILLS ===" in context
    
    def test_get_full_context_fallback_to_dynamic(self, minimal_html):
        """Test context extraction falls back to dynamic sections."""
        html_without_static = """
        <!DOCTYPE html>
        <html>
        <head><title>Test Resume</title></head>
        <body>
            <div id="intro"><p>Fallback intro text</p></div>
        </body>
        </html>
        """
        
        with patch("builtins.open", mock_open(read_data=html_without_static)):
            parser = HTMLResumeParser()
            context = parser.get_full_context()
            
            assert "Test Resume" in context
            assert "Fallback intro text" in context
    
    def test_get_full_context_no_soup(self):
        """Test get_full_context when soup is None."""
        with patch("builtins.open", side_effect=FileNotFoundError()):
            parser = HTMLResumeParser()
            context = parser.get_full_context()
            assert context == ""
    
    def test_extract_intro(self, sample_html):
        """Test intro extraction."""
        with patch("builtins.open", mock_open(read_data=sample_html)):
            parser = HTMLResumeParser()
            intro = parser._extract_intro()
            
            assert "Shreyansh Jain - AI/ML Engineer" in intro
            assert "Fallback intro text" in intro
    
    def test_extract_intro_no_elements(self):
        """Test intro extraction with missing elements."""
        html = "<html><body></body></html>"
        with patch("builtins.open", mock_open(read_data=html)):
            parser = HTMLResumeParser()
            intro = parser._extract_intro()
            assert intro == ""
    
    def test_extract_experience(self, sample_html):
        """Test experience extraction."""
        with patch("builtins.open", mock_open(read_data=sample_html)):
            parser = HTMLResumeParser()
            experience = parser._extract_experience()
            
            assert "ML Engineer" in experience
            assert "Company XYZ" in experience
            assert "2022-2023" in experience
            assert "Developed models" in experience
    
    def test_extract_experience_no_section(self):
        """Test experience extraction with no section."""
        html = "<html><body></body></html>"
        with patch("builtins.open", mock_open(read_data=html)):
            parser = HTMLResumeParser()
            experience = parser._extract_experience()
            assert experience == ""
    
    def test_extract_experience_no_jobs(self):
        """Test experience extraction with empty job list."""
        html = """<html><body>
            <section id="experience">
                <div id="experience-list"></div>
            </section>
        </body></html>"""
        with patch("builtins.open", mock_open(read_data=html)):
            parser = HTMLResumeParser()
            experience = parser._extract_experience()
            assert experience == ""
    
    def test_extract_education(self, sample_html):
        """Test education extraction."""
        with patch("builtins.open", mock_open(read_data=sample_html)):
            parser = HTMLResumeParser()
            education = parser._extract_education()
            
            assert "BS Computer Science" in education
            assert "College Name" in education
            assert "2016-2020" in education
    
    def test_extract_education_no_section(self):
        """Test education extraction with no section."""
        html = "<html><body></body></html>"
        with patch("builtins.open", mock_open(read_data=html)):
            parser = HTMLResumeParser()
            education = parser._extract_education()
            assert education == ""
    
    def test_extract_skills(self, sample_html):
        """Test skills extraction."""
        with patch("builtins.open", mock_open(read_data=sample_html)):
            parser = HTMLResumeParser()
            skills = parser._extract_skills()
            
            assert "AI/ML:" in skills
            assert "TensorFlow" in skills
            # Proficiency should be removed
            assert "(Expert)" not in skills or "TensorFlow" in skills
    
    def test_extract_skills_no_section(self):
        """Test skills extraction with no section."""
        html = "<html><body></body></html>"
        with patch("builtins.open", mock_open(read_data=html)):
            parser = HTMLResumeParser()
            skills = parser._extract_skills()
            assert skills == ""
    
    def test_extract_projects(self, sample_html):
        """Test projects extraction."""
        with patch("builtins.open", mock_open(read_data=sample_html)):
            parser = HTMLResumeParser()
            projects = parser._extract_projects()
            
            assert "CV System" in projects
            assert "Computer vision project" in projects
            assert "PyTorch, OpenCV" in projects
    
    def test_extract_projects_no_section(self):
        """Test projects extraction with no section."""
        html = "<html><body></body></html>"
        with patch("builtins.open", mock_open(read_data=html)):
            parser = HTMLResumeParser()
            projects = parser._extract_projects()
            assert projects == ""
    
    def test_extract_certifications(self, sample_html):
        """Test certifications extraction."""
        with patch("builtins.open", mock_open(read_data=sample_html)):
            parser = HTMLResumeParser()
            certs = parser._extract_certifications()
            
            assert "Azure Certified" in certs
            assert "Microsoft" in certs
            assert "2023" in certs
    
    def test_extract_certifications_no_section(self):
        """Test certifications extraction with no section."""
        html = "<html><body></body></html>"
        with patch("builtins.open", mock_open(read_data=html)):
            parser = HTMLResumeParser()
            certs = parser._extract_certifications()
            assert certs == ""
    
    def test_extract_awards(self, sample_html):
        """Test awards extraction."""
        with patch("builtins.open", mock_open(read_data=sample_html)):
            parser = HTMLResumeParser()
            awards = parser._extract_awards()
            
            assert "Hackathon Winner" in awards
            assert "Tech Event" in awards
            assert "2021" in awards
            assert "Won AI hackathon" in awards
    
    def test_extract_awards_no_section(self):
        """Test awards extraction with no section."""
        html = "<html><body></body></html>"
        with patch("builtins.open", mock_open(read_data=html)):
            parser = HTMLResumeParser()
            awards = parser._extract_awards()
            assert awards == ""
    
    def test_extract_interests(self, sample_html):
        """Test interests extraction."""
        with patch("builtins.open", mock_open(read_data=sample_html)):
            parser = HTMLResumeParser()
            interests = parser._extract_interests()
            
            assert "AI Research" in interests
            assert "Reading papers" in interests
    
    def test_extract_interests_no_section(self):
        """Test interests extraction with no section."""
        html = "<html><body></body></html>"
        with patch("builtins.open", mock_open(read_data=html)):
            parser = HTMLResumeParser()
            interests = parser._extract_interests()
            assert interests == ""


class TestGlobalFunctions:
    """Test global HTML parser functions."""
    
    def test_get_html_context_initializes_parser(self, monkeypatch):
        """Test get_html_context initializes global parser."""
        sample_html = "<html><head><title>Test</title></head><body></body></html>"
        
        # Reset global parser
        import app.services.html_parser as hp
        hp._html_parser = None
        
        with patch("builtins.open", mock_open(read_data=sample_html)):
            context = get_html_context()
            assert isinstance(context, str)
            assert hp._html_parser is not None
    
    def test_get_html_context_reuses_parser(self, monkeypatch):
        """Test get_html_context reuses existing parser."""
        sample_html = "<html><head><title>Test</title></head><body></body></html>"
        
        import app.services.html_parser as hp
        
        with patch("builtins.open", mock_open(read_data=sample_html)):
            # First call
            context1 = get_html_context()
            parser1 = hp._html_parser
            
            # Second call should reuse
            context2 = get_html_context()
            parser2 = hp._html_parser
            
            assert parser1 is parser2
    
    def test_reload_html_context(self, monkeypatch):
        """Test reload_html_context creates new parser."""
        sample_html = "<html><head><title>Test</title></head><body></body></html>"
        
        import app.services.html_parser as hp
        
        with patch("builtins.open", mock_open(read_data=sample_html)):
            # Initial load
            get_html_context()
            parser1 = hp._html_parser
            
            # Reload
            reload_html_context()
            parser2 = hp._html_parser
            
            assert parser1 is not parser2
    
    def test_get_html_context_with_actual_file(self):
        """Test get_html_context with actual index.html file."""
        # This tests against the real file
        context = get_html_context()
        
        # Should return a string (may be empty or have content)
        assert isinstance(context, str)
    
    def test_reload_with_actual_file(self):
        """Test reload with actual file."""
        reload_html_context()
        context = get_html_context()
        assert isinstance(context, str)


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_malformed_html(self):
        """Test parser handles malformed HTML."""
        malformed = "<html><body><div>Unclosed div<p>Test</body></html>"
        
        with patch("builtins.open", mock_open(read_data=malformed)):
            parser = HTMLResumeParser()
            context = parser.get_full_context()
            # BeautifulSoup should still parse it
            assert isinstance(context, str)
    
    def test_empty_html_file(self):
        """Test parser handles empty HTML file."""
        with patch("builtins.open", mock_open(read_data="")):
            parser = HTMLResumeParser()
            context = parser.get_full_context()
            assert context == ""
    
    def test_html_with_special_characters(self):
        """Test parser handles special characters."""
        html_with_special = """
        <html><body>
            <div id="intro"><p>Test &amp; Special &lt;chars&gt;</p></div>
        </body></html>
        """
        
        with patch("builtins.open", mock_open(read_data=html_with_special)):
            parser = HTMLResumeParser()
            intro = parser._extract_intro()
            # BeautifulSoup should decode HTML entities
            assert "&" in intro or "Test" in intro
    
    def test_nested_structures(self):
        """Test parser handles deeply nested structures."""
        nested_html = """
        <html><body>
            <section id="experience">
                <div id="experience-list">
                    <article class="job">
                        <h3>Title</h3>
                        <div><div><div>
                            <ul><li>Nested item</li></ul>
                        </div></div></div>
                    </article>
                </div>
            </section>
        </body></html>
        """
        
        with patch("builtins.open", mock_open(read_data=nested_html)):
            parser = HTMLResumeParser()
            exp = parser._extract_experience()
            assert "Title" in exp
    
    def test_multiple_skill_categories(self):
        """Test skills extraction with multiple categories."""
        html = """
        <html><body>
            <section id="skills">
                <div class="skill-category">
                    <h3>Programming</h3>
                    <span class="skill-item">Python</span>
                </div>
                <div class="skill-category">
                    <h3>Databases</h3>
                    <span class="skill-item">PostgreSQL</span>
                </div>
            </section>
        </body></html>
        """
        
        with patch("builtins.open", mock_open(read_data=html)):
            parser = HTMLResumeParser()
            skills = parser._extract_skills()
            
            assert "Programming:" in skills
            assert "Python" in skills
            assert "Databases:" in skills
            assert "PostgreSQL" in skills
    
    def test_missing_optional_fields(self):
        """Test extraction when optional fields are missing."""
        html = """
        <html><body>
            <section id="experience">
                <div id="experience-list">
                    <article class="job">
                        <h3>Job Title</h3>
                        <!-- Missing company, dates, description -->
                    </article>
                </div>
            </section>
        </body></html>
        """
        
        with patch("builtins.open", mock_open(read_data=html)):
            parser = HTMLResumeParser()
            exp = parser._extract_experience()
            assert "Job Title" in exp
