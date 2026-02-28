# Deployment Guide

Complete production deployment for VoxaLab AI. Supports local, Docker, and cloud environments.

---

## Table of Contents

1. Quick Start
2. Local Development
3. Docker Deployment
4. Environment Configuration
5. Troubleshooting

---

## Quick Start

### Prerequisites

- Git
- Python 3.10 or later
- Node.js 16 or later
- Mistral API key from https://console.mistral.ai

### Get Running in 5 Minutes

```bash
git clone <repository-url>
cd voicecoach-ai

cd backend
pip install -r requirements.txt
cp .env.example .env
python main.py

cd ../frontend
npm install
npm start
```

Frontend: http://localhost:3000
API Docs: http://localhost:8000/docs

---

## Local Development

### Backend Setup

```bash
cd backend

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
echo "MISTRAL_API_KEY=your-key" >> .env
echo "ELEVENLABS_API_KEY=your-key" >> .env

python main.py
```

Backend runs on http://localhost:8000

### Frontend Setup

```bash
cd frontend

npm install

npm start
```

Frontend runs on http://localhost:3000

---

## Docker Deployment

### Using Docker Compose

```bash
docker-compose up
```

This starts:
- Backend on port 8000
- Frontend on port 3000

### Individual Docker Containers

Build backend:
```bash
cd backend
docker build -t voicecoach-backend .
docker run -e MISTRAL_API_KEY=your-key -p 8000:8000 voicecoach-backend
```

Build frontend:
```bash
cd frontend
docker build -t voicecoach-frontend .
docker run -p 3000:3000 voicecoach-frontend
```

---

## Environment Configuration

### Backend Environment Variables

Create `backend/.env`:

```
MISTRAL_API_KEY=your-mistral-api-key
ELEVENLABS_API_KEY=your-elevenlabs-api-key
HOST=0.0.0.0
PORT=8000
ENV=production
```

### Frontend Configuration

The frontend automatically detects the backend:
- Local: http://localhost:8000
- Production: Environment-specific URL

---

## Production Deployment

### Prerequisites

- Server with Python 3.10+
- Node.js 16+ installed
- Port 80 or 443 accessible
- SSL certificate (recommended)

### Steps

1. Clone repository on production server
2. Set up environment variables
3. Run backend with Uvicorn
4. Run frontend with npm or build static files
5. Configure reverse proxy (nginx/Apache)
6. Set up SSL with Let's Encrypt

### Systemd Service (Linux)

Create `/etc/systemd/system/voicecoach-backend.service`:

```
[Unit]
Description=VoxaLab AI Backend
After=network.target

[Service]
Type=simple
User=voicecoach
WorkingDirectory=/path/to/voicecoach-ai/backend
Environment="PATH=/path/to/voicecoach-ai/backend/venv/bin"
ExecStart=/path/to/voicecoach-ai/backend/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable voicecoach-backend
sudo systemctl start voicecoach-backend
```

---

## Monitoring and Logs

### View Backend Logs

```bash
cd backend
tail -f logs/app.log
```

### View Application Logs

Check `/backend/logs/` directory for detailed logs:
- app.log - Application events
- errors.log - Error messages
- access.log - Request logs

### Health Check

```bash
curl http://localhost:8000/docs
```

If you see the API documentation, the backend is running.

---

## Troubleshooting

### Backend won't start

Check Python version:
```bash
python --version
```

Reinstall dependencies:
```bash
pip install --upgrade -r requirements.txt
```

Check .env file exists:
```bash
cat .env
```

### Frontend won't start

Clear cache:
```bash
rm -rf node_modules
npm install
npm start
```

### Connection refused

Check ports:
```bash
Backend port 8000: netstat -tln | grep 8000
Frontend port 3000: netstat -tln | grep 3000
```

### API errors

Check backend is running:
```bash
curl http://localhost:8000/health
```

### Transcription slow

Whisper model downloads on first use (1GB). Wait 10-15 seconds for initialization.

---

## Performance

Typical response times:
- Audio recording: Real-time
- Transcription: 2-15 seconds
- AI analysis: 5-8 seconds
- Total: 20-30 seconds

---

## Security

- Use HTTPS in production
- Store API keys in environment variables
- Implement rate limiting
- Set up firewall rules
- Regular security updates

---

## Support

Issues? Check:
1. README.md for overview
2. API documentation at http://localhost:8000/docs
3. Application logs in backend/logs/
```

---

## Local Development

### Setup Backend

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Edit .env with your keys
# MISTRAL_API_KEY=sk-your-key-here
# HUGGINGFACE_API_KEY=hf_your-token-here

# Start backend
python main.py
```

