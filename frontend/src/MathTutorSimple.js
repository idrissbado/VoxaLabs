import React, { useState, useRef } from 'react';
import {
  FiHome, FiAlertCircle, FiCheckCircle, FiLoader,
  FiSend, FiPaperclip, FiX
} from 'react-icons/fi';

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

      <style jsx>{`
        .math-tutor-container {
          min-height: 100vh;
          background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
          display: flex;
          flex-direction: column;
        }

        .navbar {
          background: white;
          border-bottom: 1px solid #e5e7eb;
          padding: 1rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        .nav-brand {
          display: flex;
          align-items: center;
          font-size: 1.25rem;
          font-weight: 600;
          color: #1f2937;
          gap: 0.5rem;
        }

        .nav-back-button {
          background: #f3f4f6;
          border: none;
          border-radius: 8px;
          padding: 0.5rem;
          cursor: pointer;
          display: flex;
          align-items: center;
          color: #6b7280;
          transition: all 0.2s;
        }

        .nav-back-button:hover {
          background: #e5e7eb;
          color: #1f2937;
        }

        .math-content {
          flex: 1;
          padding: 2rem;
          overflow-y: auto;
        }

        .error-banner {
          display: flex;
          align-items: center;
          gap: 1rem;
          background: #fee2e2;
          border: 1px solid #fca5a5;
          border-radius: 8px;
          padding: 1rem;
          margin-bottom: 1.5rem;
          color: #dc2626;
        }

        .error-banner button {
          background: transparent;
          border: none;
          font-size: 1.5rem;
          cursor: pointer;
          color: inherit;
        }

        .submission-form, .chat-view {
          background: white;
          border-radius: 12px;
          padding: 2rem;
          box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        }

        .form-header, .summary-header {
          margin-bottom: 2rem;
          text-align: center;
        }

        .form-header h1, .chat-view h2 {
          margin: 0;
          font-size: 1.75rem;
          color: #1f2937;
          margin-bottom: 0.5rem;
        }

        .form-header p {
          margin: 0;
          color: #6b7280;
          font-size: 1rem;
        }

        .summary-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          text-align: left;
          margin-bottom: 1rem;
        }

        .summary-header h2 {
          margin: 0;
          font-size: 1.25rem;
        }

        .btn-reset {
          background: #f3f4f6;
          border: 1px solid #d1d5db;
          padding: 0.5rem 1rem;
          border-radius: 6px;
          cursor: pointer;
          font-size: 0.875rem;
          transition: all 0.2s;
        }

        .btn-reset:hover {
          background: #e5e7eb;
        }

        .form-body {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }

        .form-section {
          display: flex;
          flex-direction: column;
        }

        .form-label {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-weight: 600;
          margin-bottom: 0.75rem;
          color: #1f2937;
        }

        .required {
          color: #dc2626;
        }

        .text-muted {
          color: #9ca3af;
          font-size: 0.875rem;
          font-weight: 400;
        }

        .form-textarea {
          border: 1px solid #d1d5db;
          border-radius: 8px;
          padding: 0.75rem;
          font-family: 'Segoe UI', sans-serif;
          font-size: 1rem;
          resize: vertical;
          transition: all 0.2s;
        }

        .form-textarea:focus {
          outline: none;
          border-color: #6366f1;
          box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }

        .file-upload-area {
          border: 2px dashed #d1d5db;
          border-radius: 8px;
          padding: 2rem;
          text-align: center;
          cursor: pointer;
          transition: all 0.2s;
          background: #f9fafb;
        }

        .file-upload-area:hover {
          border-color: #6366f1;
          background: #f3f4f6;
        }

        .file-upload-prompt {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 0.5rem;
          color: #6b7280;
        }

        .file-upload-prompt p {
          margin: 0;
          font-weight: 500;
        }

        .file-selected {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 1rem;
          padding: 1rem;
          background: #ecfdf5;
          border-radius: 8px;
          color: #059669;
        }

        .btn-remove {
          background: transparent;
          border: none;
          cursor: pointer;
          color: inherit;
          font-size: 1.2rem;
        }

        .form-actions {
          display: flex;
          gap: 1rem;
          margin-top: 1rem;
        }

        .btn {
          padding: 0.75rem 1.5rem;
          border-radius: 8px;
          border: none;
          font-weight: 600;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 1rem;
          transition: all 0.2s;
        }

        .btn-primary {
          background: #6366f1;
          color: white;
        }

        .btn-primary:hover:not(:disabled) {
          background: #4f46e5;
          transform: translateY(-2px);
        }

        .btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .spin {
          animation: spin 1s linear infinite;
        }

        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }

        .problem-summary {
          background: #f9fafb;
          border: 1px solid #e5e7eb;
          border-radius: 8px;
          padding: 1.5rem;
          margin-bottom: 2rem;
        }

        .problem-text {
          background: white;
          padding: 1rem;
          border-radius: 6px;
          margin-bottom: 1rem;
          line-height: 1.6;
          color: #374151;
        }

        .problem-meta {
          display: flex;
          gap: 1rem;
          flex-wrap: wrap;
        }

        .badge {
          background: #dbeafe;
          color: #1e40af;
          padding: 0.25rem 0.75rem;
          border-radius: 4px;
          font-size: 0.875rem;
          font-weight: 500;
        }

        .hints-section {
          margin-bottom: 2rem;
        }

        .hints-section h3 {
          margin: 0 0 1rem 0;
          color: #1f2937;
        }

        .hints-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 1rem;
        }

        .hint-card {
          background: #fffbeb;
          border: 1px solid #fde68a;
          border-radius: 8px;
          padding: 1.25rem;
          position: relative;
        }

        .hint-number {
          position: absolute;
          top: 12px;
          right: 12px;
          background: #f59e0b;
          color: white;
          width: 28px;
          height: 28px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 600;
          font-size: 0.875rem;
        }

        .hint-card p {
          margin: 0 0 0 0;
          color: #78350f;
          line-height: 1.5;
          padding-right: 2rem;
        }

        .chat-section {
          margin-top: 2rem;
        }

        .chat-section h3 {
          margin: 0 0 1rem 0;
          color: #1f2937;
        }

        .chat-messages {
          background: #f9fafb;
          border: 1px solid #e5e7eb;
          border-radius: 8px;
          padding: 1rem;
          height: 300px;
          overflow-y: auto;
          margin-bottom: 1rem;
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        .message {
          padding: 0.75rem 1rem;
          border-radius: 6px;
          line-height: 1.4;
          font-size: 0.95rem;
        }

        .message-user {
          background: #dbeafe;
          color: #1e3a8a;
          align-self: flex-end;
          max-width: 70%;
        }

        .message-assistant {
          background: #dcfce7;
          color: #166534;
          align-self: flex-start;
          max-width: 70%;
        }

        .chat-input-form {
          display: flex;
          gap: 0.5rem;
        }

        .chat-input {
          flex: 1;
          border: 1px solid #d1d5db;
          border-radius: 8px;
          padding: 0.75rem 1rem;
          font-size: 1rem;
          font-family: inherit;
        }

        .chat-input:focus {
          outline: none;
          border-color: #6366f1;
          box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }

        .btn-send {
          background: #6366f1;
          color: white;
          border: none;
          border-radius: 8px;
          padding: 0.75rem;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.2s;
        }

        .btn-send:hover:not(:disabled) {
          background: #4f46e5;
        }

        .btn-send:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        @media (max-width: 768px) {
          .math-content {
            padding: 1rem;
          }

          .submission-form, .chat-view {
            padding: 1.5rem;
          }

          .hints-grid {
            grid-template-columns: 1fr;
          }

          .message-user, .message-assistant {
            max-width: 100%;
          }
        }
      `}</style>
    </div>
  );
}
