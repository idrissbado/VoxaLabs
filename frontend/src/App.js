import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import { MathTutor } from './MathTutor';
import {
  FiMic, FiStopCircle, FiPlay, FiPause, FiCheck,
  FiDownload, FiRefreshCw, FiVolume2, FiSettings,
  FiBarChart2, FiTrendingUp, FiCode, FiLayout,
  FiLoader, FiCheckCircle, FiAlertCircle, FiEdit, FiAward,
  FiTarget, FiZap, FiArrowRight, FiArrowLeft, FiChevronsRight,
  FiLinkedin, FiUser, FiHome, FiBookOpen
} from 'react-icons/fi';

const API_BASE = typeof window !== 'undefined' && window.location.hostname !== 'localhost' 
  ? '' 
  : 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Simple logger for debugging
const logger = (message) => {
  console.log(`[VoxaLab] ${message}`);
};

function App() {
  const [page, setPage] = useState('landing');
  const [mode, setMode] = useState('interview'); // 'interview' or 'math'
  const [selectedRole, setSelectedRole] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [userAnswer, setUserAnswer] = useState('');
  const [inputMethod, setInputMethod] = useState('typing');
  const [transcript, setTranscript] = useState('');
  const [sessionAnswers, setSessionAnswers] = useState([]);
  const [sessionReport, setSessionReport] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playingFeedback, setPlayingFeedback] = useState(null);
  const [recordedAudioBlob, setRecordedAudioBlob] = useState(null);
  const [recordedAudioUrl, setRecordedAudioUrl] = useState(null);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [allQuestions, setAllQuestions] = useState([]);
  const [error, setError] = useState(null);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerIntervalRef = useRef(null);
  const audioPlayerRef = useRef(null);

  const roleOptions = [
    { id: 'java', name: 'Java Backend', icon: FiCode, color: '#FF6B6B', gradient: 'from-red-500 to-pink-600' },
    { id: 'frontend', name: 'Frontend Engineer', icon: FiLayout, color: '#4ECDC4', gradient: 'from-cyan-500 to-blue-600' },
    { id: 'devops', name: 'DevOps Engineer', icon: FiSettings, color: '#45B7D1', gradient: 'from-blue-500 to-indigo-600' },
    { id: 'data', name: 'Data Scientist', icon: FiBarChart2, color: '#96CEB4', gradient: 'from-green-500 to-emerald-600' },
    { id: 'pm', name: 'Product Manager', icon: FiTrendingUp, color: '#FFEAA7', gradient: 'from-amber-400 to-orange-600' }
  ];

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'fr', name: 'Français' },
    { code: 'es', name: 'Español' },
    { code: 'de', name: 'Deutsch' },
    { code: 'zh', name: '中文' },
    { code: 'ja', name: '日本語' }
  ];

  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const startSession = async (role) => {
    try {
      setLoading(true);
      setError(null);
      setSelectedRole(role);
      setCurrentQuestionIndex(0);
      setUserAnswer('');
      setTranscript('');
      setFeedback(null);
      setSessionAnswers([]);

      const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      setSessionId(newSessionId);

      const response = await api.get(`/session/questions`, {
        params: { role, language: selectedLanguage }
      });

      const questions = response.data.questions || [];
      setAllQuestions(questions);
      
      if (questions.length > 0) {
        setCurrentQuestion(questions[0]);
        setPage('practice');
      } else {
        setError('No questions available for this role.');
      }
    } catch (err) {
      setError('Failed to start session: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioChunksRef.current = [];
      
      const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        setRecordedAudioBlob(audioBlob);
        setRecordedAudioUrl(URL.createObjectURL(audioBlob));
      };

      mediaRecorder.start();
      setIsRecording(true);
      setRecordingTime(0);

      timerIntervalRef.current = setInterval(() => {
        setRecordingTime((prev) => prev + 1);
      }, 1000);
    } catch (err) {
      setError('Microphone access denied: ' + err.message);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
      clearInterval(timerIntervalRef.current);
    }
  };

  const transcribeAudio = async () => {
    if (!recordedAudioBlob) {
      setError('No audio recorded');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const formData = new FormData();
      formData.append('file', recordedAudioBlob, 'audio.webm');
      formData.append('language', selectedLanguage);

      const response = await api.post('/analysis/transcribe', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      setTranscript(response.data.transcript || 'No speech detected');
      setUserAnswer(response.data.transcript || '');
      setInputMethod('typing');
      logger('✓ Audio transcribed successfully');
    } catch (err) {
      logger('✗ Transcription failed: ' + (err.response?.data?.detail || err.message));
      setError('Audio transcription is currently unavailable. Please type your answer instead.');
      // Allow user to type answer as fallback
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = async () => {
    if (!userAnswer.trim()) {
      setError('Please provide an answer');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      logger(`Submitting answer for question: ${currentQuestion?.substring(0, 50)}...`);
      logger(`User role: ${selectedRole?.name}, Language: ${selectedLanguage}`);

      const response = await api.post('/session/answer', {
        session_id: sessionId,
        question: currentQuestion,
        user_answer: userAnswer,
        language: selectedLanguage,
        role: selectedRole?.name || selectedRole
      });

      logger('✓ Answer submitted successfully');
      console.log('Coaching feedback received:', response.data);
      
      setFeedback(response.data);
      setSessionAnswers([...sessionAnswers, { question: currentQuestion, answer: userAnswer, score: response.data.score || 0 }]);
      
      if (!response.data.score && !response.data.feedback) {
        logger('⚠️ Warning: No feedback received. This might indicate an API issue.');
        setError('Got response but feedback is incomplete. Showing what we have...');
      }
    } catch (err) {
      logger('✗ Error submitting answer: ' + (err.response?.data?.detail || err.message));
      console.error('Full error:', err);
      setError('Failed to submit answer: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const nextQuestion = () => {
    if (currentQuestionIndex < allQuestions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setCurrentQuestion(allQuestions[currentQuestionIndex + 1]);
      setUserAnswer('');
      setTranscript('');
      setFeedback(null);
      setRecordedAudioUrl(null);
      setInputMethod('typing');
    } else {
      generateReport();
    }
  };

  const generateReport = async () => {
    try {
      setLoading(true);
      const response = await api.post('/report/generate', {
        session_id: sessionId,
        answers: sessionAnswers
      });
      setSessionReport(response.data);
      setPage('report');
    } catch (err) {
      setError('Failed to generate report: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const playCoachVoice = async () => {
    if (!feedback?.tips) return;

    try {
      setIsPlaying(true);
      setPlayingFeedback(feedback);

      const response = await api.post('/tts/speak', {
        text: feedback.tips,
        voice_id: 'default'
      }, {
        responseType: 'blob'
      });

      const audioUrl = URL.createObjectURL(response.data);
      audioPlayerRef.current = new Audio(audioUrl);
      audioPlayerRef.current.onended = () => setIsPlaying(false);
      audioPlayerRef.current.play();
    } catch (err) {
      setError('TTS failed: ' + err.message);
      setIsPlaying(false);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="app-container" style={{ '--mouse-x': `${mousePosition.x}px`, '--mouse-y': `${mousePosition.y}px` }}>
      <div className="animated-background">
        <div className="gradient-orb orb-1"></div>
        <div className="gradient-orb orb-2"></div>
        <div className="gradient-orb orb-3"></div>
        <div className="grid-overlay"></div>
      </div>

      {page === 'landing' && (
        <div className="landing-page">
          <nav className="navbar">
            <div className="nav-brand">
              <FiCode className="ai-icon" />
              <span>PrepCoach</span>
            </div>
            <div className="nav-links">
              <button 
                className="nav-link" 
                onClick={() => setPage('landing')}
                title="Home"
              >
                <FiHome size={20} />
              </button>
              <button 
                className="nav-link" 
                onClick={() => setPage('about')}
                title="About"
              >
                <FiUser size={20} />
              </button>
            </div>
            <div className="nav-language-selector">
              <select 
                value={selectedLanguage} 
                onChange={(e) => setSelectedLanguage(e.target.value)}
                className="language-dropdown"
              >
                {languages.map(lang => (
                  <option key={lang.code} value={lang.code}>{lang.name}</option>
                ))}
              </select>
            </div>
          </nav>

          <div className="landing-content">
            <div className="coaching-modes-section">
              <h2 className="section-title">Choose Your Coaching Mode</h2>
              <div className="coaching-modes-grid">
                <div 
                  className="coaching-mode-card interview-mode"
                  onClick={() => setPage('landing')}
                >
                  <div className="mode-icon">🎤</div>
                  <h3>Interview Coach</h3>
                  <p>Master interview skills for tech and non-tech roles</p>
                </div>
                <div 
                  className="coaching-mode-card math-mode"
                  onClick={() => setPage('math')}
                >
                  <div className="mode-icon">📐</div>
                  <h3>Math Tutor</h3>
                  <p>Solve complex mathematics with step-by-step guidance</p>
                </div>
                <div 
                  className="coaching-mode-card finance-mode"
                  onClick={() => alert('Finance Coach coming soon!')}
                >
                  <div className="mode-icon">💰</div>
                  <h3>Finance Coach</h3>
                  <p>Excel in finance interviews and investment analysis</p>
                </div>
                <div 
                  className="coaching-mode-card advisor-mode"
                  onClick={() => alert('Personal Advisor coming soon!')}
                >
                  <div className="mode-icon">🎯</div>
                  <h3>Personal Advisor</h3>
                  <p>Get career guidance and personalized coaching</p>
                </div>
              </div>
            </div>

            <div className="hero-section">
              <div className="hero-text">
                <h1 className="hero-title">Master Your <span className="gradient-text">Interview Skills</span></h1>
                <p className="hero-subtitle">Real-time AI coaching powered by advanced voice analysis and personalized feedback</p>
              </div>

              <div className="features-showcase">
                <div className="feature-item">
                  <FiMic className="feature-icon" />
                  <div className="feature-text">
                    <h3>Voice Recognition</h3>
                    <p>Speak naturally or type your answers</p>
                  </div>
                </div>
                <div className="feature-item">
                  <FiZap className="feature-icon" />
                  <div className="feature-text">
                    <h3>Instant Feedback</h3>
                    <p>AI-powered coaching in seconds</p>
                  </div>
                </div>
                <div className="feature-item">
                  <FiAward className="feature-icon" />
                  <div className="feature-text">
                    <h3>Score & Analysis</h3>
                    <p>Detailed performance metrics</p>
                  </div>
                </div>
                <div className="feature-item">
                  <FiVolume2 className="feature-icon" />
                  <div className="feature-text">
                    <h3>Voice Coaching</h3>
                    <p>Hear feedback spoken naturally</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="roles-container">
              <h2 className="section-title">Choose Your Role</h2>
              <div className="roles-grid">
                {roleOptions.map((role) => {
                  const IconComponent = role.icon;
                  return (
                    <div
                      key={role.id}
                      className={`role-card ${selectedRole?.id === role.id ? 'selected' : ''}`}
                      onClick={() => setSelectedRole(role)}
                    >
                      <div className={`role-icon-wrapper bg-gradient-to-br ${role.gradient}`}>
                        <IconComponent size={32} />
                      </div>
                      <h3>{role.name}</h3>
                      <FiArrowRight className="role-arrow" />
                    </div>
                  );
                })}
              </div>
            </div>

            {selectedRole && (
              <div className="start-session-wrapper">
                <button 
                  className="start-button"
                  onClick={() => startSession(selectedRole.id)}
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <FiLoader className="spin" />
                      Starting...
                    </>
                  ) : (
                    <>
                      Start Interview Practice
                      <FiChevronsRight />
                    </>
                  )}
                </button>
              </div>
            )}

            {error && (
              <div className="error-banner">
                <FiAlertCircle />
                <span>{error}</span>
              </div>
            )}
          </div>
        </div>
      )}

      {page === 'practice' && currentQuestion && (
        <div className="practice-page">
          <div className="practice-header">
            <button className="back-button" onClick={() => setPage('landing')}>
              <FiArrowLeft /> Back
            </button>
            <div className="progress-info">
              <span className="question-counter">Question {currentQuestionIndex + 1} of {allQuestions.length}</span>
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${((currentQuestionIndex + 1) / allQuestions.length) * 100}%` }}></div>
              </div>
            </div>
          </div>

          <div className="practice-content">
            <div className="question-panel">
              <div className="question-header">
                <FiTarget className="question-icon" />
                <h2>Your Question</h2>
              </div>
              <p className="question-text">{currentQuestion}</p>
            </div>

            <div className="answer-panel">
              <div className="input-method-tabs">
                <button 
                  className={`method-tab ${inputMethod === 'typing' ? 'active' : ''}`}
                  onClick={() => setInputMethod('typing')}
                >
                  <FiEdit size={18} />
                  Type Answer
                </button>
                <button 
                  className={`method-tab ${inputMethod === 'recording' ? 'active' : ''}`}
                  onClick={() => setInputMethod('recording')}
                >
                  <FiMic size={18} />
                  Record Answer
                </button>
              </div>

              {inputMethod === 'typing' ? (
                <div className="typing-input">
                  <textarea
                    className="answer-textarea"
                    value={userAnswer}
                    onChange={(e) => setUserAnswer(e.target.value)}
                    placeholder="Type your answer here... Share your thoughts, experiences, and approach to this question."
                  />
                  <div className="char-count">{userAnswer.length} characters</div>
                </div>
              ) : (
                <div className="recording-input">
                  <div className={`recording-visualizer ${isRecording ? 'recording' : ''}`}>
                    <div className="recording-circle"></div>
                    <div className="recording-waveform">
                      {[...Array(12)].map((_, i) => (
                        <div key={i} className="wave-bar"></div>
                      ))}
                    </div>
                    <span className="recording-time">{formatTime(recordingTime)}</span>
                  </div>

                  <div className="recording-buttons">
                    {!isRecording ? (
                      <button className="record-start" onClick={startRecording}>
                        <FiMic /> Start Recording
                      </button>
                    ) : (
                      <button className="record-stop" onClick={stopRecording}>
                        <FiStopCircle /> Stop Recording
                      </button>
                    )}
                  </div>

                  {recordedAudioUrl && (
                    <div className="recorded-audio-preview">
                      <audio ref={audioPlayerRef} src={recordedAudioUrl} className="audio-player" />
                      <div className="audio-controls">
                        <button onClick={() => audioPlayerRef.current?.play()} className="play-btn">
                          <FiPlay /> Play
                        </button>
                        <button onClick={() => audioPlayerRef.current?.pause()} className="pause-btn">
                          <FiPause /> Pause
                        </button>
                      </div>
                    </div>
                  )}

                  {isRecording === false && recordedAudioUrl && (
                    <button className="transcribe-btn" onClick={transcribeAudio} disabled={loading}>
                      {loading ? <FiLoader className="spin" /> : <FiVolume2 />}
                      Transcribe & Use
                    </button>
                  )}

                  {transcript && (
                    <div className="transcript-display">
                      <p className="transcript-label">Transcribed text:</p>
                      <p className="transcript-text">{transcript}</p>
                    </div>
                  )}
                </div>
              )}

              {error && (
                <div className="error-message">
                  <FiAlertCircle />
                  {error}
                </div>
              )}

              <button 
                className="submit-button"
                onClick={submitAnswer}
                disabled={loading || !userAnswer.trim()}
              >
                {loading ? (
                  <>
                    <FiLoader className="spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <FiCheck />
                    Submit Answer
                  </>
                )}
              </button>
            </div>
          </div>

          {feedback && (
            <div className="feedback-panel">
              <div className="feedback-header-section">
                <div className="score-display">
                  <div className="score-circle">
                    <span className="score-number">{feedback.score}</span>
                    <span className="score-max">/100</span>
                  </div>
                  <div className="score-info">
                    <h3>{feedback.feedback}</h3>
                    <p className="score-label">Performance Rating</p>
                  </div>
                </div>
              </div>

              <div className="feedback-content">
                <div className="feedback-section">
                  <h4 className="feedback-title">Coaching Tips</h4>
                  <p className="feedback-text">{feedback.tips}</p>
                </div>

                <div className="feedback-actions">
                  <button className="voice-button" onClick={playCoachVoice} disabled={isPlaying}>
                    <FiVolume2 />
                    {isPlaying ? 'Listening...' : 'Hear Coach Voice'}
                  </button>
                </div>

                <button className="next-button" onClick={nextQuestion}>
                  {currentQuestionIndex === allQuestions.length - 1 ? (
                    <>
                      <FiCheckCircle /> Finish & See Report
                    </>
                  ) : (
                    <>
                      Next Question <FiArrowRight />
                    </>
                  )}
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {page === 'report' && sessionReport && (
        <div className="report-page">
          <div className="report-header">
            <h1>Your Interview Report</h1>
            <p>Comprehensive analysis of your performance</p>
          </div>

          <div className="report-cards">
            <div className="report-card summary-card">
              <h3>Overall Performance</h3>
              <div className="summary-stats">
                <div className="stat">
                  <span className="stat-label">Average Score</span>
                  <span className="stat-value">{sessionReport.average_score?.toFixed(1) || 'N/A'}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Questions Answered</span>
                  <span className="stat-value">{sessionAnswers.length}</span>
                </div>
              </div>
            </div>

            <div className="report-card details-card">
              <h3>Detailed Breakdown</h3>
              <div className="report-details">
                {sessionAnswers.map((answer, idx) => (
                  <div key={idx} className="answer-item">
                    <div className="answer-number">{idx + 1}</div>
                    <div className="answer-info">
                      <p className="answer-q">{answer.question}</p>
                      <p className="answer-score">Score: {answer.score}/100</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="report-actions">
            <button className="action-button" onClick={() => { setPage('landing'); setSelectedRole(null); }}>
              <FiRefreshCw /> Practice Again
            </button>
            <button className="action-button download-button" onClick={() => alert('Download feature coming soon!')}>
              <FiDownload /> Download Report
            </button>
          </div>
        </div>
      )}

      {page === 'about' && (
        <div className="about-page">
          <nav className="navbar">
            <div className="nav-brand">
              <FiCode className="ai-icon" />
              <span>PrepCoach</span>
            </div>
            <div className="nav-links">
              <button 
                className="nav-link" 
                onClick={() => setPage('landing')}
                title="Home"
              >
                <FiHome size={20} />
              </button>
            </div>
          </nav>

          <div className="about-content">
            <div className="about-container">
              <div className="about-profile">
                <div className="profile-card-header">
                  <div className="profile-avatar">👨‍💼</div>
                  <div className="profile-header-info">
                    <h1 className="profile-name">Idriss Olivier Bado</h1>
                    <p className="profile-title">AI Engineer & PrepCoach Creator</p>
                  </div>
                </div>
                
                <div className="profile-bio">
                    <p>
                      I'm passionate about leveraging AI and machine learning to revolutionize how people prepare for critical moments in their careers. PrepCoach is built with the belief that everyone deserves access to world-class coaching and personalized feedback.
                    </p>
                    <p>
                      With expertise in full-stack development, AI integration, and product design, I've created PrepCoach to bridge the gap between traditional coaching and cutting-edge AI technology.
                    </p>
                </div>

                <div className="about-mission">
                  <h2>Our Mission</h2>
                  <p>
                    PrepCoach empowers learners and professionals worldwide by providing intelligent, personalized coaching for interviews, career development, exam preparation, and skill training. We believe that preparation should be accessible, engaging, and effective for everyone.
                  </p>
                </div>

                <div className="about-features-section">
                  <h2>Platform Features</h2>
                  
                  <div className="features-grid">
                      <div className="feature-card">
                        <div className="feature-icon-large">🎤</div>
                        <h3>Interview Coach</h3>
                        <p>Real-time AI coaching for multiple professional roles including Java Backend, Frontend, DevOps, Data Science, and Product Manager positions. Get instant feedback on your answers with voice recognition and detailed analysis.</p>
                        <ul className="feature-list">
                          <li>✓ Multiple role-based interviews</li>
                          <li>✓ Voice and text input modes</li>
                          <li>✓ Real-time transcription</li>
                          <li>✓ Detailed performance reports</li>
                          <li>✓ Multi-language support</li>
                        </ul>
                      </div>

                      <div className="feature-card">
                        <div className="feature-icon-large">📐</div>
                        <h3>Math Tutor</h3>
                        <p>Advanced mathematical problem solver and step-by-step tutor powered by Mistral Large 3. Perfect for learning complex mathematics through guided problem-solving and detailed explanations with LaTeX formatting.</p>
                        <ul className="feature-list">
                          <li>✓ Problem analysis & classification</li>
                          <li>✓ Step-by-step validation</li>
                          <li>✓ LaTeX solution generation</li>
                          <li>✓ Practice problem generation</li>
                          <li>✓ Learning insights & guidance</li>
                        </ul>
                      </div>

                      <div className="feature-card">
                        <div className="feature-icon-large">💰</div>
                        <h3>Finance Coach</h3>
                        <p>Specialized coaching for finance interviews and financial analysis. Get expert guidance on investment strategies, financial modeling, case studies, and market analysis with real-world scenarios.</p>
                        <ul className="feature-list">
                          <li>✓ Finance interview prep</li>
                          <li>✓ Investment analysis</li>
                          <li>✓ Financial modeling guidance</li>
                          <li>✓ Case study walkthroughs</li>
                          <li>✓ Market insights</li>
                        </ul>
                      </div>
                    </div>
                  </div>

                <div className="profile-features">
                  <h2>My Expertise</h2>
                  <div className="expertise-grid">
                    <div className="feature">
                      <FiCode size={24} />
                      <div>
                        <h3>Full-Stack Development</h3>
                        <p>React, Python, FastAPI, Machine Learning</p>
                      </div>
                    </div>
                    <div className="feature">
                      <FiZap size={24} />
                      <div>
                        <h3>AI Integration</h3>
                        <p>Mistral Large 3, Whisper, LangChain</p>
                      </div>
                    </div>
                    <div className="feature">
                      <FiTarget size={24} />
                      <div>
                        <h3>Product Design</h3>
                        <p>User-centric, scalable platforms</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="profile-cta">
                  <a 
                    href="https://www.linkedin.com/in/idriss-olivier-bado/" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="linkedin-link"
                  >
                    <FiLinkedin size={24} />
                    <span>Connect on LinkedIn</span>
                  </a>
                </div>

                <div className="about-tech">
                  <h2>Technology Stack</h2>
                  <div className="tech-grid">
                    <div className="tech-item">
                      <strong>Frontend</strong>
                      <p>React 18, Tailwind CSS, Web Audio API</p>
                    </div>
                    <div className="tech-item">
                      <strong>Backend</strong>
                      <p>FastAPI, Python, Uvicorn</p>
                    </div>
                    <div className="tech-item">
                      <strong>AI/ML</strong>
                      <p>Mistral Large 3, Whisper, LangChain</p>
                    </div>
                    <div className="tech-item">
                      <strong>Deployment</strong>
                      <p>Docker, Hugging Face Spaces</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {page === 'math' && (
        <MathTutor onBack={() => setPage('landing')} />
      )}
    </div>
  );
}

export default App;
