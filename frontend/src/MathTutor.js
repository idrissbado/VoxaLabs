import React, { useState } from 'react';
import axios from 'axios';
import {
  FiArrowRight, FiArrowLeft, FiCheck, FiRefreshCw,
  FiLoader, FiAlertCircle, FiCheckCircle, FiEdit,
  FiDownload, FiHome, FiCode
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

export function MathTutor({ onBack }) {
  const [phase, setPhase] = useState('input');
  const [problem, setProblem] = useState('');
  const [problemAnalysis, setProblemAnalysis] = useState(null);
  const [studentSteps, setStudentSteps] = useState([]);
  const [currentStep, setCurrentStep] = useState('');
  const [stepFeedback, setStepFeedback] = useState(null);
  const [finalSolution, setFinalSolution] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [stepNumber, setStepNumber] = useState(1);
  const [hint, setHint] = useState(null);
  const [showingHint, setShowingHint] = useState(false);
  const [downloadFormat, setDownloadFormat] = useState('markdown');

  const analyzeProblem = async () => {
    if (!problem.trim()) {
      setError('Please enter a math problem');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await api.post('/math/analyze', {
        problem_text: problem
      });

      setProblemAnalysis(response.data);
      setPhase('solving');
      setStudentSteps([]);
      setCurrentStep('');
      setStepNumber(1);
      setStepFeedback(null);
      
      // Automatically get hint for this problem
      try {
        const hintResponse = await api.post('/math/hint', {
          problem_text: problem,
          student_progress: 'Just started'
        });
        setHint(hintResponse.data);
        setShowingHint(true);
      } catch (hintErr) {
        console.error('Error getting hint:', hintErr);
      }
    } catch (err) {
      setError('Error: ' + (err.response?.data?.detail || err.message));
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const submitStep = async () => {
    if (!currentStep.trim()) {
      setError('Please enter your step');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const context = studentSteps.length > 0 
        ? studentSteps.map(s => `Step ${s.number}: ${s.step}`).join('\n')
        : '';

      const response = await api.post('/math/validate-step', {
        problem_text: problem,
        step_number: stepNumber,
        student_step: currentStep,
        context: context
      });

      setStepFeedback(response.data);
      
      if (response.data.is_correct) {
        setStudentSteps([...studentSteps, { number: stepNumber, step: currentStep }]);
        setCurrentStep('');
        setStepNumber(stepNumber + 1);
        setShowingHint(false); // Hide hint after correct step
        
        // Get updated hint for next step
        try {
          const progressText = `Completed ${studentSteps.length + 1} steps`;
          const hintResponse = await api.post('/math/hint', {
            problem_text: problem,
            student_progress: progressText
          });
          setHint(hintResponse.data);
          setShowingHint(true);
        } catch (hintErr) {
          console.error('Error getting hint:', hintErr);
        }
      }
    } catch (err) {
      setError('Error validating step: ' + (err.response?.data?.detail || err.message));
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const finishProblem = async () => {
    const studentSolution = studentSteps.map(s => s.step).join('\n');

    try {
      setLoading(true);
      setError(null);

      const response = await api.post('/math/generate-solution', {
        problem_text: problem,
        student_solution: studentSolution
      });
      setFinalSolution(response.data);

      setPhase('solution');
    } catch (err) {
      setError('Failed to generate solution: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const requestHint = async () => {
    // No longer needed - hints are automatic after each step
  };

  const downloadSolution = async (format) => {
    try {
      setLoading(true);
      setError(null);

      const response = await api.post('/math/download', {
        problem_text: problem,
        solution_data: finalSolution,
        format_type: format
      });

      const data = response.data;
      const element = document.createElement('a');
      const file = new Blob([data.content], { type: data.mime_type });
      element.href = URL.createObjectURL(file);
      element.download = data.filename;
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    } catch (err) {
      setError('Error downloading solution: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const resetProblem = () => {
    setProblem('');
    setProblemAnalysis(null);
    setStudentSteps([]);
    setCurrentStep('');
    setStepFeedback(null);
    setFinalSolution(null);
    setPhase('input');
    setError(null);
    setStepNumber(1);
    setHint(null);
    setShowingHint(false);
  };

  return (
    <div className="math-tutor-container">
      <nav className="navbar">
        <div className="nav-brand">
          <FiCode className="ai-icon" />
          <span>PrepCoach - Math Tutor</span>
        </div>
        <button 
          className="nav-back-button"
          onClick={onBack}
          title="Back to Home"
        >
          <FiHome size={20} />
        </button>
      </nav>

      <div className="math-content">
        {error && (
          <div className="error-banner">
            <FiAlertCircle size={20} />
            <span>{error}</span>
            <button onClick={() => setError(null)}>×</button>
          </div>
        )}

        {phase === 'input' && (
          <div className="math-phase phase-input">
            <div className="phase-header">
              <h1>Math Problem Solver</h1>
              <p>Submit any math problem for step-by-step guidance and validation</p>
            </div>

            <div className="problem-input-section">
              <label htmlFor="problem-text">Enter your math problem:</label>
              <textarea
                id="problem-text"
                value={problem}
                onChange={(e) => setProblem(e.target.value)}
                placeholder="e.g., Solve for x: 2x + 5 = 13"
                rows="6"
                className="problem-textarea"
              />

              <div className="input-hints">
                <p><strong>Examples:</strong></p>
                <ul>
                  <li>Solve for x: 3x - 7 = 20</li>
                  <li>Find the derivative of f(x) = x³ + 2x</li>
                  <li>Solve: √(2x) = 4</li>
                  <li>Factor: x² + 5x + 6</li>
                </ul>
              </div>

              <button
                className="submit-button"
                onClick={analyzeProblem}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <FiLoader className="spinner" /> Analyzing...
                  </>
                ) : (
                  <>
                    <FiArrowRight /> Start Solving
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {phase === 'solving' && problemAnalysis && (
          <div className="math-phase phase-solving">
            <div className="problem-info-panel">
              <h2>Problem Analysis</h2>
              <div className="analysis-grid">
                <div className="analysis-item">
                  <strong>Topic:</strong>
                  <p>{problemAnalysis.topic} - {problemAnalysis.subtopic}</p>
                </div>
                <div className="analysis-item">
                  <strong>Difficulty:</strong>
                  <p>{"★".repeat(problemAnalysis.difficulty)}{"☆".repeat(5 - problemAnalysis.difficulty)}</p>
                </div>
                <div className="analysis-item full-width">
                  <strong>Key Concepts:</strong>
                  <div className="concepts-tags">
                    {problemAnalysis.required_concepts.map((concept, idx) => (
                      <span key={idx} className="concept-tag">{concept}</span>
                    ))}
                  </div>
                </div>
              </div>

              <div className="first-question-box">
                <strong>First Question:</strong>
                <p>{problemAnalysis.first_question}</p>
              </div>
            </div>

            {showingHint && hint && (
              <div className="hint-display initial-hint">
                <div className="hint-header">
                  <h3>💡 Guidance to Get Started (Level {hint.hint_level}/5)</h3>
                  <button 
                    className="close-hint"
                    onClick={() => setShowingHint(false)}
                    title="Dismiss hint"
                  >
                    ×
                  </button>
                </div>
                <div className="hint-content">
                  <p><strong>💭 Hint:</strong> {hint.hint}</p>
                  <p><strong>🎯 Strategy:</strong> {hint.guidance}</p>
                  <div className="next-steps">
                    <strong>📋 Suggested approach:</strong>
                    <ul>
                      {hint.next_steps && hint.next_steps.map((step, idx) => (
                        <li key={idx}>{step}</li>
                      ))}
                    </ul>
                  </div>
                  {hint.common_error_to_avoid && (
                    <div className="warning-box">
                      <strong>⚠️ Common mistake to avoid:</strong> {hint.common_error_to_avoid}
                    </div>
                  )}
                </div>
              </div>
            )}

            <div className="steps-container">
              <h2>Your Steps</h2>

              {studentSteps.length > 0 && (
                <div className="completed-steps">
                  {studentSteps.map((s, idx) => (
                    <div key={idx} className="step-card completed">
                      <div className="step-header">
                        <div className="step-number">
                          <FiCheckCircle /> Step {s.number}
                        </div>
                      </div>
                      <div className="step-content">{s.step}</div>
                    </div>
                  ))}
                </div>
              )}

              <div className="step-input-section">
                <label>Step {stepNumber}:</label>
                <textarea
                  value={currentStep}
                  onChange={(e) => setCurrentStep(e.target.value)}
                  placeholder="Enter your next step..."
                  rows="4"
                  className="step-textarea"
                  onKeyDown={(e) => {
                    if (e.ctrlKey && e.key === 'Enter') {
                      submitStep();
                    }
                  }}
                />

                {stepFeedback && (
                  <div className={`feedback-box ${stepFeedback.is_correct ? 'correct' : 'incorrect'}`}>
                    <div className="feedback-header">
                      {stepFeedback.is_correct ? (
                        <>
                          <FiCheckCircle size={20} />
                          <strong>✓ Correct!</strong>
                        </>
                      ) : (
                        <>
                          <FiAlertCircle size={20} />
                          <strong>⚠ Let's review this step</strong>
                        </>
                      )}
                    </div>
                    <p className="coaching-feedback"><strong>Coach says:</strong> {stepFeedback.feedback || stepFeedback.explanation || 'Good work on this step!'}</p>
                    {stepFeedback.error_type && (
                      <p className="error-type"><strong>Note:</strong> {stepFeedback.error_type}</p>
                    )}
                    {stepFeedback.explanation && (
                      <p className="explanation">{stepFeedback.explanation}</p>
                    )}
                    {stepFeedback.hint && (
                      <div className="hint-box">
                        <strong>💡 Hint for next step:</strong> {stepFeedback.hint}
                      </div>
                    )}
                    {stepFeedback.reasoning_quality_score && (
                      <div className="confidence-meter">
                        <span>Reasoning Quality: {stepFeedback.reasoning_quality_score}/10</span>
                        <div className="meter">
                          <div 
                            className="meter-fill" 
                            style={{width: `${stepFeedback.reasoning_quality_score * 10}%`}}
                          />
                        </div>
                      </div>
                    )}
                  </div>
                )}

                <div className="step-actions">
                  <button
                    className="submit-button"
                    onClick={submitStep}
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <FiLoader className="spinner" /> Validating...
                      </>
                    ) : (
                      <>
                        <FiCheck /> Validate Step
                      </>
                    )}
                  </button>

                  {studentSteps.length > 0 && (
                    <button
                      className="finish-button"
                      onClick={finishProblem}
                      disabled={loading}
                    >
                      <FiArrowRight /> Finish & See Solution
                    </button>
                  )}

                  <button
                    className="reset-button"
                    onClick={resetProblem}
                    disabled={loading}
                  >
                    <FiRefreshCw /> Start Over
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {phase === 'solution' && finalSolution && (
          <div className="math-phase phase-solution">
            <div className="solution-header">
              <h2>Complete Solution</h2>
              <div className="mastery-badge">
                <strong>Mastery Score: {finalSolution.mastery_score}%</strong>
              </div>
            </div>

            <div className="solution-sections">
              <div className="solution-box">
                <h3>Full Solution</h3>
                <div className="solution-text">{finalSolution.full_solution}</div>
              </div>

              {finalSolution.latex_solution && (
                <div className="latex-box">
                  <h3>Mathematical Notation</h3>
                  <div className="latex-display">
                    <code>{finalSolution.latex_solution}</code>
                  </div>
                  <p className="latex-note">Copy the LaTeX code above for academic documents</p>
                </div>
              )}

              <div className="concepts-box">
                <h3>Key Concepts</h3>
                <ul className="concepts-list">
                  {finalSolution.key_concepts.map((concept, idx) => (
                    <li key={idx}>{concept}</li>
                  ))}
                </ul>
              </div>

              {finalSolution.learning_insights && (
                <div className="insights-box">
                  <h3>Learning Insights</h3>
                  <p>{finalSolution.learning_insights}</p>
                </div>
              )}
            </div>

            <div className="solution-actions">
              <div className="download-section">
                <label>📥 Download Solution:</label>
                <div className="download-buttons">
                  <button
                    className="download-button"
                    onClick={() => downloadSolution('markdown')}
                    disabled={loading}
                    title="Download as Markdown (.md)"
                  >
                    {loading ? <FiLoader className="spinner" /> : <FiDownload />}
                    Markdown
                  </button>
                  <button
                    className="download-button"
                    onClick={() => downloadSolution('latex')}
                    disabled={loading}
                    title="Download as LaTeX (.tex)"
                  >
                    {loading ? <FiLoader className="spinner" /> : <FiDownload />}
                    LaTeX
                  </button>
                  <button
                    className="download-button"
                    onClick={() => downloadSolution('html')}
                    disabled={loading}
                    title="Download as HTML (.html)"
                  >
                    {loading ? <FiLoader className="spinner" /> : <FiDownload />}
                    HTML
                  </button>
                  <button
                    className="download-button"
                    onClick={() => downloadSolution('json')}
                    disabled={loading}
                    title="Download as JSON (.json)"
                  >
                    {loading ? <FiLoader className="spinner" /> : <FiDownload />}
                    JSON
                  </button>
                </div>
              </div>

              <button
                className="submit-button"
                onClick={resetProblem}
              >
                <FiArrowLeft /> Solve Another Problem
              </button>
              <button
                className="secondary-button"
                onClick={() => onBack()}
              >
                <FiHome /> Back to Home
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
