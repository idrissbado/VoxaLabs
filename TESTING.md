# 🧪 Math Tutor Testing Guide

Quick reference for testing the Math Tutor feature locally.

## Quick Start Testing

### 1. Start Backend
```bash
cd backend
python main.py
```

Should show:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2. Start Frontend (new terminal)
```bash
cd frontend
npm start
```

Should show:
```
Compiled successfully!
You can now view voicecoach in the browser.
Local: http://localhost:3000
```

### 3. Test in Browser
1. Open http://localhost:3000
2. Click the mode selector
3. Choose **"Math Tutor"**
4. Enter a math problem (examples below)
5. Follow the step-by-step process

---

## Test Cases

### ✅ Test Case 1: Simple Linear Equation (Baseline)
**Problem Input**:
```
Solve for x: 2x + 5 = 13
```

**Expected Behavior**:
1. Analysis shows:
   - Topic: Algebra
   - Difficulty: ⭐⭐ (2-3 stars)
   - Concepts: variable isolation, inverse operations
   - First Question: "What operation removes +5?"

2. User enters Step 1: `2x = 8`
   - Shows: ✅ Correct!
   - Explanation: "Good! You isolated x by subtracting 5 from both sides."

3. User enters Step 2: `x = 4`
   - Shows: ✅ Correct!
   - Final solution displays with LaTeX: `x = 4`

---

### ✅ Test Case 2: Intentional Error Detection
**Problem Input**:
```
Solve for x: 3x - 2 = 10
```

**Intentionally Enter Wrong Step**:
```
3x = 10 - 2 = 8
```

**Expected Behavior**:
1. Shows: ❌ Not quite right
2. Error Type: algebraic
3. Displays helpful hint without spoiling
4. Reasoning Quality Score: Low (e.g., 3/10)

---

### ✅ Test Case 3: Multi-Step Problem
**Problem Input**:
```
Find the derivative of f(x) = 3x^2 + 2x + 5
```

**Expected Behavior**:
1. Analysis shows difficulty: ⭐⭐⭐⭐ (4 stars)
2. System guides step-by-step through differentiation
3. Each step validated for calculus correctness
4. Final LaTeX solution: `f'(x) = 6x + 2`

---

### ✅ Test Case 4: Quadratic Equation
**Problem Input**:
```
Solve: x^2 - 5x + 6 = 0
```

**Expected Behavior**:
1. Difficulty: ⭐⭐⭐ (3 stars)
2. Validates factoring: `(x-2)(x-3) = 0`
3. Validates solutions: `x = 2, x = 3`
4. Shows mastery score and learning insights

---

## API Testing (Advanced)

### Using curl or Postman

**Test 1: Analyze Problem**
```bash
curl -X POST http://localhost:8000/math/analyze \
  -H "Content-Type: application/json" \
  -d '{"problem_text": "Solve for x: 2x + 5 = 13"}'
```

**Expected Response**:
```json
{
  "topic": "Algebra",
  "subtopic": "Linear Equations",
  "difficulty": 2,
  "required_concepts": ["variable isolation", "inverse operations"],
  "first_question": "What operation...",
  "solution_steps_count": 2
}
```

**Test 2: Validate Step**
```bash
curl -X POST http://localhost:8000/math/validate-step \
  -H "Content-Type: application/json" \
  -d '{
    "problem_text": "Solve for x: 2x + 5 = 13",
    "step_number": 1,
    "student_step": "2x = 8",
    "context": ""
  }'
```

**Expected Response**:
```json
{
  "is_correct": true,
  "error_type": null,
  "confidence": 0.95,
  "explanation": "Correct! You isolated the x term...",
  "hint": null,
  "reasoning_quality_score": 9
}
```

**Test 3: Generate Solution**
```bash
curl -X POST http://localhost:8000/math/generate-solution \
  -H "Content-Type: application/json" \
  -d '{
    "problem_text": "Solve for x: 2x + 5 = 13",
    "student_solution": "2x = 8\nx = 4"
  }'
```

