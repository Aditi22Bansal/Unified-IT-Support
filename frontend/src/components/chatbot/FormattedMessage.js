import React from 'react';
import './ChatMessage.css';

const FormattedMessage = ({ message, isUser, timestamp, confidence }) => {
  // Function to render HTML content safely
  const renderHTML = (htmlString) => {
    return { __html: htmlString };
  };

  // Function to get confidence class
  const getConfidenceClass = (conf) => {
    if (conf >= 0.8) return 'high';
    if (conf >= 0.6) return 'medium';
    return 'low';
  };

  return (
    <div className={`chat-message ${isUser ? 'user' : 'assistant'}`}>
      <div
        className="message-content"
        dangerouslySetInnerHTML={renderHTML(message)}
      />
      <div className="message-metadata">
        <span className="message-timestamp">{timestamp}</span>
        {!isUser && confidence && (
          <span className={`message-confidence ${getConfidenceClass(confidence)}`}>
            Confidence: {Math.round(confidence * 100)}%
          </span>
        )}
      </div>
    </div>
  );
};

export default FormattedMessage;




