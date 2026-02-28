import React, { useState, useRef } from 'react';
import axios from 'axios';
import './App.css';

// Backend API URL - works both locally and on HF Spaces
// On HF Spaces, routes are at root: /session, /analysis, /report, /tts
// On localhost, routes are at http://localhost:8000
const API_BASE = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000' 
  : '';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  }
});

function App() {
  const [page, setPage] = useState('landing');
  const [selectedRole, setSelectedRole] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [userAnswer, setUserAnswer] = useState('');
  const [sessionAnswers, setSessionAnswers] = useState([]);
  const [sessionReport, setSessionReport] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playingFeedback, setPlayingFeedback] = useState(null);
  
  // Audio recording refs
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerIntervalRef = useRef(null);
  const audioPlayerRef = useRef(null);

  // Available roles for interview practice
  const roleOptions = [
    { name: 'Software Engineer', icon: '💻' },
    { name: 'Product Manager', icon: '📊' },
    { name: 'Designer', icon: '🎨' },
    { name: 'Data Scientist', icon: '📈' },
    { name: 'Marketing', icon: '📱' }
  ];

  // Start a new practice session
  const startSession = async () => {
    if (!selectedRole) return;
    
    setLoading(true);
    try {
      const response = await api.post('/session/create', {
        role: selectedRole,
        user_id: 'demo-user'
      });
      
      setSessionId(response.data.session_id);
      setCurrentQuestion(response.data.questions[0]);
      setCurrentQuestionIndex(0);
      setPage('practice');
      setUserAnswer('');
      setFeedback(null);
      setSessionAnswers([]);
    } catch (error) {
      console.error('Error starting session:', error);
      alert('Failed to start session: ' + (error.response?.data?.detail || error.message));
    }
    setLoading(false);
  };

  // Start recording audio from microphone
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        
        // Convert audio to base64 for API
        const reader = new FileReader();
        reader.onloadend = async () => {
          const base64Audio = reader.result.split(',')[1];
          await analyzeAudio(base64Audio);
        };
        reader.readAsDataURL(audioBlob);
        
        // Stop all audio tracks
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
      setRecordingTime(0);

      // Start timer that updates every second
      timerIntervalRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
    } catch (error) {
      alert('Microphone access denied. Please enable microphone permissions.');
      console.error('Microphone error:', error);
    }
  };

  // Stop recording and process audio
  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      clearInterval(timerIntervalRef.current);
    }
  };

  // Analyze audio from microphone
  const analyzeAudio = async (audioBase64) => {
    setLoading(true);
    try {
      const response = await api.post('/analysis/audio', {
        audio_base64: audioBase64,
        question: currentQuestion,
        role: selectedRole,
        session_id: sessionId
      });

      setUserAnswer(response.data.transcript);
      setFeedback(response.data);
      
      // Store answer for final report
      setSessionAnswers([...sessionAnswers, {
        question: currentQuestion,
        answer: response.data.transcript,
        feedback: response.data
      }]);
    } catch (error) {
      console.error('Error analyzing audio:', error);
      alert('Failed to analyze audio: ' + (error.response?.data?.detail || error.message));
    }
    setLoading(false);
  };

  // Submit text answer
  const submitAnswer = async () => {
    if (!userAnswer.trim()) {
      alert('Please provide an answer before submitting.');
      return;
    }

    setLoading(true);
    try {
      const response = await api.post('/analysis/text', {
        text: userAnswer,
        question: currentQuestion,
        role: selectedRole,
        session_id: sessionId
      });

      setFeedback(response.data);
      
      // Store answer for final report
      setSessionAnswers([...sessionAnswers, {
        question: currentQuestion,
        answer: userAnswer,
        feedback: response.data
      }]);
    } catch (error) {
      console.error('Error submitting answer:', error);
      alert('Failed to analyze answer: ' + (error.response?.data?.detail || error.message));
    }
    setLoading(false);
  };

  // Move to next question
  const nextQuestion = async () => {
    if (currentQuestionIndex < 4) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setCurrentQuestion(feedback?.next_question || 'Next question');
      setUserAnswer('');
      setFeedback(null);
    } else {
      // All questions done - generate report
      await generateReport();
    }
  };

  // Generate final report
  const generateReport = async () => {
    setLoading(true);
    try {
      const response = await api.post('/report/generate', {
        session_id: sessionId,
        role: selectedRole,
        answers: sessionAnswers
      });

      setSessionReport(response.data);
      setPage('report');
    } catch (error) {
      console.error('Error generating report:', error);
      alert('Failed to generate report: ' + (error.response?.data?.detail || error.message));
    }
    setLoading(false);
  };

  // Reset and go back to landing
  const resetSession = () => {
    setPage('landing');
    setSelectedRole(null);
    setSessionId(null);
    setCurrentQuestion(null);
    setCurrentQuestionIndex(0);
    setUserAnswer('');
    setFeedback(null);
    setSessionAnswers([]);
    setSessionReport(null);
    setIsRecording(false);
    setRecordingTime(0);
  };

  // Format recording time as MM:SS
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  // Play coach feedback as audio
  const playCoachVoice = async (text, feedbackId) => {
    if (isPlaying) return;
    
    try {
      setIsPlaying(true);
      setPlayingFeedback(feedbackId);
      
      const response = await api.post('/tts/speak', {
        text: text,
        voice_id: null
      }, {
        responseType: 'blob'
      });
      
      const audioUrl = URL.createObjectURL(response.data);
      if (audioPlayerRef.current) {
        audioPlayerRef.current.src = audioUrl;
        audioPlayerRef.current.play();
      }
    } catch (error) {
      console.error('Error playing audio:', error);
      alert('Failed to play audio: ' + (error.response?.data?.detail || error.message));
    }
  };

  // Handle audio playback end
  const handleAudioEnd = () => {
    setIsPlaying(false);
    setPlayingFeedback(null);
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1>🎤 VoiceCoach AI</h1>
          {sessionId && (
            <div className="header-info">
              <span>Candidate: Idriss Olivier Bado</span>
              <span>Role: {selectedRole}</span>
            </div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="app-main">
        {/* Landing Page */}
        {page === 'landing' && (
          <div className="page landing-page">
            {/* Hero Section */}
            <section className="hero-section">
              <h2>Master Your Interview Skills with AI Coaching</h2>
              <p>Practice with real-time feedback powered by Mistral AI</p>
              <div className="hero-animation">
                <div className="pulse-dot"></div>
              </div>
            </section>

            {/* Role Selection */}
            <section className="roles-section">
              <h3>Select Your Target Role</h3>
              <div className="roles-grid">
                {roleOptions.map((role) => (
                  <button
                    key={role.name}
                    className={`role-card ${selectedRole === role.name ? 'selected' : ''}`}
                    onClick={() => setSelectedRole(role.name)}
                  >
                    <div className="role-icon">{role.icon}</div>
                    <div className="role-name">{role.name}</div>
                  </button>
                ))}
              </div>
              <button
                className="btn btn-primary"
                onClick={startSession}
                disabled={!selectedRole || loading}
              >
                {loading ? 'Starting...' : 'Start Practice Session'}
              </button>
            </section>

            {/* About Section */}
            <section className="about-section">
              <h3>Platform Founded By</h3>
              <div className="founder-card">
                <div className="about-header">
                  <div className="about-avatar">👔</div>
                  <div className="about-info">
                    <h4>Idriss Olivier Bado</h4>
                    <p className="about-title">Founder & CEO</p>
                    <p className="about-subtitle">Former Head of Data & Software Engineering</p>
                  </div>
                </div>
                <div className="about-bio">
                  <p>
                    Idriss founded VoiceCoach AI to democratize interview preparation. With 15+ years leading data and 
                    engineering teams at Fortune 500 companies, he conducted hundreds of technical interviews and identified 
                    a critical gap: candidates lack real-time, intelligent feedback on their communication skills. VoiceCoach AI 
                    combines his interviewing expertise with advanced AI to provide personalized coaching 24/7.
                  </p>
                </div>
                <div className="expertise-tags">
                  <span className="tag">Data Architecture</span>
                  <span className="tag">Full-Stack Engineering</span>
                  <span className="tag">Engineering Leadership</span>
                  <span className="tag">Interview Methodology</span>
                </div>
              </div>

              <h3 style={{ marginTop: '3rem' }}>Specialized Coaches By Role</h3>
              <div className="coaches-grid">
                <div className="coach-card">
                  <div className="coach-avatar">💻</div>
                  <h4>Alex Chen</h4>
                  <p className="coach-role">Software Engineering Coach</p>
                  <p className="coach-bio">Senior Architect at Google. Specialized in system design, scalability, and technical depth interviews.</p>
                  <div className="coach-tags">
                    <span className="tag-small">System Design</span>
                    <span className="tag-small">Algorithms</span>
                  </div>
                </div>
                <div className="coach-card">
                  <div className="coach-avatar">📊</div>
                  <h4>Maya Patel</h4>
                  <p className="coach-role">Product Manager Coach</p>
                  <p className="coach-bio">Director of Product at Meta. Expert in strategy communication, metrics, and cross-functional thinking.</p>
                  <div className="coach-tags">
                    <span className="tag-small">Strategy</span>
                    <span className="tag-small">Metrics</span>
                  </div>
                </div>
                <div className="coach-card">
                  <div className="coach-avatar">🎨</div>
                  <h4>Jordan Smith</h4>
                  <p className="coach-role">Design Coach</p>
                  <p className="coach-bio">Principal Designer at Apple. Focused on UX thinking, design process, and human-centered problem solving.</p>
                  <div className="coach-tags">
                    <span className="tag-small">UX Thinking</span>
                    <span className="tag-small">Design Process</span>
                  </div>
                </div>
                <div className="coach-card">
                  <div className="coach-avatar">📈</div>
                  <h4>Dr. Rajesh Kumar</h4>
                  <p className="coach-role">Data Science Coach</p>
                  <p className="coach-bio">ML Research Lead at OpenAI. Specializes in statistical thinking, modeling approaches, and insights communication.</p>
                  <div className="coach-tags">
                    <span className="tag-small">Statistics</span>
                    <span className="tag-small">ML Models</span>
                  </div>
                </div>
                <div className="coach-card">
                  <div className="coach-avatar">📱</div>
                  <h4>Sarah Williams</h4>
                  <p className="coach-role">Marketing Coach</p>
                  <p className="coach-bio">VP Growth at Stripe. Expert in go-to-market strategy, customer psychology, and growth metrics.</p>
                  <div className="coach-tags">
                    <span className="tag-small">Growth</span>
                    <span className="tag-small">Strategy</span>
                  </div>
                </div>
              </div>
            </section>

            {/* Features Section */}
            <section className="features-section">
              <div className="feature">
                <div className="feature-icon">🎙️</div>
                <h4>Voice Recording</h4>
                <p>Practice with real microphone or type your answer</p>
              </div>
              <div className="feature">
                <div className="feature-icon">🤖</div>
                <h4>AI Feedback</h4>
                <p>Get instant coaching from Mistral AI</p>
              </div>
              <div className="feature">
                <div className="feature-icon">📊</div>
                <h4>Detailed Report</h4>
                <p>Comprehensive analysis of your performance</p>
              </div>
            </section>
          </div>
        )}

        {/* Practice Page */}
        {page === 'practice' && currentQuestion && (
          <div className="page practice-page">
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${((currentQuestionIndex + 1) / 5) * 100}%` }}
              ></div>
            </div>
            
            <div className="question-container">
              <div className="question-number">Question {currentQuestionIndex + 1} of 5</div>
              <h2 className="question-text">{currentQuestion}</h2>
            </div>

            {!feedback ? (
              <div className="answer-section">
                <div className="answer-input-wrapper">
                  {isRecording ? (
                    <div className="recording-state">
                      <div className="recording-indicator">
                        <span className="pulse-circle"></span>
                        Recording...
                      </div>
                      <div className="recording-time">{formatTime(recordingTime)}</div>
                      <button 
                        className="btn btn-danger"
                        onClick={stopRecording}
                      >
                        Stop Recording
                      </button>
                    </div>
                  ) : (
                    <>
                      <div className="input-tabs">
                        <button className="tab-btn active">🎤 Voice</button>
                        <button className="tab-btn">📝 Type</button>
                      </div>
                      
                      <textarea
                        className="answer-textarea"
                        placeholder="Type your answer here... or use the microphone button below"
                        value={userAnswer}
                        onChange={(e) => setUserAnswer(e.target.value)}
                      ></textarea>

                      <div className="answer-actions">
                        <button
                          className="btn btn-mic"
                          onClick={startRecording}
                          disabled={loading}
                          title="Click to start recording audio"
                        >
                          🎤 Record Answer
                        </button>
                        <button
                          className="btn btn-primary"
                          onClick={submitAnswer}
                          disabled={!userAnswer.trim() || loading}
                        >
                          {loading ? 'Analyzing...' : 'Submit Answer'}
                        </button>
                      </div>
                    </>
                  )}
                </div>
              </div>
            ) : (
              <div className="feedback-section">
                <h3>AI Coaching Feedback</h3>
                
                <div className="feedback-card">
                  <h4>Your Answer</h4>
                  <p className="answer-text">{userAnswer}</p>
                </div>

                {feedback.overall_score !== undefined && (
                  <div className="scores-grid">
                    <div className="score-box">
                      <div className="score-label">Overall Score</div>
                      <div className="score-value">{feedback.overall_score}/10</div>
                    </div>
                    {feedback.scores && (
                      <>
                        <div className="score-box">
                          <div className="score-label">Clarity</div>
                          <div className="score-value">{feedback.scores.clarity || 'N/A'}</div>
                        </div>
                        <div className="score-box">
                          <div className="score-label">Structure</div>
                          <div className="score-value">{feedback.scores.structure || 'N/A'}</div>
                        </div>
                        <div className="score-box">
                          <div className="score-label">Impact</div>
                          <div className="score-value">{feedback.scores.impact || 'N/A'}</div>
                        </div>
                      </>
                    )}
                  </div>
                )}

                {feedback.feedback && (
                  <div className="feedback-card">
                    <div className="feedback-header">
                      <h4>Coaching Tips</h4>
                      <button
                        className={`btn btn-voice ${isPlaying && playingFeedback === 'coaching' ? 'playing' : ''}`}
                        onClick={() => playCoachVoice(feedback.feedback, 'coaching')}
                        disabled={isPlaying}
                        title="Listen to coaching tips"
                      >
                        {isPlaying && playingFeedback === 'coaching' ? '🔊 Playing...' : '🔉 Hear Coach'}
                      </button>
                    </div>
                    <p>{feedback.feedback}</p>
                  </div>
                )}

                {feedback.filler_words && feedback.filler_words.length > 0 && (
                  <div className="feedback-card warning">
                    <h4>Filler Words Detected</h4>
                    <div className="filler-list">
                      {feedback.filler_words.map((item, idx) => (
                        <span key={idx} className="filler-item">
                          "{item.word}" ({item.count}x)
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {currentQuestionIndex < 4 ? (
                  <button
                    className="btn btn-primary"
                    onClick={() => {
                      setFeedback(null);
                      setUserAnswer('');
                      nextQuestion();
                    }}
                  >
                    Next Question →
                  </button>
                ) : (
                  <button
                    className="btn btn-primary"
                    onClick={async () => {
                      await generateReport();
                    }}
                  >
                    Generate Final Report
                  </button>
                )}
              </div>
            )}
          </div>
        )}

        {/* Report Page */}
        {page === 'report' && sessionReport && (
          <div className="page report-page">
            <h2>Your Interview Report</h2>
            
            <div className="report-card">
              <h3>{selectedRole}</h3>
              <p className="report-date">
                {new Date().toLocaleDateString()} • {sessionAnswers.length} questions answered
              </p>
            </div>

            {sessionReport.overall_score !== undefined && (
              <div className="overall-score">
                <div className="score-ring">
                  <div className="score-text">{sessionReport.overall_score}</div>
                  <div className="score-label">Overall</div>
                </div>
              </div>
            )}

            {sessionReport.summary && (
              <div className="report-card">
                <h4>Summary</h4>
                <p>{sessionReport.summary}</p>
              </div>
            )}

            {sessionReport.strengths && (
              <div className="report-card success">
                <h4>Your Strengths</h4>
                <ul>
                  {(Array.isArray(sessionReport.strengths) ? sessionReport.strengths : [sessionReport.strengths]).map((strength, idx) => (
                    <li key={idx}>✓ {strength}</li>
                  ))}
                </ul>
              </div>
            )}

            {sessionReport.improvements && (
              <div className="report-card warning">
                <h4>Areas for Improvement</h4>
                <ul>
                  {(Array.isArray(sessionReport.improvements) ? sessionReport.improvements : [sessionReport.improvements]).map((improvement, idx) => (
                    <li key={idx}>→ {improvement}</li>
                  ))}
                </ul>
              </div>
            )}

            {sessionReport.tips && (
              <div className="report-card">
                <h4>Next Steps</h4>
                <p>{sessionReport.tips}</p>
              </div>
            )}

            <button
              className="btn btn-primary"
              onClick={resetSession}
            >
              Start New Session
            </button>
          </div>
        )}
      </main>

      {/* Hidden audio player for TTS */}
      <audio 
        ref={audioPlayerRef}
        onEnded={handleAudioEnd}
        style={{ display: 'none' }}
      />
    </div>
  );
}

export default App;
