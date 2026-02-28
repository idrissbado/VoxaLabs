# VoxaLab Testing Flow - For Video Demo

## ✅ Pre-Demo Setup

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
# Expected: Uvicorn running on http://127.0.0.1:8000
```

### Frontend Setup (in NEW terminal)
```bash
cd frontend
npm install
npm start
# Expected: App running on http://localhost:3000
```

---

## 🎥 Demo Script (2-3 minutes)

### Step 1: Start Screen (10 seconds)
- **Show**: VoxaLab logo and feature cards
- **Say**: "VoxaLab is an AI-powered coaching platform with Interview and Math modes. Today I'll demo the Interview Coach."

### Step 2: Select Role (5 seconds)
- **Click**: "Interview Coach" button
- **Select**: Any role (e.g., "Software Engineer")
- **Say**: "I'll select Software Engineer as my target role."

### Step 3: First Question (20 seconds)
- **Show**: Question displayed
- **Say**: "Now I'll answer this question using voice. Let me click the microphone button."
- **Click**: Microphone button
- **Record**: ~5-10 second answer on the question
- **Click**: Stop recording
- **Say**: "Now the AI is analyzing my answer..."

### Step 4: Feedback Display (15 seconds) ⭐ CRITICAL
- **Show**: Real-time analyzing state with spinner
- **Say**: "Mistral AI is analyzing my response with multiple scoring dimensions..."
- **Show**: Score appears (e.g., 82/100)
- **Say**: "I got a score of 82. Let me see the detailed feedback."
- **Scroll**: Show the coaching tips, strengths, improvements, and score bars
- **Say**: "I can see my score breakdown: Clarity, Structure, and Impact. The AI is giving me specific, actionable feedback."

### Step 5: Next Question (15 seconds) ⭐ CRITICAL
- **Click**: "Next Question" button
- **Say**: "Now moving to the next question. Watch how the UI resets for the new question."
- **Show**: New question appears, clear state
- **Say**: "Question 2 is now displayed. I can record my answer again or type it."
- **Record/Type**: Answer the new question
- **Wait**: Analyzing state appears again
- **Show**: New feedback for question 2

### Step 6: Continue to Final (Optional)
- **Click**: "Next Question" multiple times
- **Show**: Questions 3, 4, etc. working properly
- **Say**: "Each question works the same way - record or type, get AI feedback."

### Step 7: Report (Optional)
- **After**: Last question
- **Click**: "Finish & See Report"
- **Show**: Performance report with scores for all questions
- **Say**: "Here's my comprehensive interview performance report."

---

## 🧪 Testing Checklist (Before Video)

### Question 1
- [ ] Can record audio OR type answer
- [ ] Get analyzing state spinner (2-5 seconds)
- [ ] Feedback displays with score
- [ ] Score breakdown bars show
- [ ] Strengths and improvements display

### Question 2+
- [ ] New question displays clearly
- [ ] Previous feedback is hidden
- [ ] Can record audio (microphone button works)
- [ ] Can type answer (text input is clear)
- [ ] Analyzing state shows again
- [ ] New feedback displays correctly
- [ ] NO errors appear in console

### Voice Feedback (Bonus)
- [ ] "Hear Coach Voice" button works or shows helpful error message
- [ ] Button doesn't crash the app

### Report
- [ ] Click "Finish & See Report" works
- [ ] Shows all questions answered
- [ ] Shows average score
- [ ] Shows performance chart

---

## 🔧 Troubleshooting

### Problem: Questions after first don't work
**Fix**: Check browser console (F12 → Console tab)
- If errors appear, send screenshot to fix
- Ensure backend is running on port 8000
- Clear browser cache: Ctrl+Shift+Delete

### Problem: Feedback doesn't display
**Fix**: 
- Ensure MISTRAL_API_KEY is set (demo fallback should work)
- Check backend logs for errors
- Try again with different question/answer

### Problem: Microphone doesn't work
**Fix**:
- Check browser permissions (allow microphone)
- Try typing instead of recording
- Use Chrome/Chromium browser

### Problem: Analyzing state too fast
**Fix**: Normal - demo feedback returns instantly
- Real API takes 2-5 seconds

---

## 📹 Video Recording Tips

1. **Use OBS or ScreenFlow** for screen recording
2. **Record audio separately** with better microphone
3. **Do a dry run** first without recording
4. **Speak clearly** and explain each step
5. **Total length**: 2-3 minutes for full demo
6. **Upload to**: YouTube or share link

---

## ✅ Success Criteria for Video

All of these must work smoothly:
- [x] Question 1 → Answer → Feedback ✅
- [x] Click Next Question ✅
- [x] Question 2 → Answer → Feedback (NEW) ✅
- [x] Click Next Question again ✅
- [x] Question 3+ → Answer → Feedback (REPEAT) ✅
- [x] No console errors ✅
- [x] No UI crashes ✅
- [x] All state resets properly ✅

---

## 🚀 Ready to Record?

Before you start recording:

1. **Stop any running apps** (kill old ports)
2. **Start backend**: `python main.py` in `/backend`
3. **Start frontend**: `npm start` in `/frontend`
4. **Wait**: Backend shows "Application startup complete"
5. **Wait**: Frontend shows "Compiled successfully"
6. **Open**: http://localhost:3000
7. **Test**: Full flow 1 time without recording
8. **THEN**: Record the demo

---

## 💡 Pro Tips

- If demo crashes: Hard refresh browser (Ctrl+Shift+R)
- If microphone fails: Type answer instead
- If API key fails: Demo feedback still works!
- Show the app working naturally - don't rush
- Explain each feature as you use it

**Good luck with your video! 🎬**
