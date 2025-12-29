import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Form, Table, Badge, Modal } from 'react-bootstrap';
import { FaBox, FaDownload, FaPaperPlane, FaExclamationTriangle, FaBrain, FaEdit, FaEnvelope } from 'react-icons/fa';
import api from '../../services/api';
import FormField from '../../components/molecules/FormField/FormField';
import Button from '../../components/atoms/Button/Button';
import Loading from '../../components/atoms/Loading/Loading';
import Spinner from '../../components/atoms/Spinner/Spinner';
import Alert from '../../components/atoms/Alert/Alert';
import './Inventario.css';

const Inventario = () => {
  const [inventario, setInventario] = useState([]);
  const [empresas, setEmpresas] = useState([]);
  const [productos, setProductos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [downloadingPDF, setDownloadingPDF] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [selectedEmpresa, setSelectedEmpresa] = useState('');
  const [formData, setFormData] = useState({
    empresa: '',
    producto: '',
    cantidad: ''
  });
  const [errors, setErrors] = useState({});
  const [emailForm, setEmailForm] = useState({
    email: ''
  });
  const [sendingEmail, setSendingEmail] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const [inventoryAlerts, setInventoryAlerts] = useState([]);
  const [loadingAlerts, setLoadingAlerts] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [editQuantity, setEditQuantity] = useState('');
  const [updatingQuantity, setUpdatingQuantity] = useState(false);
  const [showEmailModal, setShowEmailModal] = useState(false);
  const [emailToSend, setEmailToSend] = useState('');
  const [emailError, setEmailError] = useState('');
  const [selectedEmpresaForEmail, setSelectedEmpresaForEmail] = useState(null);

  useEffect(() => {
    fetchEmpresas();
    fetchProductos();
    fetchInventario();
  }, []);

  useEffect(() => {
    if (selectedEmpresa) {
      fetchInventarioByEmpresa(selectedEmpresa);
    } else {
      fetchInventario();
    }
  }, [selectedEmpresa]);

  const fetchEmpresas = async () => {
    try {
      const response = await api.get('/api/empresas/');
      setEmpresas(response.data.results || response.data);
    } catch (error) {
      console.error('Error al cargar empresas:', error);
    }
  };

  const fetchProductos = async () => {
    try {
      const response = await api.get('/api/productos/');
      setProductos(response.data.results || response.data);
    } catch (error) {
      console.error('Error al cargar productos:', error);
    }
  };

  const fetchInventario = async () => {
    setLoading(true);
    try {
      const response = await api.get('/api/inventario/');
      setInventario(response.data.results || response.data);
    } catch (error) {
      console.error('Error al cargar inventario:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchInventoryAlerts = async () => {
    setLoadingAlerts(true);
    try {
      const params = selectedEmpresa ? { empresa: selectedEmpresa } : {};
      const response = await api.get('/api/inventario/predictions/', { params });
      setInventoryAlerts(response.data.alerts || []);
      if (response.data.alerts && response.data.alerts.length === 0) {
        setSuccessMessage('No se encontraron alertas de inventario. Todos los productos tienen stock suficiente.');
        setTimeout(() => setSuccessMessage(null), 5000);
      }
    } catch (error) {
      console.error('Error al cargar alertas de inventario:', error);
      setInventoryAlerts([]);
      setErrorMessage(error.response?.data?.error || 'Error al obtener predicciones de inventario');
      setTimeout(() => setErrorMessage(null), 5000);
    } finally {
      setLoadingAlerts(false);
    }
  };

  const fetchInventarioByEmpresa = async (empresaNit) => {
    setLoading(true);
    try {
      const response = await api.get(`/api/inventario/empresa/${empresaNit}/`);
      setInventario(response.data);
    } catch (error) {
      console.error('Error al cargar inventario:', error);
    } finally {
      setLoading(false);
    }
  };

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
      const data = {
        ...formData,
        cantidad: parseInt(formData.cantidad)
      };
      await api.post('/api/inventario/', data);
      setSuccessMessage('Producto agregado al inventario exitosamente');
      resetForm();
      if (selectedEmpresa) {
        fetchInventarioByEmpresa(selectedEmpresa);
      } else {
        fetchInventario();
      }
      // Actualizar alertas después de agregar producto
      if (inventoryAlerts.length > 0) {
        fetchInventoryAlerts();
      }
      setTimeout(() => setSuccessMessage(null), 5000);
    } catch (error) {
      if (error.response?.data) {
        setErrors(error.response.data);
        setErrorMessage(error.response.data.non_field_errors?.[0] || 'Error al agregar al inventario');
        setTimeout(() => setErrorMessage(null), 5000);
      }
    } finally {
      setSubmitting(false);
    }
  };

  const handleDownloadPDF = async (empresaNit) => {
    setDownloadingPDF(empresaNit);
    try {
      const response = await api.get(`/api/inventario/pdf/${empresaNit}/`, {
        responseType: 'blob'
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `inventario_${empresaNit}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      setSuccessMessage('PDF descargado exitosamente');
      setTimeout(() => setSuccessMessage(null), 5000);
    } catch (error) {
      setErrorMessage(error.response?.data?.error || 'Error al descargar PDF');
      setTimeout(() => setErrorMessage(null), 5000);
    } finally {
      setDownloadingPDF(null);
    }
  };

  const handleSendEmail = (empresaNit) => {
    // Encontrar el nombre de la empresa
    const empresa = empresas.find(emp => emp.nit === empresaNit);
    setSelectedEmpresaForEmail(empresaNit);
    setEmailToSend('');
    setEmailError('');
    setShowEmailModal(true);
  };

  const handleEmailSubmit = async (e) => {
    e.preventDefault();
    setEmailError('');

    // Validar email
    if (!emailToSend) {
      setEmailError('Por favor, ingrese un correo electrónico');
      return;
    }

    if (!emailToSend.includes('@')) {
      setEmailError('El correo electrónico debe contener el símbolo "@"');
      return;
    }

    // Validar formato básico de email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(emailToSend)) {
      setEmailError('Por favor, ingrese un correo electrónico válido (ejemplo: usuario@dominio.com)');
      return;
    }

    setSendingEmail(selectedEmpresaForEmail);
    setShowEmailModal(false);
    
    try {
      await api.post(`/api/inventario/send-pdf/${selectedEmpresaForEmail}/`, { email: emailToSend });
      setSuccessMessage(`PDF enviado exitosamente a ${emailToSend}`);
      setTimeout(() => setSuccessMessage(null), 5000);
      setEmailToSend('');
      setSelectedEmpresaForEmail(null);
    } catch (error) {
      setErrorMessage(error.response?.data?.error || 'Error al enviar email');
      setTimeout(() => setErrorMessage(null), 5000);
    } finally {
      setSendingEmail(null);
    }
  };

  const resetForm = () => {
    setFormData({
      empresa: '',
      producto: '',
      cantidad: ''
    });
    setShowForm(false);
    setErrors({});
  };

  const empresaOptions = empresas.map(emp => ({
    value: emp.nit,
    label: `${emp.nombre} - ${emp.nit}`
  }));

  const productoOptions = productos.map(prod => ({
    value: prod.id,
    label: `${prod.nombre} (${prod.codigo})`
  }));

  // Agrupar inventario por empresa
  const inventarioPorEmpresa = inventario.reduce((acc, item) => {
    const key = item.empresa_nombre;
    if (!acc[key]) {
      acc[key] = [];
    }
    acc[key].push(item);
    return acc;
  }, {});

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
            <FaBox /> Inventario
          </h1>
        </Col>
        <Col xs="auto" className="d-flex gap-2">
          <Button 
            variant="info" 
            onClick={fetchInventoryAlerts}
            disabled={loadingAlerts}
            loading={loadingAlerts}
          >
            <FaBrain className="me-1" /> Ver Predicciones IA
          </Button>
          <Button onClick={() => setShowForm(!showForm)}>
            {showForm ? 'Cancelar' : 'Agregar al Inventario'}
          </Button>
        </Col>
      </Row>

      {inventoryAlerts.length > 0 && (
        <Card className="mb-4 border-warning shadow-sm">
          <Card.Header className="bg-warning bg-gradient text-dark d-flex align-items-center justify-content-between">
            <div className="d-flex align-items-center gap-2">
              <FaExclamationTriangle /> 
              <strong>Alertas de Inventario - Predicciones IA</strong>
            </div>
            <Badge bg="danger" pill>{inventoryAlerts.length}</Badge>
          </Card.Header>
          <Card.Body>
            {loadingAlerts ? (
              <div className="text-center py-3">
                <Spinner size="medium" />
                <p className="mt-2 mb-0">Analizando inventario con IA...</p>
              </div>
            ) : (
              <div className="alert-list">
                {inventoryAlerts.map((alert, index) => (
                  <div 
                    key={index} 
                    className={`alert alert-${alert.nivel_riesgo === 'ALTO' ? 'danger' : alert.nivel_riesgo === 'MEDIO' ? 'warning' : 'info'} mb-3 d-flex align-items-start`}
                    style={{
                      borderLeft: `4px solid ${alert.nivel_riesgo === 'ALTO' ? '#dc3545' : alert.nivel_riesgo === 'MEDIO' ? '#ffc107' : '#0dcaf0'}`,
                      borderRadius: '8px'
                    }}
                  >
                    <FaExclamationTriangle className="me-2 mt-1" style={{ fontSize: '1.2rem' }} />
                    <div className="flex-grow-1">
                      <div className="d-flex align-items-center justify-content-between mb-2">
                        <strong>{alert.producto}</strong>
                        <Badge 
                          bg={alert.nivel_riesgo === 'ALTO' ? 'danger' : alert.nivel_riesgo === 'MEDIO' ? 'warning' : 'info'}
                          className="ms-2"
                        >
                          {alert.nivel_riesgo}
                        </Badge>
                      </div>
                      <p className="mb-1"><strong>Empresa:</strong> {alert.empresa}</p>
                      <p className="mb-1"><strong>Cantidad actual:</strong> {alert.cantidad_actual} unidades</p>
                      <p className="mb-0">
                        <strong>⚠️ {alert.alerta}</strong>
                        {alert.dias_hasta_quiebre !== null && (
                          <span className="ms-2">
                            <Badge bg="danger">{alert.dias_hasta_quiebre} días</Badge>
                          </span>
                        )}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card.Body>
        </Card>
      )}

      <Row className="mb-4">
        <Col md={4}>
          <FormField
            label="Filtrar por empresa"
            type="select"
            name="filterEmpresa"
            value={selectedEmpresa}
            onChange={(e) => setSelectedEmpresa(e.target.value)}
            options={[{ value: '', label: 'Todas las empresas' }, ...empresaOptions]}
          />
        </Col>
      </Row>

      {showForm && (
        <Card className="mb-4 shadow-sm">
          <Card.Header>
            <Card.Title className="mb-0">Agregar Producto al Inventario</Card.Title>
          </Card.Header>
          <Card.Body>
          <Form onSubmit={handleSubmit}>
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
            <FormField
              label="Producto"
              type="select"
              name="producto"
              value={formData.producto}
              onChange={handleChange}
              required
              error={errors.producto}
              options={productoOptions}
            />
            <FormField
              label="Cantidad"
              type="number"
              name="cantidad"
              value={formData.cantidad}
              onChange={handleChange}
              required
              error={errors.cantidad}
              placeholder="0"
            />
            <div className="d-flex gap-2">
              <Button type="submit" variant="primary" disabled={submitting} loading={submitting}>
                {submitting ? (
                  <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Spinner size="small" />
                    Agregando...
                  </span>
                ) : (
                  'Agregar'
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
        <Loading text="Cargando inventario" />
      ) : Object.keys(inventarioPorEmpresa).length === 0 ? (
        <Card className="text-center py-5">
          <Card.Body>
            <FaBox size={64} className="mb-3 text-muted" />
            <h4>No hay inventario disponible</h4>
            <p className="text-muted">Agrega productos al inventario para comenzar</p>
          </Card.Body>
        </Card>
      ) : (
        Object.entries(inventarioPorEmpresa).map(([empresaNombre, items]) => {
          const empresaNit = items[0].empresa;
          return (
            <Card key={empresaNit} className="mb-4 shadow-sm">
              <Card.Header className="d-flex justify-content-between align-items-center">
                <Card.Title className="mb-0">{empresaNombre}</Card.Title>
                <div className="d-flex gap-2">
                  <Button
                    size="small"
                    variant="success"
                    onClick={() => handleDownloadPDF(empresaNit)}
                    disabled={downloadingPDF === empresaNit}
                    loading={downloadingPDF === empresaNit}
                  >
                    {downloadingPDF === empresaNit ? (
                      <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <Spinner size="small" />
                        Descargando...
                      </span>
                    ) : (
                      <>
                        <FaDownload className="me-1" /> Descargar PDF
                      </>
                    )}
                  </Button>
                  <Button
                    size="small"
                    variant="primary"
                    onClick={() => handleSendEmail(empresaNit)}
                    disabled={sendingEmail === empresaNit}
                    loading={sendingEmail === empresaNit}
                  >
                    {sendingEmail === empresaNit ? (
                      <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <Spinner size="small" />
                        Enviando...
                      </span>
                    ) : (
                      <>
                        <FaPaperPlane className="me-1" /> Enviar PDF por Email
                      </>
                    )}
                  </Button>
                </div>
              </Card.Header>
              <Card.Body className="p-0">
                <Table responsive striped hover className="mb-0">
                  <thead className="table-dark">
                    <tr>
                      <th>Código</th>
                      <th>Producto</th>
                      <th>Cantidad</th>
                      <th>Precio USD</th>
                      <th>Precio EUR</th>
                      <th>Precio COP</th>
                      <th>Hash Transacción</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {items.map((item) => (
                      <tr key={item.id}>
                        <td>{item.producto_codigo}</td>
                        <td>{item.producto_nombre}</td>
                        <td><strong>{item.cantidad}</strong></td>
                        <td>${item.precio_usd}</td>
                        <td>€{item.precio_eur}</td>
                        <td>${item.precio_cop}</td>
                        <td className="font-monospace small">{item.transaccion_hash || 'N/A'}</td>
                        <td>
                          <Button
                            size="small"
                            variant="outline-primary"
                            onClick={() => {
                              setEditingItem(item);
                              setEditQuantity(item.cantidad.toString());
                            }}
                          >
                            <FaEdit className="me-1" /> Editar
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </Card.Body>
            </Card>
          );
        })
      )}

      {/* Modal para editar cantidad */}
      <Modal show={editingItem !== null} onHide={() => setEditingItem(null)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Editar Cantidad de Inventario</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {editingItem && (
            <>
              <p className="mb-3">
                <strong>Producto:</strong> {editingItem.producto_nombre}<br />
                <strong>Empresa:</strong> {editingItem.empresa_nombre}<br />
                <strong>Cantidad actual:</strong> {editingItem.cantidad}
              </p>
              <Form
                onSubmit={async (e) => {
                  e.preventDefault();
                  setUpdatingQuantity(true);
                  try {
                    await api.patch(`/api/inventario/${editingItem.id}/`, {
                      cantidad: parseInt(editQuantity)
                    });
                    setSuccessMessage('Cantidad actualizada exitosamente');
                    setEditingItem(null);
                    setEditQuantity('');
                    if (selectedEmpresa) {
                      fetchInventarioByEmpresa(selectedEmpresa);
                    } else {
                      fetchInventario();
                    }
                    // Actualizar alertas si están cargadas
                    if (inventoryAlerts.length > 0) {
                      fetchInventoryAlerts();
                    }
                    setTimeout(() => setSuccessMessage(null), 5000);
                  } catch (error) {
                    setErrorMessage(error.response?.data?.cantidad?.[0] || error.response?.data?.detail || 'Error al actualizar la cantidad');
                    setTimeout(() => setErrorMessage(null), 5000);
                  } finally {
                    setUpdatingQuantity(false);
                  }
                }}
              >
                <FormField
                  label="Nueva Cantidad"
                  type="number"
                  name="cantidad"
                  value={editQuantity}
                  onChange={(e) => setEditQuantity(e.target.value)}
                  required
                  placeholder="0"
                  min="0"
                />
                <div className="d-flex gap-2 mt-3">
                  <Button type="submit" variant="primary" disabled={updatingQuantity} loading={updatingQuantity}>
                    {updatingQuantity ? (
                      <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <Spinner size="small" />
                        Actualizando...
                      </span>
                    ) : (
                      'Actualizar'
                    )}
                  </Button>
                  <Button type="button" variant="secondary" onClick={() => setEditingItem(null)} disabled={updatingQuantity}>
                    Cancelar
                  </Button>
                </div>
              </Form>
            </>
          )}
        </Modal.Body>
      </Modal>

      {/* Modal para ingresar email al enviar PDF */}
      <Modal 
        show={showEmailModal} 
        onHide={() => {
          setShowEmailModal(false);
          setEmailToSend('');
          setEmailError('');
          setSelectedEmpresaForEmail(null);
        }} 
        centered
        backdrop="static"
        size="lg"
      >
        <Modal.Header 
          className="bg-primary text-white border-0"
          style={{
            background: 'linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%)',
            padding: '1.25rem 1.5rem'
          }}
        >
          <Modal.Title className="d-flex align-items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" className="bi bi-envelope" viewBox="0 0 16 16">
              <path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm2-1a1 1 0 0 0-1 1v.217l7 4.2 7-4.2V4a1 1 0 0 0-1-1zm13 2.383-4.708 2.825L15 11.105zm-.034 6.876-5.64-3.471L8 9.583l-1.326-.795-5.64 3.47A1 1 0 0 0 2 13h12a1 1 0 0 0 .966-.741M1 11.105l4.708-2.897L1 5.383z"/>
            </svg>
            Enviar PDF por Correo Electrónico
          </Modal.Title>
          <button
            type="button"
            className="btn-close btn-close-white"
            onClick={() => {
              setShowEmailModal(false);
              setEmailToSend('');
              setEmailError('');
              setSelectedEmpresaForEmail(null);
            }}
            aria-label="Cerrar"
          ></button>
        </Modal.Header>
        <Modal.Body className="p-4">
          {selectedEmpresaForEmail && (
            <div className="mb-4 p-3 rounded" style={{ backgroundColor: '#e7f3ff', borderLeft: '4px solid #0d6efd' }}>
              <p className="mb-0">
                <strong>Empresa:</strong> {empresas.find(emp => emp.nit === selectedEmpresaForEmail)?.nombre || selectedEmpresaForEmail}
              </p>
              <p className="mb-0 text-muted small">
                Se enviará el PDF del inventario al correo electrónico que ingrese a continuación.
              </p>
            </div>
          )}
          <Form onSubmit={handleEmailSubmit}>
            <FormField
              label="Correo Electrónico del Destinatario"
              type="email"
              name="email"
              value={emailToSend}
              onChange={(e) => {
                setEmailToSend(e.target.value);
                setEmailError('');
              }}
              required
              placeholder="ejemplo@correo.com"
              error={emailError}
            />
            {emailError && (
              <div className="alert alert-danger d-flex align-items-center gap-2 mt-2" role="alert">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" className="bi bi-exclamation-triangle" viewBox="0 0 16 16">
                  <path d="M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.146.146 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.163.163 0 0 1-.054.06.116.116 0 0 1-.066.017H1.146a.115.115 0 0 1-.066-.017.163.163 0 0 1-.054-.06.176.176 0 0 1 .002-.183L7.884 2.073a.147.147 0 0 1 .054-.057m1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767z"/>
                  <path d="M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z"/>
                </svg>
                <span>{emailError}</span>
              </div>
            )}
            <div className="mt-3 p-3 rounded" style={{ backgroundColor: '#f8f9fa', border: '1px solid #dee2e6' }}>
              <p className="mb-0 small text-muted d-flex align-items-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-send me-2" viewBox="0 0 16 16">
                  <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm1.12-4.696L14.13 2.576 5.777 6.464z"/>
                </svg>
                El PDF del inventario será generado y enviado automáticamente al correo especificado.
              </p>
            </div>
            <div className="d-flex gap-2 mt-4">
              <Button 
                type="submit" 
                variant="primary" 
                className="flex-grow-1"
                disabled={!emailToSend || sendingEmail === selectedEmpresaForEmail}
              >
                {sendingEmail === selectedEmpresaForEmail ? (
                  <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
                    <Spinner size="small" />
                    Enviando...
                  </span>
                ) : (
                  <>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-send me-2" viewBox="0 0 16 16">
                      <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm1.12-4.696L14.13 2.576 5.777 6.464z"/>
                    </svg>
                    Enviar PDF
                  </>
                )}
              </Button>
              <Button 
                type="button" 
                variant="secondary" 
                onClick={() => {
                  setShowEmailModal(false);
                  setEmailToSend('');
                  setEmailError('');
                  setSelectedEmpresaForEmail(null);
                }}
                disabled={sendingEmail === selectedEmpresaForEmail}
              >
                Cancelar
              </Button>
            </div>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
};

export default Inventario;