Backend is now accessible at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# Application loads at http://localhost:3000
```

### Verify Installation

```bash
# Test backend health
curl http://localhost:8000/health

# Test frontend accessibility
curl http://localhost:3000
```

---

## Hugging Face Spaces Deployment

Deploy VoiceCoach AI to Hugging Face Spaces for free, persistent hosting.

### Step 1: Create Hugging Face Account

1. Visit https://huggingface.co/join
2. Complete signup
3. Create API token: Settings → Access Tokens → New token (write)

### Step 2: Create Backend Space

1. Go to https://huggingface.co/new-space
2. Fill in:
   - **Owner**: Your username
   - **Space name**: `voicecoach-api`
   - **License**: `MIT`
   - **Space SDK**: `Docker`
   - **Description**: "VoiceCoach AI - Interview Coaching Platform"
3. Click "Create Space"

### Step 3: Deploy Backend Code

```bash
# Navigate to backend directory
cd backend

# Configure Git for HuggingFace
git config user.email "you@example.com"
git config user.name "Your Name"

# Initialize repository
git init
git add .
git commit -m "Initial backend deployment"

# Add HuggingFace remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/voicecoach-api

# Authenticate with HuggingFace
huggingface-cli login
# Paste your token when prompted

# Push to HuggingFace
git push -f hf main:main

# Space builds automatically (2-5 minutes)
# Monitor at: https://huggingface.co/spaces/YOUR_USERNAME/voicecoach-api
```

### Step 4: Set Environment Secrets

1. Navigate to your Space: https://huggingface.co/spaces/YOUR_USERNAME/voicecoach-api
2. Click "Settings" in top menu
3. Scroll to "Repository secrets" section
4. Add these secrets (click "New secret" for each):

```
MISTRAL_API_KEY: sk-your-mistral-key-here
HUGGINGFACE_API_KEY: hf_your-huggingface-token-here
ENV: production
ALLOWED_ORIGINS: https://YOUR_USERNAME-voicecoach-app.hf.space,https://yourdomain.com
LOG_LEVEL: INFO
```

5. Click "Save"

### Step 5: Verify Backend Deployment

Wait 2-5 minutes for the Space to build and restart. Then:

```bash
# Check if backend is running
curl https://YOUR_USERNAME-voicecoach-api.hf.space/health

# Should return: {"status": "healthy"}

# Access API docs
# https://YOUR_USERNAME-voicecoach-api.hf.space/docs
```

### Step 6: Deploy Frontend (Optional)

For best results, deploy frontend separately to Vercel or static hosting:

```bash
# Build React application
cd frontend
npm run build

# Creates 'build' folder with static files
# Deploy this folder to Vercel, Netlify, or GitHub Pages

# If using Vercel:
npm install -g vercel
vercel
# Follow prompts to deploy
```

### Step 7: Connect Frontend to Backend

After frontend deployment, update the API endpoint:

**Option A: Environment Variables (Recommended)**

Create `.env.production` in frontend:

```
REACT_APP_API_URL=https://YOUR_USERNAME-voicecoach-api.hf.space
```

Update `frontend/src/App.js`:

```javascript
const API_BASE = process.env.REACT_APP_API_URL || 
  'https://YOUR_USERNAME-voicecoach-api.hf.space';
```

**Option B: Direct Configuration**

Edit `frontend/src/App.js`:

```javascript
const API_BASE = 'https://YOUR_USERNAME-voicecoach-api.hf.space';
```

### Accessing Deployed Application

- **Backend API**: `https://YOUR_USERNAME-voicecoach-api.hf.space`
- **API Documentation**: `https://YOUR_USERNAME-voicecoach-api.hf.space/docs`
- **Frontend**: `https://YOUR_USERNAME-voicecoach-app.vercel.app` (if deployed to Vercel)

---

## Railway Deployment

Deploy to Railway for production with database and custom domain support.

### Step 1: Create Railway Account

1. Visit https://railway.app
2. Sign up with GitHub
3. Authorize Railway to access your repos

### Step 2: Create New Project

1. Click "Create New Project"
2. Select "Deploy from GitHub repo"
3. Choose your voicecoach repository
4. Railway auto-detects Python environment

### Step 3: Configure Backend Service

```bash
# In Railway Dashboard:
# 1. Select 'backend' service
# 2. Go to Variables
# 3. Add environment variables:

MISTRAL_API_KEY=sk-your-key-here
HUGGINGFACE_API_KEY=hf_your-token-here
ENV=production
ALLOWED_ORIGINS=https://yourdomain.com
```

