"""
Comprehensive tests for PDF Resume Parser.

Tests cover:
- PDF text extraction (pdfplumber and PyPDF2 fallback)
- LLM-based parsing for all resume sections
- Error handling and fallback logic
- Regex-based extraction
- Integration testing
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock, mock_open
import httpx
from typing import List
from app.services.pdf_parser import PDFResumeParser, get_pdf_parser
from app.models.schemas import (
    Resume, ContactInfo, Experience, Education, Skill, Project, SkillCategory
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def pdf_parser():
    """Create a fresh PDF parser instance."""
    return PDFResumeParser()


@pytest.fixture
def sample_resume_text():
    """Sample resume text for testing."""
    return """
John Doe
Senior Software Engineer
john.doe@example.com | +1-555-0100 | linkedin.com/in/johndoe
San Francisco, CA

PROFESSIONAL SUMMARY
Experienced software engineer with 8+ years in full-stack development,
specializing in Python, AI/ML, and cloud technologies.

EXPERIENCE

Senior Software Engineer | TechCorp Inc. | San Francisco, CA
January 2020 - Present
- Led development of AI-powered recommendation system serving 1M+ users
- Reduced API response time by 40% through optimization
- Mentored team of 5 junior engineers
- Implemented CI/CD pipeline reducing deployment time by 60%

Software Engineer | StartupXYZ | New York, NY
June 2017 - December 2019
- Developed microservices architecture handling 100K requests/day
- Built RESTful APIs using Python and FastAPI
- Improved test coverage from 40% to 95%

EDUCATION

Bachelor of Technology in Computer Science | MIT | Cambridge, MA
September 2013 - May 2017
GPA: 3.8/4.0
Honors: Dean's List (4 semesters), Valedictorian

SKILLS
Programming: Python, JavaScript, Java, C++
Frameworks: FastAPI, Django, React, LangChain, PyTorch
Databases: PostgreSQL, MongoDB, Redis, FAISS
Tools: Docker, Kubernetes, Git, Azure, AWS
Soft Skills: Leadership, Communication, Problem Solving

PROJECTS

AI Resume Chatbot | Python, FastAPI, LangChain | 2024
- Built intelligent chatbot using multi-agent architecture
- Achieved 95% test coverage with comprehensive testing
- Deployed on Railway with CI/CD pipeline
- Technologies: Python, FastAPI, LangChain, Ollama, PostgreSQL

CERTIFICATIONS
- AWS Certified Solutions Architect
- Google Cloud Professional Data Engineer
- Microsoft Azure AI Engineer

LANGUAGES
- English (Native)
- Spanish (Professional)
- Mandarin (Conversational)

