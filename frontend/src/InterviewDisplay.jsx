import React from 'react';
import './InterviewDisplay.css';

const InterviewDisplay = ({ interview, tokensUsed, onClose }) => {
  if (!interview) {
    return null;
  }

  return (
    <div className="interview-display">
      <div className="interview-header">
        <h2>{interview.interview_name || 'Generated Interview'}</h2>
        <button className="close-button" onClick={onClose}>×</button>
      </div>

      <div className="interview-meta">
        <div className="meta-item">
          <span className="meta-label">Requisition ID:</span>
          <span className="meta-value">{interview.req_id}</span>
        </div>
        <div className="meta-item">
          <span className="meta-label">Interview ID:</span>
          <span className="meta-value">#{interview.id}</span>
        </div>
        {tokensUsed && (
          <div className="meta-item">
            <span className="meta-label">Tokens Used:</span>
            <span className="meta-value">{tokensUsed.toLocaleString()}</span>
          </div>
        )}
      </div>

      <div className="questions-container">
        {interview.questions && interview.questions.length > 0 ? (
          interview.questions.map((question, index) => (
            <div key={question.id || index} className="question-card">
              <div className="question-header">
                <span className="question-number">Question {question.question_number}</span>
                <span className="question-type">{question.question_type || 'technical'}</span>
              </div>
              
              <div className="question-text">
                {question.question_text}
              </div>

              {question.criteria && question.criteria.length > 0 && (
                <div className="criteria-section">
                  <h4>Evaluation Criteria ({question.criteria.length} items):</h4>
                  <ul className="criteria-list">
                    {question.criteria.map((criterion, idx) => (
                      <li key={idx} className="criterion-item">
                        <strong>{criterion.criterion}:</strong>
                        <span>{criterion.description}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))
        ) : (
          <div className="no-questions">
            <p>No questions generated yet.</p>
          </div>
        )}
      </div>

      {interview.created_at && (
        <div className="interview-footer">
          <p>Created: {new Date(interview.created_at).toLocaleString()}</p>
        </div>
      )}
    </div>
  );
};

export default InterviewDisplay;