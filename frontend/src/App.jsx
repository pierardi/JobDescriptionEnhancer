import React, { useState, useEffect } from 'react';
import InterviewForm from './InterviewForm';
import InterviewDisplay from './InterviewDisplay';
import { createInterview, healthCheck } from './api';
import './App.css';

function App() {
  const [interview, setInterview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [tokensUsed, setTokensUsed] = useState(null);
  const [serverStatus, setServerStatus] = useState('checking');

  useEffect(() => {
    // Check server health on mount
    checkServerHealth();
  }, []);

  const checkServerHealth = async () => {
    try {
      await healthCheck();
      setServerStatus('online');
    } catch (err) {
      setServerStatus('offline');
      console.error('Server health check failed:', err);
    }
  };

  const handleSubmit = async (formData) => {
    setLoading(true);
    setError(null);
    setInterview(null);
    setTokensUsed(null);

    try {
      const response = await createInterview(formData);
      
      if (response.success) {
        setInterview(response.interview);
        setTokensUsed(response.total_tokens_used || 0);
        // Scroll to interview display
        setTimeout(() => {
          const displayElement = document.querySelector('.interview-display');
          if (displayElement) {
            displayElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }, 100);
      } else {
        setError(response.error || 'Failed to create interview');
      }
    } catch (err) {
      setError(err.message || 'An error occurred while creating the interview');
      console.error('Error creating interview:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCloseInterview = () => {
    setInterview(null);
    setTokensUsed(null);
    // Scroll back to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="container">
          <h1>TechScreen Interview Generator</h1>
          <p>Create technical interviews from job descriptions using AI</p>
          <div className={`server-status ${serverStatus}`}>
            {serverStatus === 'online' ? '🟢 Server Online' : '🔴 Server Offline'}
          </div>
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          {error && (
            <div className="error-alert">
              <strong>Error:</strong> {error}
              <button onClick={() => setError(null)} className="close-alert">×</button>
            </div>
          )}

          {!interview && (
            <InterviewForm onSubmit={handleSubmit} loading={loading} />
          )}

          {interview && (
            <>
              <div className="success-alert">
                <strong>✓ Success!</strong> Interview generated successfully.
              </div>
              <InterviewDisplay
                interview={interview}
                tokensUsed={tokensUsed}
                onClose={handleCloseInterview}
              />
            </>
          )}
        </div>
      </main>

      <footer className="app-footer">
        <div className="container">
          <p>TechScreen Interview Generation System v1.0.0</p>
        </div>
      </footer>
    </div>
  );
}

export default App;