AWARDS
- Employee of the Year 2023
- Best Innovation Award 2022
"""


@pytest.fixture
def mock_pdf_page():
    """Mock PDF page object."""
    page = Mock()
    page.extract_text.return_value = "Sample page text content"
    return page


@pytest.fixture
def mock_ollama_response():
    """Mock successful Ollama API response."""
    def create_response(content: str):
        mock_resp = Mock()
        mock_resp.json.return_value = {"response": content}
        mock_resp.raise_for_status.return_value = None
        return mock_resp
    return create_response


# ============================================================================
# PDF TEXT EXTRACTION TESTS
# ============================================================================

class TestPDFTextExtraction:
    """Test PDF text extraction with both libraries."""
    
    @patch('app.services.pdf_parser.pdfplumber.open')
    def test_extract_text_pdfplumber_success(self, mock_pdfplumber, pdf_parser):
        """Test successful text extraction using pdfplumber."""
        # Setup mock
        mock_pdf = MagicMock()
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "Page 1 content"
        mock_page2 = Mock()
        mock_page2.extract_text.return_value = "Page 2 content"
        mock_pdf.pages = [mock_page1, mock_page2]
        mock_pdfplumber.return_value.__enter__.return_value = mock_pdf
        
        # Execute
        result = pdf_parser.extract_text_from_pdf("/fake/path.pdf")
        
        # Verify
        assert result == "Page 1 content\n\nPage 2 content"
        mock_pdfplumber.assert_called_once_with("/fake/path.pdf")
    
    @patch('app.services.pdf_parser.PdfReader')
    @patch('app.services.pdf_parser.pdfplumber.open')
    def test_extract_text_pypdf2_fallback(self, mock_pdfplumber, mock_pdfreader, pdf_parser):
        """Test fallback to PyPDF2 when pdfplumber fails."""
        # pdfplumber fails
        mock_pdfplumber.side_effect = Exception("pdfplumber error")
        
        # PyPDF2 succeeds
        mock_reader = Mock()
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "PyPDF2 page 1"
        mock_page2 = Mock()
        mock_page2.extract_text.return_value = "PyPDF2 page 2"
        mock_reader.pages = [mock_page1, mock_page2]
        mock_pdfreader.return_value = mock_reader
        
        # Execute
        result = pdf_parser.extract_text_from_pdf("/fake/path.pdf")
        
        # Verify
        assert result == "PyPDF2 page 1\n\nPyPDF2 page 2"
        mock_pdfreader.assert_called_once_with("/fake/path.pdf")
    
    @patch('app.services.pdf_parser.PdfReader')
    @patch('app.services.pdf_parser.pdfplumber.open')
    def test_extract_text_both_fail(self, mock_pdfplumber, mock_pdfreader, pdf_parser):
        """Test error when both extraction methods fail."""
        mock_pdfplumber.side_effect = Exception("pdfplumber error")
        mock_pdfreader.side_effect = Exception("PyPDF2 error")
        
        with pytest.raises(ValueError, match="Failed to extract text from PDF"):
            pdf_parser.extract_text_from_pdf("/fake/path.pdf")
    
    @patch('app.services.pdf_parser.pdfplumber.open')
    def test_extract_text_empty_pages(self, mock_pdfplumber, pdf_parser):
        """Test extraction with empty pages (None text)."""
        mock_pdf = MagicMock()
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "Content"
        mock_page2 = Mock()
        mock_page2.extract_text.return_value = None  # Empty page
        mock_page3 = Mock()
        mock_page3.extract_text.return_value = "More content"
        mock_pdf.pages = [mock_page1, mock_page2, mock_page3]
        mock_pdfplumber.return_value.__enter__.return_value = mock_pdf
        
        result = pdf_parser.extract_text_from_pdf("/fake/path.pdf")
        
        # Only non-None pages should be included
        assert result == "Content\n\nMore content"


# ============================================================================
# CONTACT INFO PARSING TESTS
# ============================================================================

class TestContactInfoParsing:
    """Test contact information extraction."""
    
    @pytest.mark.asyncio
    async def test_parse_contact_info_llm_success(self, pdf_parser, sample_resume_text):
        """Test successful contact info parsing via LLM."""
        llm_response = """{
            "email": "john.doe@example.com",
            "phone": "+1-555-0100",
            "location": "San Francisco, CA",
            "linkedin": "linkedin.com/in/johndoe",
            "github": "github.com/johndoe",
            "website": "johndoe.com"
        }"""
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {"response": llm_response}
            mock_response.raise_for_status = Mock()
            
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await pdf_parser.parse_contact_info(sample_resume_text)
            
            assert result.email == "john.doe@example.com"
            assert result.phone == "+1-555-0100"
            assert result.location == "San Francisco, CA"
            assert result.linkedin == "linkedin.com/in/johndoe"
    
    @pytest.mark.asyncio
    async def test_parse_contact_info_regex_fallback(self, pdf_parser):
        """Test regex fallback when LLM fails."""
        text = """
        Jane Smith
        jane.smith@company.com
        +1-555-9999
        linkedin.com/in/janesmith
        New York, NY
        """
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                side_effect=Exception("LLM failed")
            )
            
            result = await pdf_parser.parse_contact_info(text)
            
            # Should use regex extraction
            assert result.email == "jane.smith@company.com"
            assert result.phone == "+1-555-9999"
            assert result.linkedin == "linkedin.com/in/janesmith"
    
    @pytest.mark.asyncio
    async def test_parse_contact_info_malformed_json(self, pdf_parser, sample_resume_text):
        """Test handling of malformed JSON response."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {"response": "Not valid JSON {incomplete"}
            mock_response.raise_for_status = Mock()
            
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await pdf_parser.parse_contact_info(sample_resume_text)
            
            # Should fallback to defaults
            assert isinstance(result, ContactInfo)
            assert result.email == "john.doe@example.com"  # From regex


# ============================================================================
# EXPERIENCE PARSING TESTS
# ============================================================================

class TestExperienceParsing:
    """Test work experience extraction."""
    
    @pytest.mark.asyncio
    async def test_parse_experience_success(self, pdf_parser, sample_resume_text):
        """Test successful experience parsing."""
        llm_response = """[
            {
                "company": "TechCorp Inc.",
                "position": "Senior Software Engineer",
                "location": "San Francisco, CA",
                "start_date": "2020-01",
                "end_date": "Present",
                "description": "Leading AI/ML development",
                "achievements": [
                    "Led development of AI system",
                    "Reduced response time by 40%",
                    "Mentored 5 engineers"
                ]
            }
        ]"""
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {"response": llm_response}
            mock_response.raise_for_status = Mock()
            
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await pdf_parser.parse_experience(sample_resume_text)
            
            assert len(result) == 1
            assert result[0].company == "TechCorp Inc."
            assert result[0].position == "Senior Software Engineer"
            assert result[0].end_date == "Present"
            assert len(result[0].achievements) == 3
    
    @pytest.mark.asyncio
    async def test_parse_experience_string_achievements(self, pdf_parser, sample_resume_text):
        """Test handling of achievements as string instead of array."""
        llm_response = """[
            {
                "company": "Company A",
                "position": "Engineer",
                "location": "NYC",
                "start_date": "2020-01",
                "end_date": "2021-12",
                "description": "Software development",
                "achievements": "Built scalable systems"
            }
        ]"""
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {"response": llm_response}
            mock_response.raise_for_status = Mock()
            
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await pdf_parser.parse_experience(sample_resume_text)
            
            assert len(result) == 1
            assert isinstance(result[0].achievements, list)
            assert result[0].achievements[0] == "Built scalable systems"
    
    @pytest.mark.asyncio
    async def test_parse_experience_error_returns_empty(self, pdf_parser, sample_resume_text):
        """Test error handling returns empty list."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                side_effect=httpx.HTTPError("Connection error")
            )
            
            result = await pdf_parser.parse_experience(sample_resume_text)
            
            assert result == []


# ============================================================================
# EDUCATION PARSING TESTS
# ============================================================================

class TestEducationParsing:
    """Test education extraction."""
    
    @pytest.mark.asyncio
    async def test_parse_education_success(self, pdf_parser, sample_resume_text):
        """Test successful education parsing."""
        llm_response = """[
            {
                "institution": "MIT",
                "degree": "Bachelor of Technology",
                "field_of_study": "Computer Science",
                "location": "Cambridge, MA",
                "start_date": "2013-09",
                "end_date": "2017-05",
                "gpa": "3.8",
                "honors": ["Dean's List", "Valedictorian"]
            }
        ]"""
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {"response": llm_response}
            mock_response.raise_for_status = Mock()
            
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await pdf_parser.parse_education(sample_resume_text)
            
            assert len(result) == 1
            assert result[0].institution == "MIT"
            assert result[0].degree == "Bachelor of Technology"
            assert result[0].gpa == "3.8"
            assert len(result[0].honors) == 2
    
    @pytest.mark.asyncio
    async def test_parse_education_error_returns_empty(self, pdf_parser, sample_resume_text):
        """Test error handling returns empty list."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                side_effect=Exception("Parse error")
            )
            
            result = await pdf_parser.parse_education(sample_resume_text)
            
            assert result == []


