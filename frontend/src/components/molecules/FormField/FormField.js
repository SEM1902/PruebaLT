import React from 'react';
import { FaExclamationCircle } from 'react-icons/fa';
import Label from '../../atoms/Label/Label';
import Input from '../../atoms/Input/Input';
import Textarea from '../../atoms/Textarea/Textarea';
import Select from '../../atoms/Select/Select';
import './FormField.css';

const FormField = ({ 
  label, 
  type = 'text', 
  name, 
  value, 
  onChange, 
  required = false,
  disabled = false,
  error,
  placeholder,
  options,
  rows,
  step
}) => {
  const renderInput = () => {
    switch (type) {
      case 'textarea':
        return (
          <Textarea
            name={name}
            id={name}
            value={value}
            onChange={onChange}
            required={required}
            disabled={disabled}
            placeholder={placeholder}
            error={!!error}
            rows={rows}
          />
        );
      case 'select':
        return (
          <Select
            name={name}
            id={name}
            value={value}
            onChange={onChange}
            required={required}
            disabled={disabled}
            error={!!error}
          >
            <option value="">Seleccione una opción</option>
            {options?.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </Select>
        );
      default:
        return (
          <Input
            type={type}
            name={name}
            id={name}
            value={value}
            onChange={onChange}
            required={required}
            disabled={disabled}
            placeholder={placeholder}
            error={!!error}
            step={step}
          />
        );
    }
  };

  return (
    <div className="form-field">
      {label && (
        <Label htmlFor={name} required={required}>
          {label}
        </Label>
      )}
      {renderInput()}
      {error && (
        <span className="form-field-error">
          <FaExclamationCircle /> {error}
        </span>
      )}
    </div>
  );
};

export default FormField;

