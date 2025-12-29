import React from 'react';
import { Toast, ToastContainer } from 'react-bootstrap';
import { FaCheckCircle, FaTimesCircle, FaExclamationTriangle, FaInfoCircle, FaEdit, FaTimes } from 'react-icons/fa';
import './Alert.css';

const Alert = ({ 
  isOpen, 
  onClose, 
  title, 
  message, 
  variant = 'info',
  showInstructions = false,
  children 
}) => {
  const variantMap = {
    info: 'primary',
    success: 'success',
    warning: 'warning',
    error: 'danger'
  };

  const icons = {
    info: <FaInfoCircle className="me-2" />,
    warning: <FaExclamationTriangle className="me-2" />,
    error: <FaTimesCircle className="me-2" />,
    success: <FaCheckCircle className="me-2" />
  };

  if (!isOpen) return null;

  return (
    <ToastContainer 
      position="top-center" 
      className="p-3 alert-toast-container"
      style={{ 
        position: 'fixed',
        top: '20px',
        left: '50%',
        transform: 'translateX(-50%)',
        zIndex: 9999,
        width: 'auto',
        maxWidth: '500px'
      }}
    >
      <Toast 
        show={isOpen} 
        onClose={onClose}
        bg={variantMap[variant] || 'primary'}
        delay={5000}
        autohide={!showInstructions}
        className="alert-toast shadow-lg border-0"
        style={{ 
          minWidth: '380px', 
          maxWidth: '500px',
          borderRadius: '12px',
          overflow: 'hidden',
          animation: 'slideDownFade 0.4s ease-out'
        }}
      >
        <Toast.Header 
          className={`bg-${variantMap[variant]} text-white border-0 py-3 px-4`}
          style={{
            background: `linear-gradient(135deg, var(--bs-${variantMap[variant]}) 0%, var(--bs-${variantMap[variant]}-dark, var(--bs-${variantMap[variant]})) 100%)`,
            fontWeight: '600',
            fontSize: '1.1rem'
          }}
          closeButton={true}
          onClose={onClose}
        >
          <strong className="me-auto d-flex align-items-center">
            <span style={{ fontSize: '1.3rem', marginRight: '0.75rem' }}>
              {icons[variant]}
            </span>
            {title}
          </strong>
        </Toast.Header>
        <Toast.Body 
          className="bg-white p-4"
          style={{
            fontSize: '0.95rem',
            lineHeight: '1.6'
          }}
        >
          <div className="text-dark mb-0">{message}</div>
          
          {showInstructions && (
            <div className="mt-3 p-3 rounded-3" style={{
              background: 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)',
              borderLeft: '4px solid var(--bs-primary)',
              boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.06)'
            }}>
              <h6 className="d-flex align-items-center mb-3 fw-bold text-primary">
                <FaEdit className="me-2" style={{ fontSize: '1.1rem' }} />
                Cómo configurar OPENAI_API_KEY:
              </h6>
              <ol className="mb-0 ps-3" style={{ fontSize: '0.9rem' }}>
                <li className="mb-2">
                  Obtén tu API key de OpenAI desde{' '}
                  <a 
                    href="https://platform.openai.com/api-keys" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-decoration-none fw-semibold"
                    style={{ color: 'var(--bs-primary)' }}
                  >
                    platform.openai.com
                  </a>
                </li>
                <li className="mb-2">
                  En la carpeta <code className="bg-light px-2 py-1 rounded" style={{ fontSize: '0.85rem' }}>backend</code>, edita el archivo <code className="bg-light px-2 py-1 rounded" style={{ fontSize: '0.85rem' }}>.env</code>
                </li>
                <li className="mb-2">
                  Agrega la siguiente línea: <code className="bg-light px-2 py-1 rounded d-inline-block" style={{ fontSize: '0.85rem' }}>OPENAI_API_KEY=tu-api-key-aqui</code>
                </li>
                <li>Reinicia el servidor backend para aplicar los cambios</li>
              </ol>
            </div>
          )}
          
          {children}
        </Toast.Body>
      </Toast>
    </ToastContainer>
  );
};

export default Alert;

