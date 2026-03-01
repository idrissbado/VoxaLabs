import React, { useState, useRef } from 'react';
import {
  FiHome, FiAlertCircle, FiCheckCircle, FiLoader,
  FiSend, FiPaperclip, FiX
} from 'react-icons/fi';
import './MathTutor.css';

const API_BASE = typeof window !== 'undefined' && window.location.hostname !== 'localhost' 
  ? '' 
  : 'http://localhost:8000';

export function MathTutorSimple({ onBack }) {
  // Submission state
  const [submissionId, setSubmissionId] = useState(null);
  const [textInput, setTextInput] = useState('');
  const [fileInput, setFileInput] = useState(null);
  const [userAttempt, setUserAttempt] = useState('');
  const [submitLoading, setSubmitLoading] = useState(false);
  const [error, setError] = useState(null);

  // Submission results
  const [submitted, setSubmitted] = useState(false);
  const [submission, setSubmission] = useState(null);

  // Chat state
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);

  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      setFileInput(file);
      setError(null);
    }
  };

  const handleSubmitExercise = async (e) => {
    e.preventDefault();
    
    if (!textInput.trim() && !fileInput) {
      setError('Please enter a problem or upload a file');
      return;
    }

    try {
      setSubmitLoading(true);
      setError(null);

      const formData = new FormData();
      if (textInput.trim()) formData.append('text_input', textInput);
      if (fileInput) formData.append('file', fileInput);
      if (userAttempt.trim()) formData.append('user_attempt', userAttempt);

      const response = await fetch(`${API_BASE}/math/submit`, {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (!data.success) {
        setError(data.error || 'Failed to submit exercise');
        return;
      }

      // Success!
      setSubmission(data);
      setSubmissionId(data.submission_id);
      setSubmitted(true);
      setFileInput(null);
      setTextInput('');
      setUserAttempt('');

      // Initialize chat with tutor's first message
      if (data.chat?.context) {
        setChatMessages(data.chat.context);
      }
    } catch (err) {
      setError('Error submitting exercise: ' + err.message);
      console.error(err);
    } finally {
      setSubmitLoading(false);
    }
  };

  const handleSendChat = async (e) => {
    e.preventDefault();
    if (!chatInput.trim() || !submissionId) return;

    const userMsg = chatInput.trim();
    setChatInput('');

    // Add user message to chat
    const newMessages = [...chatMessages, { role: 'user', content: userMsg }];
    setChatMessages(newMessages);

    try {
      setChatLoading(true);

      const formData = new FormData();
      formData.append('submission_id', submissionId);
      formData.append('user_message', userMsg);

      const response = await fetch(`${API_BASE}/math/chat`, {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (data.success) {
        // Add tutor response
        newMessages.push({
          role: 'assistant',
          content: data.tutor_response || data.guidance || 'How can I help you with this step?'
        });
        setChatMessages(newMessages);
      }
    } catch (err) {
      console.error('Chat error:', err);
    } finally {
      setChatLoading(false);
    }
  };

  const resetForm = () => {
    setSubmitted(false);
    setSubmission(null);
    setSubmissionId(null);
    setChatMessages([]);
    setChatInput('');
    setTextInput('');
    setFileInput(null);
    setUserAttempt('');
  };

  return (
    <div className="math-tutor-container">
      {/* Navigation */}
      <nav className="navbar">
        <div className="nav-brand">
          <span style={{ fontSize: '1.5rem', marginRight: '12px' }}>📐</span>
          <span>Math Tutor</span>
        </div>
        <button className="nav-back-button" onClick={onBack} title="Back to Home">
          <FiHome size={20} />
        </button>
      </nav>

      <div className="math-content" style={{ maxWidth: '900px', margin: '0 auto' }}>
        {/* Error banner */}
        {error && (
          <div className="error-banner">
            <FiAlertCircle size={20} />
            <span>{error}</span>
            <button onClick={() => setError(null)}>×</button>
          </div>
        )}

        {!submitted ? (
          // SUBMISSION FORM
          <div className="submission-form">
            <div className="form-header">
              <h1>Submit Your Math Problem</h1>
              <p>Get hints, guidance, and interactive help</p>
            </div>

            <form onSubmit={handleSubmitExercise} className="form-body">
              {/* Problem Input */}
              <div className="form-section">
                <label className="form-label">
                  <span>📝 Math Problem</span>
                  <span className="required">*</span>
                </label>
                <textarea
                  value={textInput}
                  onChange={(e) => setTextInput(e.target.value)}
                  placeholder="Type your math problem here...&#10;e.g., Solve for x: 2x + 5 = 13&#10;or: Find the derivative of f(x) = x³ + 2x"
                  rows="5"
                  className="form-textarea"
                />
              </div>

              {/* File Upload */}
              <div className="form-section">
                <label className="form-label">
                  <span>📎 Or upload a file</span>
                  <span className="text-muted">(optional)</span>
                </label>
                <div 
                  className="file-upload-area"
                  onClick={() => fileInputRef.current?.click()}
                >
                  <input
                    ref={fileInputRef}
                    type="file"
                    onChange={handleFileChange}
                    accept=".pdf,.jpg,.jpeg,.png,.tex,.txt"
                    style={{ display: 'none' }}
                  />
                  {fileInput ? (
                    <div className="file-selected">
                      <FiCheckCircle size={20} color="var(--primary)" />
                      <span>{fileInput.name}</span>
                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          setFileInput(null);
                        }}
                        className="btn-remove"
                      >
                        <FiX />
                      </button>
                    </div>
                  ) : (
                    <div className="file-upload-prompt">
                      <FiPaperclip size={24} />
                      <p>Click to upload: PDF, Image, LaTeX, or Text</p>
                      <span className="text-muted">or drag and drop</span>
                    </div>
                  )}
                </div>
              </div>

              {/* Your Attempt (optional) */}
              <div className="form-section">
                <label className="form-label">
                  <span>✏️ Your attempt so far</span>
                  <span className="text-muted">(optional)</span>
                </label>
                <textarea
                  value={userAttempt}
                  onChange={(e) => setUserAttempt(e.target.value)}
                  placeholder="Describe what you've tried so far..."
                  rows="3"
                  className="form-textarea"
                />
              </div>

              {/* Submit Button */}
              <div className="form-actions">
                <button 
                  type="submit" 
                  disabled={submitLoading}
                  className="btn btn-primary"
                >
                  {submitLoading ? (
                    <>
                      <FiLoader size={16} className="spin" /> Analyzing...
                    </>
                  ) : (
                    <>
                      <FiSend size={16} /> Submit Exercise
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        ) : (
          // CHAT & HINTS VIEW
          <div className="chat-view">
            {/* Problem Summary */}
            <div className="problem-summary">
              <div className="summary-header">
                <h2>Problem</h2>
                <button onClick={resetForm} className="btn-reset">
                  ← New Problem
                </button>
              </div>
              <div className="problem-text">
                {submission.problem.text}
                {submission.problem.text.length < submission.problem.full_text.length && '...'}
              </div>
              <div className="problem-meta">
                <span className="badge">📚 {submission.problem.topic}</span>
                <span className="badge">⭐ Difficulty: {submission.problem.difficulty}/5</span>
              </div>
            </div>

            {/* Hints Section */}
            <div className="hints-section">
              <h3>💡 Hints to Guide You</h3>
              <div className="hints-grid">
                <div className="hint-card">
                  <div className="hint-number">1</div>
                  <p>{submission.hints.hint_1}</p>
                </div>
                <div className="hint-card">
                  <div className="hint-number">2</div>
                  <p>{submission.hints.hint_2}</p>
                </div>
                <div className="hint-card">
                  <div className="hint-number">3</div>
                  <p>{submission.hints.hint_3}</p>
                </div>
              </div>
            </div>

            {/* Chat Section */}
            <div className="chat-section">
              <h3>💬 Interactive Tutor Chat</h3>
              
              <div className="chat-messages">
                {chatMessages.filter(m => m.role !== 'system').map((msg, idx) => (
                  <div key={idx} className={`message message-${msg.role}`}>
                    {msg.role === 'user' ? '👤 You' : '🤖 Tutor'}: {msg.content}
                  </div>
                ))}
              </div>

              <form onSubmit={handleSendChat} className="chat-input-form">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  placeholder="Ask the tutor a question or share your progress..."
                  className="chat-input"
                  disabled={chatLoading}
                />
                <button
                  type="submit"
                  disabled={chatLoading || !chatInput.trim()}
                  className="btn-send"
                >
                  {chatLoading ? <FiLoader size={18} className="spin" /> : <FiSend size={18} />}
                </button>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