# ============================================================================
# SKILLS PARSING TESTS
# ============================================================================

class TestSkillsParsing:
    """Test skills extraction and categorization."""
    
    @pytest.mark.asyncio
    async def test_parse_skills_success(self, pdf_parser, sample_resume_text):
        """Test successful skills parsing."""
        llm_response = """[
            {"name": "Python", "category": "Programming", "proficiency": "Expert"},
            {"name": "FastAPI", "category": "Frameworks & Libraries", "proficiency": "Advanced"},
            {"name": "PostgreSQL", "category": "Databases & Vector Stores", "proficiency": "Advanced"},
            {"name": "Docker", "category": "Cloud & DevOps", "proficiency": "Intermediate"}
        ]"""
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {"response": llm_response}
            mock_response.raise_for_status = Mock()
            
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await pdf_parser.parse_skills(sample_resume_text)
            
            assert len(result) == 4
            assert result[0].name == "Python"
            assert result[0].category == SkillCategory.PROGRAMMING
            assert result[1].category == SkillCategory.FRAMEWORKS
    
    @pytest.mark.asyncio
    async def test_parse_skills_invalid_category(self, pdf_parser, sample_resume_text):
        """Test handling of invalid skill category."""
        llm_response = """[
            {"name": "Python", "category": "INVALID_CATEGORY", "proficiency": "Expert"},
            {"name": "Java", "category": "Programming", "proficiency": "Advanced"}
        ]"""
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {"response": llm_response}
            mock_response.raise_for_status = Mock()
            
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await pdf_parser.parse_skills(sample_resume_text)
            
            # Invalid category should be converted to OTHER
            assert len(result) == 2
            assert result[0].category == SkillCategory.OTHER
            assert result[1].category == SkillCategory.PROGRAMMING
    
    @pytest.mark.asyncio
    async def test_parse_skills_error_returns_empty(self, pdf_parser, sample_resume_text):
        """Test error handling returns empty list."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                side_effect=httpx.HTTPError("Connection failed")
            )
            
            result = await pdf_parser.parse_skills(sample_resume_text)
            
            assert result == []


# ============================================================================
# PROJECTS PARSING TESTS
# ============================================================================

class TestProjectsParsing:
    """Test projects extraction."""
    
    @pytest.mark.asyncio
    async def test_parse_projects_success(self, pdf_parser, sample_resume_text):
        """Test successful projects parsing."""
        llm_response = """[
            {
                "name": "AI Resume Chatbot",
                "description": "Intelligent chatbot using multi-agent architecture",
                "technologies": ["Python", "FastAPI", "LangChain"],
                "url": "github.com/user/project",
                "start_date": "2024-01",
                "end_date": "2024-06",
                "highlights": [
                    "Achieved 95% test coverage",
                    "Deployed on Railway",
                    "Built multi-agent system"
                ]
            }
        ]"""
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {"response": llm_response}
            mock_response.raise_for_status = Mock()
            
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await pdf_parser.parse_projects(sample_resume_text)
            
            assert len(result) == 1
            assert result[0].name == "AI Resume Chatbot"
            assert len(result[0].technologies) == 3
            assert len(result[0].highlights) == 3
    
    @pytest.mark.asyncio
    async def test_parse_projects_error_returns_empty(self, pdf_parser, sample_resume_text):
        """Test error handling returns empty list."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                side_effect=Exception("Parse failed")
            )
            
            result = await pdf_parser.parse_projects(sample_resume_text)
            
            assert result == []


