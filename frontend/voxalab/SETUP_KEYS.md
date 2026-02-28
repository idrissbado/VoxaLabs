# VoxaLab Setup Guide - API Keys & Environment

## 🔑 Required API Keys

### 1. Mistral AI API Key
**Purpose**: Powers the coaching AI engine

**Get it**:
1. Go to https://console.mistral.ai/api-keys/
2. Create new API key
3. Copy and save it

**Set it**:
```bash
export MISTRAL_API_KEY="your_key_here"
```

---

### 2. ElevenLabs API Key  
**Purpose**: Text-to-speech voice output for coach feedback

**Get it**:
1. Sign up at https://elevenlabs.io
2. Go to https://elevenlabs.io/app/api-keys
3. Copy your API key

**Set it**:
```bash
export ELEVENLABS_API_KEY="your_key_here"
```

---

### 3. Hugging Face Token
**Purpose**: Deploy to HF Spaces

**Get it**:
1. Go to https://huggingface.co/settings/tokens
2. Create **write** token
3. Copy it

**Set it** (for HF Spaces):
1. Go to your Space settings
2. Add under "Repository Secrets":
   - `HUGGINGFACE_API_KEY`: your token

---

## ⚙️ Local Setup

### .env file
Create `backend/.env`:
```dotenv
MISTRAL_API_KEY=your_mistral_key
ELEVENLABS_API_KEY=your_elevenlabs_key
PORT=8000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Run Locally
```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py

# Frontend (new terminal)
cd frontend
npm install
npm start
```

---

## 🚀 HF Spaces Setup

### Add Secrets to HF Spaces

1. Go to your Space: https://huggingface.co/spaces/mistral-hackaton-2026/voxalab
2. Click **Settings** → **Repository secrets**
3. Add these secrets:

| Key | Value |
|-----|-------|
| `MISTRAL_API_KEY` | Your Mistral key |
| `ELEVENLABS_API_KEY` | Your ElevenLabs key |
| `HUGGINGFACE_API_KEY` | Your HF write token |

### Verify Deployment

App will auto-build after secrets are added. Check:
- **App tab**: Should see VoxaLab UI
- **Logs tab**: Should show `✅ Backend routes loaded successfully`

---

## ✅ Verify Everything Works

### Test locally:
```bash
curl http://localhost:8000/health
# Should return: {"status": "ok"}
```

### Test HF Spaces:
Visit: https://huggingface.co/spaces/mistral-hackaton-2026/voxalab
- Should see React app loading
- Should be able to record and get feedback

---

## 🐛 Troubleshooting

**No backend routes loaded?**
- Check MISTRAL_API_KEY is set: `echo $MISTRAL_API_KEY`
- Check logs for import errors

**No voice output?**
- Verify ELEVENLABS_API_KEY is set
- Check ElevenLabs account has credits

**HF Spaces build error?**
- Check Repository Secrets are added correctly
- Wait 5 minutes after adding secrets for rebuild

---

## 📝 File Locations

- Env template: `backend/.env.example`
- Main backend: `backend/main.py`
- Backend routes: `backend/routers/`
- Frontend: `frontend/src/App.js`
- Docker config: `Dockerfile` + `main_hf.py`
