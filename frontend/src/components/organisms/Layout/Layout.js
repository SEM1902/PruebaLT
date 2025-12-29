import React from 'react';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../../context/AuthContext';
import { Navbar, Nav, Container } from 'react-bootstrap';
import { FaChartBar } from 'react-icons/fa';
import Button from '../../atoms/Button/Button';
import Chatbot from '../Chatbot/Chatbot';
import './Layout.css';

const Layout = () => {
  const { user, logout, isAdministrador } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="layout">
      <Navbar bg="dark" variant="dark" expand="lg" className="mb-4">
        <Container>
          <Navbar.Brand as={Link} to="/empresas" className="d-flex align-items-center gap-2">
            <FaChartBar /> Sistema de Gestión
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link as={Link} to="/empresas">Empresas</Nav.Link>
              {isAdministrador() && (
                <>
                  <Nav.Link as={Link} to="/productos">Productos</Nav.Link>
                  <Nav.Link as={Link} to="/inventario">Inventario</Nav.Link>
                </>
              )}
            </Nav>
            <Nav className="ms-auto align-items-center">
              <Navbar.Text className="me-3 text-white">
                <span className="me-2">{user?.email}</span>
                <span className="text-light">({user?.rol})</span>
              </Navbar.Text>
              <Button variant="secondary" size="small" onClick={handleLogout}>
                Cerrar Sesión
              </Button>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <main className="layout-main">
        <Container>
          <Outlet />
        </Container>
      </main>
      <Chatbot />
    </div>
  );
};

export default Layout;

