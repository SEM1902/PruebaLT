import React from 'react';
import './Spinner.css';

const Spinner = ({ size = 'medium', className = '' }) => {
  const spinnerClasses = `spinner spinner-${size} ${className}`.trim();
  
  return (
    <div className={spinnerClasses}>
      <div className="spinner-circle"></div>
    </div>
  );
};

export default Spinner;

