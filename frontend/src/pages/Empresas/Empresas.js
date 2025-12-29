import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Form } from 'react-bootstrap';
import { FaBuilding, FaEdit, FaTrash } from 'react-icons/fa';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';
import FormField from '../../components/molecules/FormField/FormField';
import Button from '../../components/atoms/Button/Button';
import Loading from '../../components/atoms/Loading/Loading';
import Spinner from '../../components/atoms/Spinner/Spinner';
import Alert from '../../components/atoms/Alert/Alert';
import './Empresas.css';

const Empresas = () => {
  const { isAdministrador } = useAuth();
  const [empresas, setEmpresas] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [deleting, setDeleting] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [formData, setFormData] = useState({
    nit: '',
    nombre: '',
    direccion: '',
    telefono: ''
  });
  const [errors, setErrors] = useState({});
  const [search, setSearch] = useState('');
  const [successMessage, setSuccessMessage] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  useEffect(() => {
    fetchEmpresas();
  }, []);

  const fetchEmpresas = async () => {
    setLoading(true);
    try {
      const params = search ? { search } : {};
      const response = await api.get('/api/empresas/', { params });
      setEmpresas(response.data.results || response.data);
    } catch (error) {
      console.error('Error al cargar empresas:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      fetchEmpresas();
    }, 300);
    return () => clearTimeout(timeoutId);
  }, [search]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setErrors({ ...errors, [e.target.name]: '' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});
    setSubmitting(true);

    try {
      if (editing) {
        await api.put(`/api/empresas/${editing.nit}/`, formData);
        setSuccessMessage('Empresa actualizada exitosamente');
      } else {
        await api.post('/api/empresas/', formData);
        setSuccessMessage('Empresa creada exitosamente');
      }
      resetForm();
      fetchEmpresas();
      setTimeout(() => setSuccessMessage(null), 5000);
    } catch (error) {
      if (error.response?.data) {
        setErrors(error.response.data);
        if (error.response.data.non_field_errors) {
          setErrorMessage(error.response.data.non_field_errors[0] || 'Error al guardar la empresa');
          setTimeout(() => setErrorMessage(null), 5000);
        }
      } else {
        setErrorMessage('Error al guardar la empresa');
        setTimeout(() => setErrorMessage(null), 5000);
      }
    } finally {
      setSubmitting(false);
    }
  };

  const handleEdit = (empresa) => {
    setEditing(empresa);
    setFormData({
      nit: empresa.nit,
      nombre: empresa.nombre,
      direccion: empresa.direccion,
      telefono: empresa.telefono
    });
    setShowForm(true);
  };

  const handleDelete = async (nit) => {
    if (window.confirm('¿Está seguro de eliminar esta empresa?')) {
      setDeleting(nit);
      try {
        await api.delete(`/api/empresas/${nit}/`);
        fetchEmpresas();
      } catch (error) {
        alert('Error al eliminar empresa');
      } finally {
        setDeleting(null);
      }
    }
  };

  const resetForm = () => {
    setFormData({
      nit: '',
      nombre: '',
      direccion: '',
      telefono: ''
    });
    setEditing(null);
    setShowForm(false);
    setErrors({});
  };

  return (
    <>
      {successMessage && (
        <Alert
          isOpen={!!successMessage}
          onClose={() => setSuccessMessage(null)}
          title="Éxito"
          message={successMessage}
          variant="success"
        />
      )}
      {errorMessage && (
        <Alert
          isOpen={!!errorMessage}
          onClose={() => setErrorMessage(null)}
          title="Error"
          message={errorMessage}
          variant="error"
        />
      )}
      <Row className="mb-4">
        <Col>
          <h1 className="d-flex align-items-center gap-2">
            <FaBuilding /> Empresas
          </h1>
        </Col>
        {isAdministrador() && (
          <Col xs="auto">
            <Button onClick={() => setShowForm(!showForm)}>
              {showForm ? 'Cancelar' : 'Nueva Empresa'}
            </Button>
          </Col>
        )}
      </Row>

      <Row className="mb-4">
        <Col md={4}>
          <FormField
            type="text"
            name="search"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Buscar empresas..."
          />
        </Col>
      </Row>

      {showForm && isAdministrador() && (
        <Card className="mb-4 shadow-sm">
          <Card.Header>
            <Card.Title className="mb-0">{editing ? 'Editar Empresa' : 'Nueva Empresa'}</Card.Title>
          </Card.Header>
          <Card.Body>
          <Form onSubmit={handleSubmit}>
            <FormField
              label="NIT"
              name="nit"
              value={formData.nit}
              onChange={handleChange}
              required
              error={errors.nit}
              disabled={!!editing}
            />
            <FormField
              label="Nombre de la empresa"
              name="nombre"
              value={formData.nombre}
              onChange={handleChange}
              required
              error={errors.nombre}
            />
            <FormField
              label="Dirección"
              type="textarea"
              name="direccion"
              value={formData.direccion}
              onChange={handleChange}
              required
              error={errors.direccion}
              rows={3}
            />
            <FormField
              label="Teléfono"
              name="telefono"
              value={formData.telefono}
              onChange={handleChange}
              required
              error={errors.telefono}
            />
            <div className="d-flex gap-2">
              <Button type="submit" variant="primary" disabled={submitting} loading={submitting}>
                {submitting ? (
                  <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Spinner size="small" />
                    {editing ? 'Actualizando...' : 'Creando...'}
                  </span>
                ) : (
                  editing ? 'Actualizar' : 'Crear'
                )}
              </Button>
              <Button type="button" variant="secondary" onClick={resetForm} disabled={submitting}>
                Cancelar
              </Button>
            </div>
          </Form>
          </Card.Body>
        </Card>
      )}

      {loading ? (
        <Loading text="Cargando empresas" />
      ) : empresas.length === 0 ? (
        <Card className="text-center py-5">
          <Card.Body>
            <FaBuilding size={64} className="mb-3 text-muted" />
            <h4>No hay empresas disponibles</h4>
            <p className="text-muted">Crea tu primera empresa para comenzar</p>
          </Card.Body>
        </Card>
      ) : (
        <Row>
          {empresas.map((empresa) => (
            <Col key={empresa.nit} md={6} lg={4} className="mb-4">
              <Card className="h-100 shadow-sm">
                <Card.Header>
                  <Card.Title className="mb-0">{empresa.nombre}</Card.Title>
                </Card.Header>
                <Card.Body>
                  <p className="mb-2"><strong>NIT:</strong> {empresa.nit}</p>
                  <p className="mb-2"><strong>Teléfono:</strong> {empresa.telefono}</p>
                  <p className="mb-0"><strong>Dirección:</strong> {empresa.direccion}</p>
                </Card.Body>
                {isAdministrador() && (
                  <Card.Footer>
                    <div className="d-flex gap-2 flex-wrap">
                      <Button size="small" variant="primary" onClick={() => handleEdit(empresa)}>
                        <FaEdit className="me-1" /> Editar
                      </Button>
                      <Button 
                        size="small" 
                        variant="danger" 
                        onClick={() => handleDelete(empresa.nit)}
                        disabled={deleting === empresa.nit}
                        loading={deleting === empresa.nit}
                      >
                        {deleting === empresa.nit ? (
                          <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <Spinner size="small" />
                            Eliminando...
                          </span>
                        ) : (
                          <>
                            <FaTrash className="me-1" /> Eliminar
                          </>
                        )}
                      </Button>
                    </div>
                  </Card.Footer>
                )}
              </Card>
            </Col>
          ))}
        </Row>
      )}
    </>
  );
};

export default Empresas;

