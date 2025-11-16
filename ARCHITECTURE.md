# Architecture Overview

## System Components

```
User Browser (HTML/CSS/JS)
       ↓
FastAPI Application (main.py)
       ↓
LangGraph Multi-Agent System
   • ResearchAgent - Extracts context from resume
   • ResponseAgent - Generates answers
   • ValidationAgent - Ensures quality
       ↓
Ollama LLM (llama3.2:1b)
```

## Request Flow

### Chat Request
```
1. User sends message → POST /api/chat
2. FastAPI validates input (Pydantic)
3. LangGraph agents process:
   - ResearchAgent: Parse HTML resume + extract relevant info
   - ResponseAgent: Generate answer using LLM
   - ValidationAgent: Check response quality
4. Return response to user
```

### Resume Display
```
1. User visits website → GET /
2. Browser loads static/index.html
3. Resume data displayed from embedded HTML
4. Chatbot ready for interaction
```

## Security Layers

1. **Rate Limiting** - 10 requests/minute per IP
2. **Input Validation** - Pydantic models enforce types/limits
3. **Prompt Injection Protection** - Pattern matching & sanitization
4. **JWT Authentication** - Secure admin portal access
5. **CORS** - Restricted origins
6. **XSS Prevention** - HTML escaping in frontend

## Technology Stack

**Frontend**
- HTML5 (Semantic markup)
- CSS3 (Professional template)
- Vanilla JavaScript (ES6+)

**Backend**
- Python 3.11+
- FastAPI (Web framework)
- Pydantic (Data validation)
- LangGraph (Multi-agent orchestration)
- LangChain (LLM integration)

**AI/ML**
- Ollama (Local LLM runtime)
- LLaMA 3.2 (Language model)
- BeautifulSoup4 (HTML parsing)

**Testing**
- pytest (Test framework)
- pytest-cov (Coverage: 96.88%)
- 247 tests passing

## File Structure

```
app/
├── core/
│   ├── auth.py          # JWT authentication
│   └── config.py        # Settings
├── models/
│   └── schemas.py       # Pydantic models
└── services/
    ├── agents.py        # LangGraph multi-agent system
    ├── html_parser.py   # HTML content extraction
    ├── ollama_service.py # LLM client
    ├── pdf_parser.py    # PDF resume extraction
    └── resume_data.py   # Resume data management

static/
├── index.html           # Main website
├── recruiters.html      # Recruiter-focused page
├── images/
│   └── shrey.jpg       # Personal photo
└── template-assets/    # CSS/JS/fonts

tests/                   # 247 tests, 96.88% coverage
main.py                  # FastAPI app entry point
```

## Data Flow

1. **User uploads PDF** (Admin Portal)
   → PDF Parser extracts data
   → Updates resume_data.py
   → Regenerates static HTML

2. **User visits website**
   → Loads index.html
   → Displays resume sections
   → Chatbot initialized

3. **User asks question**
   → LangGraph ResearchAgent parses HTML
   → ResponseAgent generates answer via Ollama
   → ValidationAgent checks quality
   → Response returned to user

## Deployment Architecture

**Local Development**
```
FastAPI :8000 + Ollama :11434
```

**Docker**
```
Container 1: FastAPI app
Container 2: Ollama service
Network: Docker network
```

**Production**
```
Cloud Platform (Railway/Render/DigitalOcean)
  → FastAPI app
  → Ollama instance or cloud LLM API
  → GitHub Pages (static files, optional)
```

## Test Coverage (96.88%)

| Module | Coverage |
|--------|----------|
| auth.py | 96.88% |
| config.py | 100% |
| schemas.py | 94.18% |
| agents.py | 94.12% |
| html_parser.py | 97.08% |
| ollama_service.py | 100% |
| resume_data.py | 95.40% |
| main.py | 98.25% |

---

This architecture provides:
- **Scalability**: Async FastAPI, horizontal scaling capable
- **Security**: 6 layers of validation and protection
- **Reliability**: High test coverage (96.88%)
- **Performance**: Local LLM inference, HTML parsing
- **Maintainability**: Clean separation of concerns