### Step 4: Deploy Frontend

```bash
# Option A: Vercel (Recommended)
cd frontend
npm install -g vercel
vercel --prod

# Option B: Railway (also supports Node.js)
# Create new Railway service for frontend
# Connect frontend repository
# Railway auto-detects Node.js
```

### Step 5: Get API URL and Configure

1. In Railway Dashboard, find your backend service
2. Copy the generated URL (e.g., `https://voicecoach-api.railway.app`)
3. Update frontend `.env.production`:

```
REACT_APP_API_URL=https://voicecoach-api.railway.app
```

### Step 6: Verify Deployment

```bash
# Check backend health
curl https://voicecoach-api.railway.app/health

# Check API documentation
# https://voicecoach-api.railway.app/docs
```

---

## Docker Deployment

Run VoiceCoach AI using Docker containers locally or in production.

### Create Dockerfile for Backend

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Create Dockerfile for Frontend

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

RUN npm run build

FROM node:18-alpine

WORKDIR /app

RUN npm install -g serve

COPY --from=build /app/build ./build

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
```

### Build Images

```bash
# Backend image
cd backend
docker build -t voicecoach-api:latest .

# Frontend image
cd ../frontend
docker build -t voicecoach-app:latest .
```

### Run with Docker Compose

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: voicecoach-api
    ports:
      - "8000:8000"
    environment:
      - MISTRAL_API_KEY=${MISTRAL_API_KEY}
      - HUGGINGFACE_API_KEY=${HUGGINGFACE_API_KEY}
      - ENV=production
      - PORT=8000
      - ALLOWED_ORIGINS=http://localhost:3000,http://frontend:3000
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    networks:
      - voicecoach

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: voicecoach-app
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://backend:8000
    depends_on:
      backend:
        condition: service_healthy
    networks:
      - voicecoach

networks:
  voicecoach:
    driver: bridge
```

### Run Application

```bash
# Start both services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild images
docker-compose up -d --build
```

### Verify Docker Deployment

```bash
# Check if containers are running
docker ps

# Check backend health
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000

# View backend logs
docker logs voicecoach-api

# View frontend logs
docker logs voicecoach-app
```

---

## Environment Configuration

### Backend .env Template

```bash
# Mistral Configuration
MISTRAL_API_KEY=sk-your-mistral-api-key-here
MISTRAL_MODEL=mistral-large-latest

# Hugging Face Configuration
HUGGINGFACE_API_KEY=hf_your-huggingface-token-here
HUGGINGFACE_REPO_ID=voicecoach-ai/voicecoach-api

# Server Configuration
HOST=0.0.0.0
PORT=8000
ENV=production

# Security
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com,https://YOUR_USERNAME-voicecoach-app.hf.space

# Logging
LOG_LEVEL=INFO

# Feature Flags
ENABLE_VOICE_TRANSCRIPTION=true
ENABLE_AUDIO_PROCESSING=true
ENABLE_REPORT_GENERATION=true

# Database (optional)
DATABASE_URL=postgresql://user:password@localhost:5432/voicecoach
```

### Frontend .env.production Template

```bash
# API Configuration
REACT_APP_API_URL=https://YOUR_USERNAME-voicecoach-api.hf.space
REACT_APP_ENV=production

# Analytics (optional)
REACT_APP_ANALYTICS_KEY=your-analytics-key
```

---

## Monitoring & Logs

### Application Health Checks

```bash
# Local
curl http://localhost:8000/health

# Hugging Face Spaces
curl https://YOUR_USERNAME-voicecoach-api.hf.space/health

# Railway
curl https://voicecoach-api.railway.app/health

# Expected response:
# {"status": "healthy", "timestamp": "2026-02-28T10:30:00Z"}
```

### View Logs

**Hugging Face Spaces:**
1. Go to your Space: https://huggingface.co/spaces/YOUR_USERNAME/voicecoach-api
2. Click "Logs" tab
3. Scroll to see real-time application output

**Railway:**
```bash
# View backend logs
railway logs backend

# Follow logs in real-time
railway logs backend -f

# View specific environment
railway logs --environment production
```

**Docker:**
```bash
# View logs
docker logs voicecoach-api
docker logs voicecoach-app

# Follow logs
docker logs -f voicecoach-api

# Last 100 lines with timestamp
docker logs -f --tail 100 voicecoach-api
```

**Local Development:**
```bash
# Terminal automatically shows FastAPI output
# Look for logs like:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete
```

