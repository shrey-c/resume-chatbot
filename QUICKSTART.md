# 🚀 Quick Start Guide - Resume Chatbot

Get your AI resume chatbot with admin portal running in **5 minutes**!

## Prerequisites Checklist

- [ ] Python 3.11+ installed
- [ ] Ollama installed from https://ollama.ai/

## Step 1: Install Dependencies (1 min)

```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install all packages (FastAPI, LangGraph, LangChain, PDF parsers, auth)
pip install -r requirements.txt
```

## Step 2: Set Up Environment (1 min)

```powershell
# Copy example environment file
cp .env.example .env

# Generate password hash for admin
python -c "from app.core.auth import generate_password_hash; print(generate_password_hash('Shreyansh@2025'))"

# Edit .env and paste the hash as ADMIN_PASSWORD_HASH
# Also set a strong ADMIN_SECRET_KEY (random string at least 32 chars)
```

Or manually edit `.env`:
```bash
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=<paste-hash-here>
ADMIN_SECRET_KEY=<random-secret-key-at-least-32-chars>
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b
```

## Step 3: Install Ollama & Model (2 min)

```powershell
# Download from https://ollama.ai/ and install

# Pull the AI model
ollama pull llama3.2:1b

# Verify installation
ollama list
```

## Step 4: Start the Server (10 sec)

```powershell
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Starting Resume Chatbot API...
INFO:     LangGraph multi-agent system initialized
INFO:     Ollama service is healthy. Using model: llama3.2:1b
```

## Step 5: Upload Your Resume (1 min)

1. **Open admin portal**: http://localhost:8000/admin
2. **Login** with credentials from Step 2
3. **Upload your resume PDF**
4. **AI automatically extracts**:
   - ✓ Contact information
   - ✓ Work experience with achievements
   - ✓ Education
   - ✓ Skills (categorized)
   - ✓ Projects with technologies
   - ✓ Certifications & awards
5. **Done!** Website updates instantly

## 🎉 Your Site is Live!

- **Resume Website**: http://localhost:8000
- **Admin Portal**: http://localhost:8000/admin  
- **API Documentation**: http://localhost:8000/docs

## Testing the Chatbot

The chatbot uses LangGraph multi-agent workflow:

**Try these questions:**
- "What AI/ML experience do you have?"
- "Tell me about your most impactful project"
- "What technologies are you expert in?"
- "Walk me through your career progression"

**Agents at work:**
1. **ResearchAgent** → Analyzes query, extracts relevant resume facts
2. **ResponseAgent** → Generates professional, enthusiastic response
3. **ValidationAgent** → Checks for accuracy, positive tone, safety

## 🎨 Customize (Optional)

### Change AI Model
Edit `.env`:
```bash
OLLAMA_MODEL=llama3  # or mistral, codellama, etc.
```
Then: `ollama pull llama3`

### Adjust Agent Behavior
Edit `app/services/agents.py`:
- **ResearchAgent** - Modify extraction prompts
- **ResponseAgent** - Adjust temperature (0.7 = creative, 0.3 = factual)
- **ValidationAgent** - Add/remove safety patterns

### Customize Website Design
- Edit `static/index.html` for structure
- Photo with subtle filter at `static/images/shrey.jpg`

## 🛠️ Troubleshooting

### "Cannot connect to AI service"
**Solution**: Start Ollama
```powershell
ollama serve
```

### "Model not found"
**Solution**: Pull the model
```powershell
ollama pull llama2
```

### "Module not found"
**Solution**: Activate virtual environment
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## What's Next?

- [ ] Customize styling in `static/styles.css`
- [ ] Add more resume sections
- [ ] Try different Ollama models
- [ ] Deploy to cloud platform
- [ ] Add custom domain

## Getting Help

- Check `README.md` for detailed documentation
- Review `tests/` for usage examples
- Check GitHub Issues
- Read Ollama documentation

## Pro Tips

1. **Better AI Responses**: Use larger models
   ```powershell
   ollama pull llama2:13b
   ```

2. **Faster Responses**: Use smaller models
   ```powershell
   ollama pull mistral
   ```

3. **Run Tests on Changes**
   ```powershell
   pytest --cov
   ```

4. **Debug Mode**: Set in `.env`
   ```
   DEBUG=True
   ```

---

**Ready to go?** Run `python main.py` and visit http://localhost:8000
