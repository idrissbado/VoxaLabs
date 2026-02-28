# VoxaLab AI - Quick Start Guide

## Start Application (30 seconds)

### Terminal 1 - Backend
```bash
cd backend
python main.py
```

Backend runs on http://localhost:8000

### Terminal 2 - Frontend
```bash
cd frontend
npm start
```

Frontend runs on http://localhost:3000

---

## How to Use

### 1. Select Your Role
- Choose from: Backend, Frontend, DevOps, Data Scientist, or Product Manager
- Select your language (English, French, Spanish, German, Chinese, Japanese)
- Click to start practice

### 2. Answer Questions

Choose your input method:

**Type Answer**
- Click the text input area
- Type your response
- Click "Get Feedback"

**Record Answer**
- Click the recording area
- Click "Start Recording"
- Speak your answer clearly
- Click "Stop Recording"
- Click "Get Feedback"

### 3. Get AI Coaching
- AI analyzes your answer
- Shows personalized coaching feedback
- Displays scores for Clarity, Depth, Communication
- Shows transcript of your speech (if recorded)
- Click "Play Audio" to hear the coach's response

### 4. Navigate Questions
- Click "Next Question" to continue
- Click "Previous" to review earlier questions
- Click "Finish" when done

### 5. Review Results
- See summary of all your responses and feedback
- Review your scores and insights
- Click "Practice Another Role" to try a different position

---

## Environment Setup

Create `.env` file in `backend/` folder:

```
MISTRAL_API_KEY=your-mistral-api-key
ELEVENLABS_API_KEY=your-elevenlabs-api-key
HOST=0.0.0.0
PORT=8000
ENV=production
```

Get your API keys from:
- Mistral: https://console.mistral.ai/
- ElevenLabs: https://elevenlabs.io/

---

## Features

- Audio Recording: Captures speech and transcribes automatically
- Text Input: Type answers directly without recording
- AI Coaching: Mistral Large 3 provides personalized feedback
- Transcription: Real speech-to-text using OpenAI Whisper
- Audio Feedback: Hear coach's response via ElevenLabs
- Question Navigation: Next/Previous buttons for easy navigation
- Multi-language: 6 languages supported
- Professional UI: React Icons for modern interface

---

## Test Workflow

1. Open http://localhost:3000
2. Select "Backend Engineer" and "English"
3. Record yourself answering OR type an answer
4. Click "Get Feedback"
5. Review coaching feedback
6. Click "Next Question" to continue
7. Complete all questions
8. View your session summary

---

## Troubleshooting

**Backend won't start**
- Check Python version: python --version (need 3.10+)
- Install dependencies: pip install -r requirements.txt
- Verify .env file has MISTRAL_API_KEY

**Frontend won't start**
- Clear cache: rm -rf node_modules && npm install
- Check Node version: node --version (need 16+)

**No audio playback**
- Verify ELEVENLABS_API_KEY is set
- Check browser microphone permissions
- Check console for errors

**Transcription slow**
- Whisper model downloads on first use (1GB)
- Wait 10-15 seconds for first transcription

---

## API Documentation

Full API documentation available at:
http://localhost:8000/docs

Test API endpoints interactively at:
http://localhost:8000/redoc
7. ✅ Click "Play Audio Feedback" to hear the coach

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version          # Should be 3.10+

# Install dependencies
pip install -r requirements.txt

# Check environment variables
# Make sure MISTRAL_API_KEY is set
```

### Frontend won't start
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm start
```

### No audio feedback
- Check `ELEVENLABS_API_KEY` is set
- Verify ElevenLabs account has API access
- Check browser volume is on

### Transcription not showing
- Check backend logs for Whisper errors
- First run downloads model (~1GB)
- Allow 10-15 seconds for first transcription

---

## 📊 Supported Roles

1. **Java Backend Engineer** 🖥️
   - Spring Boot, Microservices, AWS

2. **Frontend Engineer** 🎨
   - React, Performance, Web Standards

3. **DevOps Engineer** ⚙️
   - CI/CD, Docker, Kubernetes

4. **Data Scientist** 📈
   - ML, Statistics, Python

5. **Product Manager** 📱
   - Strategy, Roadmap, Users

---

## 🌍 Supported Languages

1. English 🇬🇧
2. Français 🇫🇷
3. Español 🇪🇸
4. Deutsch 🇩🇪
5. 中文 🇨🇳
6. 日本語 🇯🇵

---

## 📱 Features at a Glance

✅ **Real-time Feedback**: Get instant coaching on your answers  
✅ **Audio + Text**: Choose how you want to respond  
✅ **Professional Icons**: Modern UI with React Icons (no emoji)  
✅ **AI-Powered**: Mistral Large 3 for intelligent analysis  
✅ **Multi-Language**: Practice in 6 languages  
✅ **Score Tracking**: See your improvement in 3 dimensions  
✅ **Audio Coaching**: Hear the coach's feedback spoken aloud  
✅ **No Fake Data**: All feedback is real AI-generated coaching  

---

## 🚀 Ready to Practice?

```bash
# Start backend
cd backend && python main.py

# Start frontend (new terminal)
cd frontend && npm start

# Open browser to http://localhost:3000
```

**Start practicing your interview skills now!** 💪

---

*VoxaLab AI v1.0 - Production Ready*
