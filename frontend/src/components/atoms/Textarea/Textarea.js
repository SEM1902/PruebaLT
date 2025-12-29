import React from 'react';
import './Textarea.css';

const Textarea = ({ 
  placeholder, 
  value, 
  onChange, 
  name,
  id,
  required = false,
  disabled = false,
  rows = 4,
  className = '',
  error = false
}) => {
  const textareaClasses = `textarea ${error ? 'textarea-error' : ''} ${className}`.trim();
  
  return (
    <textarea
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      name={name}
      id={id}
      required={required}
      disabled={disabled}
      rows={rows}
      className={textareaClasses}
    />
  );
};

export default Textarea;

