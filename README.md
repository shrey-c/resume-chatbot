# 🤖 AI-Powered Resume Chatbot

An intelligent, full-stack resume website with an AI chatbot assistant powered by LangGraph and Ollama LLM. Features a secure admin portal for PDF resume uploads, multi-agent architecture, and professional UI.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2.28-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🎯 Core Functionality
- **Professional Resume Website** - Responsive, modern UI showcasing experience, skills, and projects
- **AI Chatbot Assistant** - Interactive chatbot powered by LangGraph multi-agent system
- **Secure Admin Portal** - JWT-authenticated portal for uploading PDF resumes
- **AI PDF Parser** - Automatically extracts and updates resume data from PDFs
- **Multi-Agent System** - Research, Response, and Validation agents for accurate responses

### 🔒 Security
- **JWT Authentication** - Secure admin access with bcrypt password hashing
- **Prompt Injection Protection** - Validates and sanitizes all user inputs
- **Rate Limiting** - 10 requests/minute to prevent abuse
- **Input Validation** - Pydantic models with comprehensive validation
- **CORS Configuration** - Restricted origin access

### 🏗️ Architecture
- **Clean Architecture** - Modular codebase with separation of concerns
- **Type Safety** - Full type hints throughout the codebase
- **Comprehensive Logging** - Centralized logging with file and console output
- **RESTful API** - Well-documented FastAPI endpoints
- **Responsive Design** - Mobile-first, professional HTML5 UP template

## 🚀 Quick Start

### Prerequisites

```bash
- Python 3.11+
- Ollama (https://ollama.ai/)
- Git
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/shrey-c/resume-chatbot.git
cd resume-chatbot
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Install and start Ollama**
```bash
# Install Ollama from https://ollama.ai/
ollama pull llama3.2:1b  # or llama2, llama3
```

5. **Set up environment**
```bash
# Copy example env file
cp .env.example .env

# Edit .env and set your admin credentials
# To generate a password hash, run:
python -c "from app.core.auth import generate_password_hash; print(generate_password_hash('your-password'))"
# Default: username=admin, password=Shreyansh@2025
```

6. **Run the application**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

7. **Access the application**
```
Website: http://localhost:8000
Admin Portal: http://localhost:8000/admin
API Docs: http://localhost:8000/docs
```

## 📁 Project Structure

```
├── app/                     # Main application package
│   ├── api/                # API routes (modular structure)
│   ├── core/               # Core configuration and auth
│   │   ├── __init__.py
│   │   ├── config.py       # Settings and configuration
│   │   └── auth.py         # JWT authentication
│   ├── models/             # Data models and schemas
│   │   ├── __init__.py
│   │   └── schemas.py      # Pydantic models
│   ├── services/           # Business logic services
│   │   ├── __init__.py
│   │   ├── agents.py       # LangGraph multi-agent system
│   │   ├── ollama_service.py # Ollama LLM client
│   │   ├── pdf_parser.py   # AI PDF extraction
│   │   └── resume_data.py  # Resume data management
│   └── __init__.py
│
├── static/                  # Frontend files
│   ├── index.html          # Main website (HTML5 UP template)
│   ├── admin.html          # Admin portal
│   └── template-assets/    # CSS, JS, fonts from HTML5 UP
│
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_api.py         # API endpoint tests
│   ├── test_models.py      # Model validation tests
│   ├── test_ollama_service.py
│   └── test_resume_data.py
│
├── logs/                    # Application logs
├── uploads/                 # PDF uploads (gitignored)
│
├── main.py                  # FastAPI application entry point
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
├── .env                     # Environment variables (create from .env.example)
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── pytest.ini               # Pytest configuration
│
├── README.md                # This file
├── QUICKSTART.md            # Quick setup guide
├── ARCHITECTURE.md          # System architecture
├── CONTRIBUTING.md          # Contribution guidelines
└── DEPLOYMENT.md            # Deployment instructions
```

## 🎯 API Endpoints

### Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main resume website |
| GET | `/api/health` | Health check |
| GET | `/api/resume` | Get resume data (JSON) |
| POST | `/api/chat` | Chat with AI assistant |

### Admin Endpoints (JWT Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin` | Admin portal UI |
| POST | `/api/admin/login` | Admin login |
| POST | `/api/admin/upload-resume` | Upload PDF resume |
| GET | `/api/admin/verify` | Verify JWT token |