**Test 4: Generate Practice Problem**
```bash
curl -X POST http://localhost:8000/math/practice-problem \
  -H "Content-Type: application/json" \
  -d '{"topic": "Linear Equations", "difficulty": 2}'
```

---

## Testing Checklist

### Frontend Tests
- [ ] Mode selector shows "Interview Coach" and "Math Tutor"
- [ ] Clicking "Math Tutor" shows problem input form
- [ ] Problem input accepts multi-line text
- [ ] Submit button is disabled with empty input
- [ ] Error message displays when problem is empty
- [ ] Problem analysis displays all fields
- [ ] Step input accepts text
- [ ] Feedback displays after step submission
- [ ] Correct feedback shows green styling
- [ ] Incorrect feedback shows orange styling
- [ ] Hints display without showing solution
- [ ] Confidence meter animates
- [ ] Solution display shows all sections
- [ ] LaTeX code is visible and copyable
- [ ] "Solve Another Problem" button resets UI
- [ ] "Back to Home" button returns to landing page

### Backend Tests
- [ ] API responds to all 4 POST endpoints
- [ ] Health check endpoint returns operational status
- [ ] Validate empty problem text (returns error)
- [ ] Validate empty step text (returns error)
- [ ] Validate step_number < 1 (returns error)
- [ ] Validate difficulty outside 1-5 range (returns error)
- [ ] Correct steps get is_correct: true
- [ ] Incorrect steps get is_correct: false
- [ ] Error types are categorized correctly
- [ ] Confidence scores are 0-1 range
- [ ] LaTeX is properly formatted
- [ ] Mastery scores are 0-100 range

### Error Handling Tests
- [ ] Network error shows user-friendly message
- [ ] API timeout shows appropriate error
- [ ] Invalid problem returns error
- [ ] Empty responses handled gracefully
- [ ] CORS errors are addressed
- [ ] API errors show helpful messages

### User Experience Tests
- [ ] Smooth transitions between phases
- [ ] No layout shifts on content load
- [ ] Mobile responsiveness on smaller screens
- [ ] Dark theme is readable
- [ ] Animations are smooth (not jarring)
- [ ] Buttons are clickable without lag
- [ ] Form inputs are accessible
- [ ] Error messages are clear and actionable

---

## Common Issues & Solutions

### Issue: API responds with 500 error

**Cause**: Mistral API key not set
```bash
# Check if API key is set
echo $MISTRAL_API_KEY

# Set it if missing
export MISTRAL_API_KEY=your-key-here
```

### Issue: Frontend shows "API request failed"

**Cause**: Backend not running or CORS issue
```bash
# Verify backend is running
curl http://localhost:8000/docs

# Check browser console for CORS errors
```

### Issue: LaTeX doesn't display properly

**Cause**: LaTeX formatting issue
- Check the generated LaTeX code
- Verify it uses `\[ ... \]` for display math
- Test with simpler expressions first

### Issue: Steps not validating correctly

**Cause**: Problem text or step format issue
- Verify problem text is clear and mathematical
- Check step text is proper mathematical notation
- Try simpler test problems first

---

## Performance Benchmarks

Expected response times:
- Problem analysis: 2-4 seconds
- Step validation: 1-3 seconds
- Solution generation: 3-5 seconds
- Practice problem: 2-3 seconds

**Note**: Times depend on Mistral API latency

---

## Debugging Tips

### Enable Verbose Logging
```bash
# Add to backend main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Frontend Network Requests
1. Open browser DevTools (F12)
2. Go to Network tab
3. Submit a problem
4. Click on each request to see:
   - Status code
   - Request/response bodies
   - Timing information

### Test Endpoints Directly
Use Swagger UI at http://localhost:8000/docs
- All endpoints documented
- Test buttons for each endpoint
- Try out different inputs

---

## Success Indicators

✅ **All systems working if**:
1. Frontend loads without errors
2. Math Tutor mode is accessible
3. Problems can be submitted and analyzed
4. Steps are validated with feedback
5. Solutions generate with LaTeX
6. No errors in browser console
7. No errors in backend logs
8. Response times are reasonable

---

**Ready to test?** Start the backend and frontend, then open http://localhost:3000 and select **Math Tutor** mode!
