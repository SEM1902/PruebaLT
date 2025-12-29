import React from 'react';
import './Button.css';

const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'medium', 
  type = 'button', 
  onClick, 
  disabled = false,
  className = '',
  loading = false
}) => {
  const buttonClasses = `btn btn-${variant} btn-${size} ${className} ${loading ? 'btn-loading' : ''}`.trim();
  
  return (
    <button
      type={type}
      className={buttonClasses}
      onClick={onClick}
      disabled={disabled || loading}
    >
      {children}
    </button>
  );
};

export default Button;

