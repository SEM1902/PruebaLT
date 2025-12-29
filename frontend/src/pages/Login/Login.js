import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Card, Form, Modal } from 'react-bootstrap';
import { FaLock, FaExclamationTriangle, FaTimesCircle } from 'react-icons/fa';
import { useAuth } from '../../context/AuthContext';
import FormField from '../../components/molecules/FormField/FormField';
import Button from '../../components/atoms/Button/Button';
import './Login.css';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Validar formato de email antes de enviar
    if (formData.email && !formData.email.includes('@')) {
      setError('El correo electrónico debe contener el símbolo "@"');
      setLoading(false);
      return;
    }

    const result = await login(formData.email, formData.password);
    
    if (result.success) {
      navigate('/empresas');
    } else {
      setError(result.error || 'Error al iniciar sesión');
    }
    
    setLoading(false);
  };

  return (
    <div className="login-container d-flex align-items-center justify-content-center min-vh-100">
      <Container className="d-flex justify-content-center">
        <Card className="login-card shadow-lg" style={{ maxWidth: '400px', width: '100%' }}>
          <Card.Body className="p-4">
            <Card.Title as="h1" className="text-center mb-4 d-flex align-items-center justify-content-center gap-2">
              <FaLock /> Inicio de Sesión
            </Card.Title>
            <Form onSubmit={handleSubmit}>
              <FormField
                label="Correo electrónico"
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                placeholder="correo@ejemplo.com"
              />
              <FormField
                label="Contraseña"
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                placeholder="Ingrese su contraseña"
              />
              <div className="d-grid gap-2">
                <Button type="submit" variant="primary" size="large" disabled={loading} className="w-100">
                  {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
                </Button>
              </div>
            </Form>
          </Card.Body>
        </Card>
      </Container>

      {/* Modal de Error de Login */}
      <Modal 
        show={!!error} 
        onHide={() => setError('')} 
        centered
        backdrop="static"
        className="error-modal"
      >
        <Modal.Header 
          className="bg-danger text-white border-0"
          style={{
            background: 'linear-gradient(135deg, #dc3545 0%, #c82333 100%)',
            padding: '1.25rem 1.5rem'
          }}
        >
          <Modal.Title className="d-flex align-items-center gap-2">
            <FaExclamationTriangle style={{ fontSize: '1.5rem' }} />
            Error de Autenticación
          </Modal.Title>
          <button
            type="button"
            className="btn-close btn-close-white"
            onClick={() => setError('')}
            aria-label="Cerrar"
          ></button>
        </Modal.Header>
        <Modal.Body className="p-4">
          <div className="d-flex align-items-start gap-3">
            <div className="flex-shrink-0">
              <FaTimesCircle 
                className="text-danger" 
                style={{ fontSize: '2.5rem' }}
              />
            </div>
            <div className="flex-grow-1">
              <h5 className="mb-3 fw-bold text-dark">
                {error.includes('@') 
                  ? 'Correo electrónico inválido' 
                  : error.includes('contraseña') || error.includes('password')
                  ? 'Contraseña incorrecta'
                  : 'Error al iniciar sesión'}
              </h5>
              <p className="mb-0 text-muted" style={{ lineHeight: '1.6' }}>
                {error.includes('@') 
                  ? 'El correo electrónico debe contener el símbolo "@" y tener un formato válido (ejemplo: usuario@dominio.com).'
                  : error.includes('contraseña') || error.includes('password')
                  ? 'La contraseña ingresada no es correcta. Por favor, verifica tus credenciales e intenta nuevamente.'
                  : error}
              </p>
            </div>
          </div>
        </Modal.Body>
        <Modal.Footer className="border-0 pt-0">
          <Button 
            variant="danger" 
            onClick={() => setError('')}
            className="px-4"
          >
            Entendido
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default Login;