# ============================================================================
# SUMMARY PARSING TESTS
# ============================================================================

class TestSummaryParsing:
    """Test professional summary extraction."""
    
    @pytest.mark.asyncio
    async def test_parse_summary_success(self, pdf_parser, sample_resume_text):
        """Test successful summary parsing."""
        llm_response = "Experienced software engineer with 8+ years in full-stack development."
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {"response": llm_response}
            mock_response.raise_for_status = Mock()
            
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await pdf_parser.parse_summary(sample_resume_text)
            
            assert result == "Experienced software engineer with 8+ years in full-stack development."
    
    @pytest.mark.asyncio
    async def test_parse_summary_strips_meta_commentary(self, pdf_parser, sample_resume_text):
        """Test removal of meta-commentary from summary."""
        llm_response = "Here is the summary: Software engineer with expertise in AI/ML."
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {"response": llm_response}
            mock_response.raise_for_status = Mock()
            
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await pdf_parser.parse_summary(sample_resume_text)
            
            assert "Here is" not in result
            assert "Software engineer" in result
    
    @pytest.mark.asyncio
    async def test_parse_summary_error_returns_default(self, pdf_parser, sample_resume_text):
        """Test error handling returns default summary."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                side_effect=httpx.TimeoutException("Timeout")
            )
            
            result = await pdf_parser.parse_summary(sample_resume_text)
            
            assert result == "Experienced professional with expertise in AI/ML and software engineering."


# ============================================================================
# SIMPLE LIST EXTRACTION TESTS
# ============================================================================

class TestSimpleListExtraction:
    """Test extraction of certifications, languages, awards."""
    
    def test_extract_certifications(self, pdf_parser, sample_resume_text):
        """Test certification extraction."""
        result = pdf_parser.extract_simple_list(sample_resume_text, "CERTIFICATIONS?")
        
        assert len(result) > 0
        assert any("AWS" in cert for cert in result)
    
    def test_extract_languages(self, pdf_parser, sample_resume_text):
        """Test language extraction."""
        result = pdf_parser.extract_simple_list(sample_resume_text, "LANGUAGES?")
        
        assert len(result) > 0
        assert any("English" in lang for lang in result)
    
    def test_extract_awards(self, pdf_parser, sample_resume_text):
        """Test awards extraction."""
        # The regex pattern needs to match the actual section header
        result = pdf_parser.extract_simple_list(sample_resume_text, "AWARDS")
        
        # Awards section exists in sample text
        assert len(result) > 0
        # Check if any award contains expected keywords (case insensitive)
        result_text = ' '.join(result).lower()
        assert 'employee' in result_text or 'innovation' in result_text or 'award' in result_text
    
    def test_extract_simple_list_not_found(self, pdf_parser):
        """Test extraction when section doesn't exist."""
        text = "Some resume text without the section"
        result = pdf_parser.extract_simple_list(text, "NONEXISTENT")
        
        assert result == []
    
    def test_extract_simple_list_limits_to_10(self, pdf_parser):
        """Test that extraction limits to 10 items."""
        text = """
        CERTIFICATIONS:
        - Cert 1
        - Cert 2
        - Cert 3
        - Cert 4
        - Cert 5
        - Cert 6
        - Cert 7
        - Cert 8
        - Cert 9
        - Cert 10
        - Cert 11
        - Cert 12
        """
        result = pdf_parser.extract_simple_list(text, "CERTIFICATIONS")
        
        assert len(result) <= 10


