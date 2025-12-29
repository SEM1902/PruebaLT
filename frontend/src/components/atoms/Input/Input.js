import React from 'react';
import './Input.css';

const Input = ({ 
  type = 'text', 
  placeholder, 
  value, 
  onChange, 
  name,
  id,
  required = false,
  disabled = false,
  className = '',
  error = false,
  step
}) => {
  const inputClasses = `input ${error ? 'input-error' : ''} ${className}`.trim();
  
  const handleChange = (e) => {
    if (type === 'number') {
      // Solo permitir números, punto decimal y signo negativo
      const inputValue = e.target.value;
      // Permitir vacío, números, un punto decimal y un signo negativo al inicio
      if (inputValue === '' || /^-?\d*\.?\d*$/.test(inputValue)) {
        onChange(e);
      }
    } else {
      onChange(e);
    }
  };
  
  return (
    <input
      type={type}
      placeholder={placeholder}
      value={value}
      onChange={handleChange}
      name={name}
      id={id}
      required={required}
      disabled={disabled}
      className={inputClasses}
      step={step}
    />
  );
};

export default Input;

