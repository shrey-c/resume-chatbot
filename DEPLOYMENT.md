# Deployment Guide

This guide covers deploying your Resume Chatbot Website to various platforms.

## Table of Contents

1. [Local Deployment](#local-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Platforms](#cloud-platforms)
4. [Production Checklist](#production-checklist)

---

## Local Deployment

### Development Server

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Server (Local)

```powershell
# Run with multiple workers
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Docker Deployment

### Using Docker Compose (Recommended)

**Advantages**: Includes Ollama service, easy setup, production-ready

```powershell
# Start all services
docker-compose up -d

# Pull the Ollama model
docker exec -it shreyansh-resume-chatbot-website-ollama-1 ollama pull llama2

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Using Dockerfile Only

```powershell
# Build image
docker build -t resume-chatbot:latest .

# Run container (requires external Ollama)
docker run -d \
  -p 8000:8000 \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -e OLLAMA_MODEL=llama2 \
  --name resume-chatbot \
  resume-chatbot:latest

# View logs
docker logs -f resume-chatbot

# Stop container
docker stop resume-chatbot
docker rm resume-chatbot
```

---

## Cloud Platforms

### 1. Railway (Easiest)

**Cost**: Free tier available
**Supports**: Docker, auto-scaling

**Steps**:

1. Sign up at [railway.app](https://railway.app)
2. Create new project → Deploy from GitHub
3. Connect your repository
4. Add environment variables:
   ```
   OLLAMA_BASE_URL=http://ollama:11434
   OLLAMA_MODEL=llama2
   MAX_REQUESTS_PER_MINUTE=10
   ```
5. Railway will auto-deploy on push

**Note**: Ollama needs to run separately. Consider using Ollama API or cloud AI service.

### 2. Render

**Cost**: Free tier available
**Supports**: Docker, auto-deploy

**Steps**:

1. Sign up at [render.com](https://render.com)
2. New → Web Service
3. Connect GitHub repository
4. Configure:
   - **Environment**: Docker
   - **Instance Type**: Free or Starter
   - Add environment variables
5. Deploy

**Ollama Setup**:
- Use Render's persistent disk for Ollama data
- Or use external AI API

### 3. Heroku

**Cost**: Paid (no free tier as of 2024)
**Supports**: Docker, easy scaling

**Steps**:

1. Install Heroku CLI
2. Login and create app:
   ```powershell
   heroku login
   heroku create your-resume-chatbot
   ```

3. Set environment variables:
   ```powershell
   heroku config:set OLLAMA_MODEL=llama2
   ```

4. Deploy:
   ```powershell
   git push heroku main
   ```

5. Scale:
   ```powershell
   heroku ps:scale web=1
   ```

### 4. AWS EC2

**Cost**: Pay-as-you-go
**Supports**: Full control, scalable

**Steps**:

1. **Launch EC2 Instance**
   - AMI: Ubuntu 22.04
   - Instance Type: t2.medium or larger (for Ollama)
   - Security Group: Allow ports 22, 80, 443, 8000

2. **Connect to instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install Docker**
   ```bash
   sudo apt update
   sudo apt install -y docker.io docker-compose
   sudo usermod -aG docker ubuntu
   ```

4. **Clone repository**
   ```bash
   git clone https://github.com/yourusername/resume-chatbot.git
   cd resume-chatbot
   ```

5. **Deploy with Docker Compose**
   ```bash
   docker-compose up -d
   docker exec -it resume-chatbot-ollama-1 ollama pull llama2
   ```

6. **Setup nginx (optional)**
   ```bash
   sudo apt install -y nginx
   # Configure nginx as reverse proxy
   ```

7. **Setup SSL with Let's Encrypt**
   ```bash
   sudo apt install -y certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

### 5. DigitalOcean

**Cost**: $5/month minimum
**Supports**: Droplets, App Platform

**Option A: Droplet (VPS)**

Similar to AWS EC2 steps above.

**Option B: App Platform**

1. Create account at [digitalocean.com](https://digitalocean.com)
2. Apps → Create App
3. Connect GitHub repository
4. Configure:
   - **Type**: Web Service
   - **Dockerfile**: Detected automatically
   - Add environment variables
5. Deploy

### 6. Google Cloud Run

**Cost**: Pay-per-use, generous free tier
**Supports**: Containers, auto-scaling

**Steps**:

1. Install Google Cloud SDK
2. Build and push image:
   ```powershell
   gcloud builds submit --tag gcr.io/PROJECT-ID/resume-chatbot
   ```

3. Deploy:
   ```powershell
   gcloud run deploy resume-chatbot \
     --image gcr.io/PROJECT-ID/resume-chatbot \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

**Note**: Ollama requires persistent storage or external service.

---

## Alternative: Using Cloud AI APIs

If running Ollama in production is challenging, consider using cloud AI APIs:

### OpenAI API

Modify `ollama_service.py`:

```python
import openai

async def generate_response(self, prompt: str, context: str):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a resume assistant. {context}"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
```

### Anthropic Claude API

Similar modification for Claude API.

**Benefits**:
- No need to run Ollama
- Potentially better responses
- Easier deployment

**Drawbacks**:
- Costs per API call
- External dependency

---

## Production Checklist

Before deploying to production:

### Security

- [ ] Change all default passwords/secrets
- [ ] Set `DEBUG=False` in production
- [ ] Use HTTPS (SSL certificate)
- [ ] Configure proper CORS origins
- [ ] Review rate limiting settings
- [ ] Enable firewall rules
- [ ] Regular security updates

### Performance

- [ ] Use production ASGI server (Uvicorn with workers)
- [ ] Configure caching if needed
- [ ] Optimize Docker image size
- [ ] Monitor resource usage
- [ ] Set up CDN for static files (optional)

### Monitoring

- [ ] Set up logging (CloudWatch, Datadog, etc.)
- [ ] Configure error tracking (Sentry)
- [ ] Set up uptime monitoring
- [ ] Create health check alerts
- [ ] Monitor API rate limits

### Backup

- [ ] Database backups (if using one)
- [ ] Configuration backups
- [ ] Docker volume backups
- [ ] Code versioning (Git)

### Documentation

- [ ] Update README with production URL
- [ ] Document deployment process
- [ ] Create runbook for common issues
- [ ] Document environment variables

### Testing

- [ ] Run full test suite
- [ ] Load testing
- [ ] Security scanning
- [ ] Cross-browser testing

---

## Environment Variables for Production

Create a `.env.production` file:

```bash
# AI Service
OLLAMA_BASE_URL=https://your-ollama-service.com
OLLAMA_MODEL=llama2

# Security
MAX_REQUESTS_PER_MINUTE=20
MAX_MESSAGE_LENGTH=500
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Application
DEBUG=False

# Optional: External AI API
# OPENAI_API_KEY=your-key-here
# USE_OPENAI=true
```

---

## Monitoring Commands

### Check application logs
```powershell
# Docker
docker logs -f resume-chatbot

# Docker Compose
docker-compose logs -f web
```

### Check resource usage
```powershell
# Docker stats
docker stats resume-chatbot
```

### Check health
```powershell
curl http://localhost:8000/api/health
```

---

## Scaling Strategies

### Horizontal Scaling

1. **Load Balancer**: Use nginx or cloud load balancer
2. **Multiple Instances**: Run multiple containers
3. **Auto-scaling**: Configure based on CPU/memory

### Vertical Scaling

1. **Increase Resources**: Larger instance type
2. **Optimize Code**: Profile and improve performance
3. **Caching**: Add Redis for response caching

### Database Scaling (Future)

If you add a database:
- Read replicas
- Connection pooling
- Query optimization

---

## Troubleshooting Production Issues

### Application won't start

1. Check logs: `docker logs resume-chatbot`
2. Verify environment variables
3. Check port conflicts
4. Verify Docker/Python installation

### Ollama connection errors

1. Verify Ollama is running
2. Check network connectivity
3. Verify OLLAMA_BASE_URL is correct
4. Check firewall rules

### High memory usage

1. Reduce Uvicorn workers
2. Use smaller Ollama model
3. Increase instance size
4. Add swap space

### Slow responses

1. Use faster Ollama model (mistral vs llama2:13b)
2. Increase timeout settings
3. Add response caching
4. Check network latency

---

## Cost Optimization

1. **Use free tiers**: Railway, Render offer free tiers
2. **Optimize Docker image**: Multi-stage builds
3. **Auto-scaling**: Scale down during low traffic
4. **CDN**: Use free CDN for static files
5. **Caching**: Reduce redundant AI calls

---

## Support

For deployment issues:
- Check the [README.md](README.md)
- Review [GitHub Issues](https://github.com/yourusername/repo/issues)
- Consult platform-specific documentation

---

**Ready to deploy?** Choose your platform and follow the steps above!