# ============================================================================
# FULL RESUME PARSING TESTS
# ============================================================================

class TestFullResumeParsing:
    """Test complete resume parsing workflow."""
    
    @pytest.mark.asyncio
    @patch('app.services.pdf_parser.pdfplumber.open')
    async def test_parse_resume_success(self, mock_pdfplumber, pdf_parser, sample_resume_text):
        """Test successful full resume parsing."""
        # Mock PDF extraction
        mock_pdf = MagicMock()
        mock_page = Mock()
        mock_page.extract_text.return_value = sample_resume_text
        mock_pdf.pages = [mock_page]
        mock_pdfplumber.return_value.__enter__.return_value = mock_pdf
        
        # Mock all LLM calls
        with patch('httpx.AsyncClient') as mock_client:
            async def mock_post(url, json=None, **kwargs):
                prompt = json.get("prompt", "")
                
                if "contact information" in prompt.lower():
                    response = '{"email": "john.doe@example.com", "phone": "+1-555-0100", "location": "San Francisco, CA", "linkedin": "linkedin.com/in/johndoe", "github": "", "website": ""}'
                elif "summary" in prompt.lower():
                    response = "Experienced software engineer with 8+ years"
                elif "experience" in prompt.lower():
                    response = '[{"company": "TechCorp", "position": "Engineer", "location": "SF", "start_date": "2020-01", "end_date": "Present", "description": "Software development work", "achievements": ["Achievement 1"]}]'
                elif "education" in prompt.lower():
                    response = '[{"institution": "MIT", "degree": "BS", "field_of_study": "CS", "location": "Cambridge", "start_date": "2013-09", "end_date": "2017-05", "gpa": "3.8", "honors": []}]'
                elif "skills" in prompt.lower():
                    response = '[{"name": "Python", "category": "Programming", "proficiency": "Expert"}]'
                elif "projects" in prompt.lower():
                    response = '[{"name": "Project A", "description": "A great project", "technologies": ["Python"], "url": "", "start_date": "", "end_date": "", "highlights": ["Highlight 1"]}]'
                else:
                    response = "Default response"
                
                mock_resp = Mock()
                mock_resp.json.return_value = {"response": response}
                mock_resp.raise_for_status = Mock()
                return mock_resp
            
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(side_effect=mock_post)
            
            result = await pdf_parser.parse_resume("/fake/path.pdf")
            
            # Verify Resume structure - basic fields are extracted
            assert isinstance(result, Resume)
            assert result.name == "John Doe"
            assert result.title == "Senior Software Engineer"
            assert result.summary == "Experienced software engineer with 8+ years"
            # Contact info should be parsed
            assert result.contact.email == "john.doe@example.com"
            # Languages are extracted via regex from sample text
            assert len(result.languages) > 0
    
    @pytest.mark.asyncio
    @patch('app.services.pdf_parser.pdfplumber.open')
    async def test_parse_resume_insufficient_text(self, mock_pdfplumber, pdf_parser):
        """Test error when PDF has insufficient text."""
        mock_pdf = MagicMock()
        mock_page = Mock()
        mock_page.extract_text.return_value = "Short"
        mock_pdf.pages = [mock_page]
        mock_pdfplumber.return_value.__enter__.return_value = mock_pdf
        
        with pytest.raises(ValueError, match="Could not extract sufficient text from PDF"):
            await pdf_parser.parse_resume("/fake/path.pdf")
    
    @pytest.mark.asyncio
    @patch('app.services.pdf_parser.pdfplumber.open')
    async def test_parse_resume_with_optional_sections(self, mock_pdfplumber, pdf_parser, sample_resume_text):
        """Test resume parsing includes optional sections."""
        mock_pdf = MagicMock()
        mock_page = Mock()
        mock_page.extract_text.return_value = sample_resume_text
        mock_pdf.pages = [mock_page]
        mock_pdfplumber.return_value.__enter__.return_value = mock_pdf
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_resp = Mock()
            mock_resp.json.return_value = {"response": '{"email": "test@example.com", "phone": "+1-555-0000", "location": "City", "linkedin": "", "github": "", "website": ""}'}
            mock_resp.raise_for_status = Mock()
            
            # Create a mock that returns the same response for all calls
            async def mock_post(url, json=None, **kwargs):
                prompt = json.get("prompt", "")
                
                if "contact" in prompt.lower():
                    response = '{"email": "test@example.com", "phone": "+1-555-0000", "location": "City", "linkedin": "", "github": "", "website": ""}'
                elif "summary" in prompt.lower():
                    response = "Professional with experience"
                elif "experience" in prompt.lower():
                    response = '[]'
                elif "education" in prompt.lower():
                    response = '[]'
                elif "skills" in prompt.lower():
                    response = '[]'
                elif "projects" in prompt.lower():
                    response = '[]'
                else:
                    response = "Professional summary"
                
                mock_resp = Mock()
                mock_resp.json.return_value = {"response": response}
                mock_resp.raise_for_status = Mock()
                return mock_resp
            
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(side_effect=mock_post)
            
            result = await pdf_parser.parse_resume("/fake/path.pdf")
            
            # Optional sections should be present (lists not None)
            assert isinstance(result.certifications, list)
            assert isinstance(result.languages, list)
            # Languages should be extracted from sample text
            assert len(result.languages) > 0


