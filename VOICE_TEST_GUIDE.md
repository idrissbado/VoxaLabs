# Voice Feature - Quick Test Guide

## Prerequisites Met
- ElevenLabs API key configured
- Backend running at http://localhost:8000
- Frontend running at http://localhost:3000
- Both servers communicating

## Step-by-Step Test

### **Step 1: Open the App**
1. Go to http://localhost:3000
2. You should see: "VoiceCoach AI" with the landing page

### **Step 2: Start a Practice Session**
1. Select a role (e.g., "Software Engineer")
2. Click "Start Practice Session"
3. You'll see a question and answer interface

### **Step 3: Answer a Question**
- **Option A - Use Microphone**: Click "Record Answer"
- **Option B - Type Answer**: Type in the text area and click "Submit Answer"

### **Step 4: See the Voice Button**
After submitting your answer, you'll see:
- Your score
- Coaching feedback
- **NEW**: "Hear Coach" button (green button)

### **Step 5: Click to Hear**
1. Click the "Hear Coach" button
2. You should hear the coaching feedback spoken in a natural voice!
3. The button will show "Playing..." while audio plays
4. Wait for audio to finish (or click again to stop)

---

## Troubleshooting

### **Button doesn't appear?**
- Check backend is running: http://localhost:8000/health
- Check browser console for errors (F12)
- Refresh the page

### **No sound when clicking?**
- Check speaker volume
- Check browser permissions (should allow audio playback)
- Open browser DevTools (F12) → Network tab
- Click "Hear Coach" and look for `/tts/speak` request
- If status is 500, check backend logs

### **Error message appears?**
- Check ELEVENLABS_API_KEY in backend/.env
- Restart backend server
- Check your ElevenLabs account has quota remaining

---

## What's Being Tested

- **Frontend**: Voice button UI, state management, audio playback
- **Backend**: TTS endpoint, ElevenLabs integration, error handling
- **Integration**: Frontend → Backend → ElevenLabs → Audio

---

## Expected Behavior

1. Click "Hear Coach"
2. Button becomes disabled (shows "Playing...")
3. Audio streams from backend
4. Coaching feedback plays in natural voice
5. After audio ends, button becomes enabled again
6. You can click again to hear again

---

## Tips

- **Quality**: Audio is professional quality from ElevenLabs
- **Speed**: First request takes ~1-2 seconds (generation)
- **Cache**: Subsequent identical requests should be faster
- **Volume**: Adjust your system volume as needed

---

## Next Steps

After confirming voice works:
1. **Deploy to Hugging Face**: Voice feature works with deployment
2. **Test all roles**: Try different interview roles
3. **Check quote usage**: Monitor your ElevenLabs account
4. **Gather feedback**: How does the voice quality feel?

---

**Status**: Ready to Test
**Voice Quality**: Premium (ElevenLabs)
**Cost**: Free tier provided
**Deployment**: Ready for HF Spaces