## 💬 Chat API Usage

```python
import requests

# Send a chat message
response = requests.post(
    "http://localhost:8000/api/chat",
    json={"message": "Tell me about your GenAI experience"}
)

print(response.json()["response"])
```

```bash
# Using curl
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What projects have you worked on?"}'
```

## 🔐 Admin Portal Usage

1. **Login**
   - Navigate to `http://localhost:8000/admin`
   - Use credentials from `.env` (default: admin / Shreyansh@2025)

2. **Upload Resume**
   - Drag and drop PDF file or click to browse
   - AI automatically extracts: name, experience, education, skills, projects
   - Data is updated in real-time

3. **Verify**
   - System validates extracted data
   - Review and confirm updates

## 🧠 Multi-Agent System

The chatbot uses a LangGraph workflow with three specialized agents:

1. **Research Agent** (temperature=0.3)
   - Analyzes user query
   - Retrieves relevant resume information
   - Provides context to Response Agent

2. **Response Agent** (temperature=0.7)
   - Generates natural, conversational responses
   - Uses resume context from Research Agent
   - Creates engaging, accurate answers

3. **Validation Agent** (rule-based)
   - Validates response quality
   - Checks for accuracy and relevance
   - Triggers revision if needed (max 2 iterations)

## ⚙️ Configuration

### Environment Variables

Create `.env` file from the example:

```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b  # or llama2, llama3

# Security
ALLOWED_ORIGINS=["http://localhost:8000","http://127.0.0.1:8000"]
MAX_REQUESTS_PER_MINUTE=10

# Admin Authentication
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=<bcrypt_hash>  # Generate using auth.generate_password_hash()
ADMIN_SECRET_KEY=<jwt_secret>      # Generate a random secret key

# Application
DEBUG=False
```

To generate credentials:
```python
python -c "from auth import generate_password_hash; print(generate_password_hash('Shreyansh@2025'))"
```

### Customizing Resume Data

Edit `resume_data.py` to update your information:

```python
def get_resume_data() -> Resume:
    return Resume(
        name="Your Name",
        title="Your Title",
        summary="Your professional summary...",
        contact=ContactInfo(
            email="your.email@example.com",
            phone="+1-234-567-8900",
            linkedin="https://linkedin.com/in/yourprofile",
            github="https://github.com/yourusername"
        ),
        experience=[...],
        education=[...],
        skills=[...],
        projects=[...]
    )
```

## 🧪 Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov=main --cov-report=html

# Run specific test file
pytest tests/test_api.py
```

**Current Test Coverage: 96.88%** (247 tests passing)

## 📦 Deployment

### Docker (Recommended)

```bash
# Build image
docker build -t resume-chatbot .

# Run container
docker run -p 8000:8000 \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  resume-chatbot
```

### Cloud Platforms

**Render / Railway / Fly.io:**
1. Connect GitHub repository
2. Set environment variables
3. Deploy automatically

**AWS / Azure / GCP:**
See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions

## 🤝 Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## 🙏 Acknowledgments

- **HTML5 UP** - Professional resume template
- **FastAPI** - Modern Python web framework
- **LangGraph** - Multi-agent orchestration
- **Ollama** - Local LLM inference
- **Pydantic** - Data validation

## 📧 Contact

**Shreyansh Chheda**
- Email: shreyansh.chheda@gmail.com
- LinkedIn: [shreyansh-chheda](https://linkedin.com/in/shreyansh-chheda)
- GitHub: [shrey-c](https://github.com/shrey-c)

---

⭐ **Star this repo if you find it helpful!**

Built with ❤️ using FastAPI, LangGraph, and Ollama