# ============================================================================
# SINGLETON PATTERN TESTS
# ============================================================================

class TestSingletonPattern:
    """Test singleton pattern for PDF parser."""
    
    def test_get_pdf_parser_returns_singleton(self):
        """Test that get_pdf_parser returns same instance."""
        parser1 = get_pdf_parser()
        parser2 = get_pdf_parser()
        
        assert parser1 is parser2
    
    def test_get_pdf_parser_creates_instance(self):
        """Test that get_pdf_parser creates instance if needed."""
        import app.services.pdf_parser as parser_module
        
        # Reset singleton
        parser_module._parser_instance = None
        
        parser = get_pdf_parser()
        
        assert parser is not None
        assert isinstance(parser, PDFResumeParser)


# ============================================================================
# HTTP ERROR HANDLING TESTS
# ============================================================================

class TestHTTPErrorHandling:
    """Test HTTP error scenarios."""
    
    @pytest.mark.asyncio
    async def test_http_timeout_in_contact_parsing(self, pdf_parser, sample_resume_text):
        """Test timeout handling in contact info parsing."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                side_effect=httpx.TimeoutException("Request timeout")
            )
            
            result = await pdf_parser.parse_contact_info(sample_resume_text)
            
            # Should fallback to regex
            assert isinstance(result, ContactInfo)
            assert result.email == "john.doe@example.com"
    
    @pytest.mark.asyncio
    async def test_http_status_error_in_experience(self, pdf_parser, sample_resume_text):
        """Test HTTP status error handling in experience parsing."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "500 Server Error", request=Mock(), response=Mock()
            )
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await pdf_parser.parse_experience(sample_resume_text)
            
            # Should return empty list
            assert result == []
    
    @pytest.mark.asyncio
    async def test_json_decode_error_in_skills(self, pdf_parser, sample_resume_text):
        """Test JSON decode error handling in skills parsing."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {"response": "Not [ valid JSON"}
            mock_response.raise_for_status = Mock()
            
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await pdf_parser.parse_skills(sample_resume_text)
            
            assert result == []


# ============================================================================
# EDGE CASES AND ROBUSTNESS TESTS
# ============================================================================

class TestEdgeCases:
    """Test edge cases and robustness."""
    
    @pytest.mark.asyncio
    async def test_empty_achievements_array(self, pdf_parser, sample_resume_text):
        """Test handling of empty achievements array."""
        llm_response = '[{"company": "A", "position": "B", "location": "C", "start_date": "2020-01", "end_date": "2021-12", "description": "Software development work with various technologies", "achievements": []}]'
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {"response": llm_response}
            mock_response.raise_for_status = Mock()
            
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await pdf_parser.parse_experience(sample_resume_text)
            
            assert len(result) == 1
            assert result[0].achievements == []
    
    @pytest.mark.asyncio
    async def test_null_values_in_education(self, pdf_parser, sample_resume_text):
        """Test handling of null values in education."""
        llm_response = '[{"institution": "University", "degree": "BS", "field_of_study": "CS", "location": "City", "start_date": "2013-09", "end_date": "2017-05", "gpa": null, "honors": []}]'
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {"response": llm_response}
            mock_response.raise_for_status = Mock()
            
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await pdf_parser.parse_education(sample_resume_text)
            
            assert len(result) == 1
            assert result[0].gpa is None
            assert result[0].honors == []
    
    def test_extract_simple_list_filters_short_items(self, pdf_parser):
        """Test that simple list extraction filters out very short items."""
        text = """
        CERTIFICATIONS:
        - AWS Certified Solutions Architect
        - A
        - AB
        - ABC
        - Valid Certificate Name
        """
        result = pdf_parser.extract_simple_list(text, "CERTIFICATIONS")
        
        # Should filter out items with <= 3 characters
        assert all(len(item) > 3 for item in result)
    
    @pytest.mark.asyncio
    async def test_multiple_json_objects_in_response(self, pdf_parser, sample_resume_text):
        """Test extraction when response contains multiple JSON objects."""
        llm_response = 'Here is the data: {"email": "john@example.com", "phone": "+1-555-0100", "location": "SF", "linkedin": "", "github": "", "website": ""} and more text'
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {"response": llm_response}
            mock_response.raise_for_status = Mock()
            
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await pdf_parser.parse_contact_info(sample_resume_text)
            
            # Should extract first JSON object
            assert result.email == "john@example.com"
