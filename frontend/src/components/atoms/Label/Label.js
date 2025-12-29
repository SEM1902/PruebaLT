import React from 'react';
import './Label.css';

const Label = ({ children, htmlFor, required = false, className = '' }) => {
  return (
    <label htmlFor={htmlFor} className={`label ${className}`.trim()}>
      {children}
      {required && <span className="label-required"> *</span>}
    </label>
  );
};

export default Label;