---

## Troubleshooting

### Issue: "Connection refused" when accessing API

**Cause**: Backend service not running or not accessible

**Solution**:
```bash
# Check if backend is running
curl http://localhost:8000/health

# If not running:
cd backend
python main.py

# Check firewall isn't blocking port 8000
# On Windows:
netstat -ano | findstr :8000

# On macOS/Linux:
lsof -i :8000
```

### Issue: "CORS error" in frontend console

**Cause**: API endpoint not in ALLOWED_ORIGINS

**Solution**:
1. Check frontend is making requests to correct API_BASE
2. Add frontend URL to backend .env ALLOWED_ORIGINS
3. Restart backend for changes to take effect

```bash
# In frontend console, check:
console.log('API Base:', API_BASE)

# In backend .env:
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### Issue: "API returns 503 Service Unavailable"

**Cause**: Mistral API rate limit or authentication issue

**Solution**:
```bash
# Verify API key is correct
# Check Mistral console at https://console.mistral.ai

# Verify requests in logs
docker logs voicecoach-api

# Test Mistral connection
python -c "
from mistralai import Mistral
client = Mistral(api_key='YOUR_KEY')
print(client.models.list())
"
```

### Issue: "Microphone not working" in production

**Cause**: HTTPS not enabled (required for Web Audio API)

**Solution**:
- Ensure frontend is served over HTTPS
- Add SSL certificate (Let's Encrypt recommended)
- Hugging Face Spaces and Railway auto-provide HTTPS

**Test microphone access:**
```javascript
// In browser console
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(() => console.log('Microphone access granted'))
  .catch(err => console.error('Error:', err))
```

### Issue: "High latency" or "slow responses"

**Cause**: Mistral API processing time or network latency

**Solution**:
```bash
# Add request logging to see where time is spent
# In backend services/mistral_service.py:

import time
start = time.time()
response = await coaching_chain.ainvoke(...)
elapsed = time.time() - start
logger.info(f"Mistral response time: {elapsed:.2f}s")
```

### Issue: "Hugging Face Space stuck building"

**Cause**: Dockerfile syntax error or missing dependencies

**Solution**:
1. Check Dockerfile syntax: `docker build backend/Dockerfile`
2. Verify requirements.txt: `pip install -r backend/requirements.txt`
3. Check Space logs: https://huggingface.co/spaces/YOUR_USERNAME/voicecoach-api
4. Rebuild manually: Push new commit to trigger rebuild

```bash
git commit --allow-empty -m "Rebuild space"
git push -f hf main:main
```

---

## Performance Optimization

### Frontend Optimization

```bash
# Build optimized production bundle
npm run build

# Analyze bundle size
npm run build -- --analyze

# Results in build/report.html
```

### Backend Optimization

```python
# Enable async/await throughout
async def analyze_answer(question: str, answer: str):
    # Use async operations
    pass

# Use LangChain caching
from langchain.cache import InMemoryCache
import langchain
langchain.llm_cache = InMemoryCache()
```

### Database Optimization (if using PostgreSQL)

```bash
# Add indexes for common queries
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_answers_session_id ON answers(session_id);

# Vacuum and analyze
VACUUM ANALYZE;
```

---

## Security Best Practices

1. **Never commit sensitive data**
   - Add `.env` to `.gitignore`
   - Use `.env.example` for template only

2. **Rotate API keys regularly**
   - Change Mistral API key monthly
   - Monitor for unauthorized usage

3. **Enable HTTPS everywhere**
   - Use SSL certificates (Hugging Face/Railway provide)
   - Redirect HTTP to HTTPS

4. **Limit CORS origins**
   - Only add trusted frontend domains
   - Remove localhost in production

5. **Rate limit endpoints**
   - Prevent brute force attempts
   - Limit API calls per user

6. **Keep dependencies updated**
   ```bash
   # Update Python packages
   pip install --upgrade -r requirements.txt
   
   # Update npm packages
   npm update
   ```

7. **Monitor logs for suspicious activity**
   - Check for unusual API patterns
   - Alert on repeated failures

---

## Support & Resources

- **API Documentation**: See `/docs` endpoint (Swagger UI)
- **Architecture**: Read [ARCHITECTURE.md](ARCHITECTURE.md)
- **Setup**: Read [SETUP.md](SETUP.md)
- **Issues**: Create GitHub Issue
- **Mistral Docs**: https://docs.mistral.ai
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev

---

**Last Updated**: February 28, 2026  
**Version**: 2.0.0  
**Status**: Production Ready
