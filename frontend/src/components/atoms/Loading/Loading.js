import React from 'react';
import './Loading.css';

const Loading = ({ text = 'Cargando', inline = false }) => {
  if (inline) {
    return (
      <div className="loading-inline">
        <div className="loading-spinner"></div>
        <span className="loading-text">
          {text}
          <span className="loading-dots">
            <span></span>
            <span></span>
            <span></span>
          </span>
        </span>
      </div>
    );
  }

  return (
    <div className="loading-container">
      <div className="loading-spinner"></div>
      <div className="loading-text">
        {text}
        <span className="loading-dots">
          <span></span>
          <span></span>
          <span></span>
        </span>
      </div>
    </div>
  );
};

export default Loading;

