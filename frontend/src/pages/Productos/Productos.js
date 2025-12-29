import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Form, Button as BootstrapButton, Alert as BootstrapAlert } from 'react-bootstrap';
import { FaShoppingBag, FaLightbulb, FaEdit, FaRobot, FaTrash } from 'react-icons/fa';
import api from '../../services/api';
import FormField from '../../components/molecules/FormField/FormField';
import Button from '../../components/atoms/Button/Button';
import Loading from '../../components/atoms/Loading/Loading';
import Spinner from '../../components/atoms/Spinner/Spinner';
import Alert from '../../components/atoms/Alert/Alert';
import './Productos.css';

const Productos = () => {
  const [productos, setProductos] = useState([]);
  const [empresas, setEmpresas] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [convertingCurrency, setConvertingCurrency] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [formData, setFormData] = useState({
    codigo: '',
    nombre: '',
    caracteristicas: '',
    precio_usd: '',
    precio_eur: '',
    precio_cop: '',
    empresa: ''
  });
  const [errors, setErrors] = useState({});
  const [filterEmpresa, setFilterEmpresa] = useState('');
  const [alertOpen, setAlertOpen] = useState(false);
  const [alertData, setAlertData] = useState({ title: '', message: '', variant: 'info', showInstructions: false });
  const [successMessage, setSuccessMessage] = useState(null);

  useEffect(() => {
    fetchEmpresas();
    fetchProductos();
  }, []);

  useEffect(() => {
    fetchProductos();
  }, [filterEmpresa]);

  const fetchEmpresas = async () => {
    try {
      const response = await api.get('/api/empresas/');
      setEmpresas(response.data.results || response.data);
    } catch (error) {
      console.error('Error al cargar empresas:', error);
    }
  };

  const fetchProductos = async () => {
    setLoading(true);
    try {
      const params = filterEmpresa ? { empresa: filterEmpresa } : {};
      const response = await api.get('/api/productos/', { params });
      setProductos(response.data.results || response.data);
    } catch (error) {
      console.error('Error al cargar productos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = async (e) => {
    const { name, value } = e.target;
    
    setFormData({
      ...formData,
      [name]: value
    });
    setErrors({ ...errors, [name]: '' });
    
    // Si se cambia el precio en USD, calcular automáticamente EUR y COP
    if (name === 'precio_usd' && value && !isNaN(value) && parseFloat(value) > 0) {
      setConvertingCurrency(true);
      try {
        const response = await api.get('/api/productos/convert-currency/', {
          params: { amount: value }
        });
        const { eur, cop } = response.data;
        setFormData(prev => ({
          ...prev,
          precio_usd: value,
          precio_eur: eur.toFixed(2),
          precio_cop: cop.toFixed(2)
        }));
      } catch (error) {
        console.error('Error al convertir monedas:', error);
        // Si falla la conversión, no hacer nada (el backend lo calculará automáticamente)
      } finally {
        setConvertingCurrency(false);
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});
    setSubmitting(true);

    try {
      // Si solo se proporciona precio_usd, el backend calculará automáticamente EUR y COP
      const data = {
        ...formData,
        precio_usd: parseFloat(formData.precio_usd) || 0,
        // Si no se proporcionan EUR o COP, el backend los calculará desde USD
        precio_eur: formData.precio_eur ? parseFloat(formData.precio_eur) : 0,
        precio_cop: formData.precio_cop ? parseFloat(formData.precio_cop) : 0
      };

      if (editing) {
        await api.put(`/api/productos/${editing.id}/`, data);
        setSuccessMessage('Producto actualizado exitosamente');
      } else {
        await api.post('/api/productos/', data);
        setSuccessMessage('Producto creado exitosamente');
      }
      resetForm();
      fetchProductos();
      setTimeout(() => setSuccessMessage(null), 5000);
    } catch (error) {
      if (error.response?.data) {
        setErrors(error.response.data);
      }
    } finally {
      setSubmitting(false);
    }
  };

  const handleEdit = (producto) => {
    setEditing(producto);
    setFormData({
      codigo: producto.codigo,
      nombre: producto.nombre,
      caracteristicas: producto.caracteristicas,
      precio_usd: producto.precio_usd,
      precio_eur: producto.precio_eur,
      precio_cop: producto.precio_cop,
      empresa: producto.empresa
    });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar este producto?')) {
      try {
        await api.delete(`/api/productos/${id}/`);
        setSuccessMessage('Producto eliminado exitosamente');
        fetchProductos();
        setTimeout(() => setSuccessMessage(null), 5000);
      } catch (error) {
        console.error('Error al eliminar producto:', error);
        setAlertData({
          title: 'Error',
          message: error.response?.data?.detail || 'Error al eliminar el producto',
          variant: 'error',
          showInstructions: false
        });
        setAlertOpen(true);
      }
    }
  };

  const handleAISuggestions = async (id) => {
    try {
      const response = await api.get(`/api/productos/${id}/ai_suggestions/`);
      const suggestions = response.data.suggestions || 'No se pudieron obtener sugerencias';
      
      // Mostrar sugerencias (sin detectar errores, similar a como funciona en Inventario)
      setAlertData({
        title: 'Sugerencias de IA',
        message: suggestions,
        variant: 'success'
      });
      setAlertOpen(true);
    } catch (error) {
      // En caso de error, mostrar mensaje genérico sin detalles técnicos
      setAlertData({
        title: 'Sugerencias de IA',
        message: 'No se pudieron obtener sugerencias en este momento.',
        variant: 'info'
      });
      setAlertOpen(true);
    }
  };

  const resetForm = () => {
    setFormData({
      codigo: '',
      nombre: '',
      caracteristicas: '',
      precio_usd: '',
      precio_eur: '',
      precio_cop: '',
      empresa: ''
    });
    setEditing(null);
    setShowForm(false);
    setErrors({});
  };

  const empresaOptions = empresas.map(emp => ({
    value: emp.nit,
    label: `${emp.nombre} - ${emp.nit}`
  }));

  return (
    <>
      <Alert
        isOpen={alertOpen}
        onClose={() => setAlertOpen(false)}
        title={alertData.title}
        message={alertData.message}
        variant={alertData.variant}
        showInstructions={alertData.showInstructions}
      />
      {successMessage && (
        <Alert
          isOpen={!!successMessage}
          onClose={() => setSuccessMessage(null)}
          title="Éxito"
          message={successMessage}
          variant="success"
        />
      )}
      <Row className="mb-4">
        <Col>
          <h1 className="d-flex align-items-center gap-2">
            <FaShoppingBag /> Productos
          </h1>
        </Col>
        <Col xs="auto">
          <Button onClick={() => setShowForm(!showForm)}>
            {showForm ? 'Cancelar' : 'Nuevo Producto'}
          </Button>
        </Col>
      </Row>

      <Row className="mb-4">
        <Col md={4}>
          <FormField
            label="Filtrar por empresa"
            type="select"
            name="filterEmpresa"
            value={filterEmpresa}
            onChange={(e) => setFilterEmpresa(e.target.value)}
            options={[{ value: '', label: 'Todas las empresas' }, ...empresaOptions]}
          />
        </Col>
      </Row>

      {showForm && (
        <Card className="mb-4 shadow-sm">
          <Card.Header>
            <Card.Title className="mb-0">{editing ? 'Editar Producto' : 'Nuevo Producto'}</Card.Title>
          </Card.Header>
          <Card.Body>
          <Form onSubmit={handleSubmit}>
            <FormField
              label="Código"
              name="codigo"
              value={formData.codigo}
              onChange={handleChange}
              required
              error={errors.codigo}
              disabled={!!editing}
            />
            <FormField
              label="Nombre del producto"
              name="nombre"
              value={formData.nombre}
              onChange={handleChange}
              required
              error={errors.nombre}
            />
            <FormField
              label="Características"
              type="textarea"
              name="caracteristicas"
              value={formData.caracteristicas}
              onChange={handleChange}
              required
              error={errors.caracteristicas}
              rows={4}
            />
            <Row className="mb-3">
              <Col md={4}>
                <FormField
                  label="Precio USD"
                  type="number"
                  name="precio_usd"
                  value={formData.precio_usd}
                  onChange={handleChange}
                  required
                  error={errors.precio_usd}
                  placeholder="0.00"
                  step="0.01"
                />
              </Col>
              <Col md={4}>
                <div style={{ position: 'relative' }}>
                  <FormField
                    label="Precio EUR"
                    type="number"
                    name="precio_eur"
                    value={formData.precio_eur}
                    onChange={handleChange}
                    required
                    error={errors.precio_eur}
                    placeholder="0.00"
                    step="0.01"
                  />
                  {convertingCurrency && (
                    <div style={{ position: 'absolute', top: '35px', right: '15px' }}>
                      <Spinner size="small" />
                    </div>
                  )}
                </div>
              </Col>
              <Col md={4}>
                <div style={{ position: 'relative' }}>
                  <FormField
                    label="Precio COP"
                    type="number"
                    name="precio_cop"
                    value={formData.precio_cop}
                    onChange={handleChange}
                    required
                    error={errors.precio_cop}
                    placeholder="0.00"
                    step="0.01"
                  />
                  {convertingCurrency && (
                    <div style={{ position: 'absolute', top: '35px', right: '15px' }}>
                      <Spinner size="small" />
                    </div>
                  )}
                </div>
              </Col>
            </Row>
            <BootstrapAlert variant="info" className="mb-3 d-flex align-items-start gap-2">
              <FaLightbulb className="mt-1" />
              <span>Los precios en EUR y COP se calculan automáticamente desde USD usando tasas de cambio en tiempo real</span>
            </BootstrapAlert>
            <FormField
              label="Empresa"
              type="select"
              name="empresa"
              value={formData.empresa}
              onChange={handleChange}
              required
              error={errors.empresa}
              options={empresaOptions}
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
        <Loading text="Cargando productos" />
      ) : productos.length === 0 ? (
        <Card className="text-center py-5">
          <Card.Body>
            <FaShoppingBag size={64} className="mb-3 text-muted" />
            <h4>No hay productos disponibles</h4>
            <p className="text-muted">Crea tu primer producto para comenzar</p>
          </Card.Body>
        </Card>
      ) : (
        <Row>
          {productos.map((producto) => (
            <Col key={producto.id} md={6} lg={4} className="mb-4">
              <Card className="h-100 shadow-sm">
                <Card.Header>
                  <Card.Title className="mb-0">{producto.nombre}</Card.Title>
                </Card.Header>
                <Card.Body>
                  <p className="mb-2"><strong>Código:</strong> {producto.codigo}</p>
                  <p className="mb-2"><strong>Empresa:</strong> {producto.empresa_nombre}</p>
                  <p className="mb-3"><strong>Características:</strong> {producto.caracteristicas}</p>
                  <div className="bg-light p-3 rounded mb-3">
                    <div className="mb-1"><strong>USD:</strong> ${producto.precio_usd}</div>
                    <div className="mb-1"><strong>EUR:</strong> €{producto.precio_eur}</div>
                    <div><strong>COP:</strong> ${producto.precio_cop}</div>
                  </div>
                </Card.Body>
                <Card.Footer>
                  <div className="d-flex gap-2 flex-wrap">
                    <Button size="small" variant="primary" onClick={() => handleEdit(producto)}>
                      <FaEdit className="me-1" /> Editar
                    </Button>
                    <Button size="small" variant="success" onClick={() => handleAISuggestions(producto.id)}>
                      <FaRobot className="me-1" /> Sugerencias IA
                    </Button>
                    <Button size="small" variant="danger" onClick={() => handleDelete(producto.id)}>
                      <FaTrash className="me-1" /> Eliminar
                    </Button>
                  </div>
                </Card.Footer>
              </Card>
            </Col>
          ))}
        </Row>
      )}
    </>
  );
};

export default Productos;

