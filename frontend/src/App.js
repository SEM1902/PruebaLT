import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Login from './pages/Login';
import Empresas from './pages/Empresas';
import Productos from './pages/Productos';
import Inventario from './pages/Inventario';
import PrivateRoute from './components/organisms/PrivateRoute';
import Layout from './components/organisms/Layout';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={
              <PrivateRoute>
                <Layout />
              </PrivateRoute>
            }
          >
            <Route index element={<Navigate to="/empresas" replace />} />
            <Route path="empresas" element={<Empresas />} />
            <Route path="productos" element={<Productos />} />
            <Route path="inventario" element={<Inventario />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;

