import React from 'react';
import './Select.css';

const Select = ({ 
  value, 
  onChange, 
  name,
  id,
  required = false,
  disabled = false,
  className = '',
  error = false,
  children
}) => {
  const selectClasses = `select ${error ? 'select-error' : ''} ${className}`.trim();
  
  return (
    <select
      value={value}
      onChange={onChange}
      name={name}
      id={id}
      required={required}
      disabled={disabled}
      className={selectClasses}
    >
      {children}
    </select>
  );
};

export default Select;

