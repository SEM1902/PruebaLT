# Sistema de Gestión de Empresas y Productos

Sistema completo desarrollado con Django, React y PostgreSQL que permite gestionar empresas, productos e inventarios con funcionalidades avanzadas de IA y Blockchain.

## Características Principales

- ✅ **Gestión de Empresas**: CRUD completo con validaciones
- ✅ **Gestión de Productos**: Productos con precios en múltiples monedas (USD, EUR, COP)
- ✅ **Inventario**: Sistema de inventario por empresa con hash de blockchain
- ✅ **Autenticación JWT**: Sistema de login seguro con contraseñas encriptadas
- ✅ **Roles de Usuario**: Administrador y Externo con permisos diferenciados
- ✅ **Generación de PDFs**: Exportación de inventarios a PDF
- ✅ **Envío de Emails**: Envío de PDFs por correo electrónico
- ✅ **IA Integrada**: Sugerencias de productos usando OpenAI
- ✅ **Blockchain**: Hash de transacciones para el inventario
- ✅ **Atomic Design**: Estructura de componentes siguiendo Atomic Design

## Tecnologías Utilizadas

### Backend
- Django 4.2.7
- Django REST Framework
- PostgreSQL
- JWT Authentication
- ReportLab (PDFs)
- OpenAI API
- Web3 (Blockchain)

### Frontend
- React 18.2.0
- React Router DOM
- Axios
- Atomic Design Pattern

## Instalación

### Prerrequisitos
- Python 3.8+
- Node.js 14+
- PostgreSQL
- npm o yarn

### Backend

1. Navegar a la carpeta del backend:
```bash
cd backend
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno. Crear un archivo `.env` en la carpeta `backend`:
```env
SECRET_KEY=tu-secret-key-aqui
DB_NAME=prueba_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password
OPENAI_API_KEY=tu-openai-api-key
```

5. Crear la base de datos PostgreSQL:
```sql
CREATE DATABASE prueba_db;
```

6. Ejecutar migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Crear un superusuario:
```bash
python manage.py createsuperuser
```

8. Iniciar el servidor:
```bash
python manage.py runserver
```

El backend estará disponible en `http://localhost:8000`

### Frontend

1. Navegar a la carpeta del frontend:
```bash
cd frontend
```

2. Instalar dependencias:
```bash
npm install
```

3. Iniciar el servidor de desarrollo:
```bash
npm start
```

El frontend estará disponible en `http://localhost:3000`

## Estructura del Proyecto

```
Prueba/
├── backend/
│   ├── api/                 # Aplicación principal
│   │   ├── models.py        # Modelos de datos
│   │   ├── views.py         # Vistas y endpoints
│   │   ├── serializers.py   # Serializadores
│   │   ├── utils.py         # Utilidades (PDF, Blockchain)
│   │   └── services.py      # Servicios (IA)
│   ├── config/              # Configuración Django
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── atoms/       # Componentes básicos
│   │   │   ├── molecules/   # Componentes compuestos
│   │   │   └── organisms/   # Componentes complejos
│   │   ├── pages/           # Páginas principales
│   │   ├── context/         # Context API
│   │   └── services/        # Servicios API
│   └── public/
└── README.md
```

## Funcionalidades por Rol

### Administrador
- Crear, editar y eliminar empresas
- Crear, editar y eliminar productos
- Gestionar inventario
- Descargar PDFs de inventario
- Enviar PDFs por email
- Ver sugerencias de productos con IA

### Externo
- Ver empresas (solo lectura)
- Visualizar productos e inventario

## API Endpoints

### Autenticación
- `POST /api/login/` - Iniciar sesión

### Empresas
- `GET /api/empresas/` - Listar empresas
- `POST /api/empresas/` - Crear empresa (Admin)
- `GET /api/empresas/{nit}/` - Obtener empresa
- `PUT /api/empresas/{nit}/` - Actualizar empresa (Admin)
- `DELETE /api/empresas/{nit}/` - Eliminar empresa (Admin)

### Productos
- `GET /api/productos/` - Listar productos (Admin)
- `POST /api/productos/` - Crear producto (Admin)
- `GET /api/productos/{id}/` - Obtener producto
- `PUT /api/productos/{id}/` - Actualizar producto (Admin)
- `DELETE /api/productos/{id}/` - Eliminar producto (Admin)
- `GET /api/productos/{id}/ai_suggestions/` - Obtener sugerencias IA

### Inventario
- `GET /api/inventario/` - Listar inventario (Admin)
- `POST /api/inventario/` - Agregar al inventario (Admin)
- `GET /api/inventario/by_empresa/{nit}/` - Inventario por empresa
- `GET /api/inventario/pdf/{nit}/` - Descargar PDF
- `POST /api/inventario/send-pdf/{nit}/` - Enviar PDF por email

## Funcionalidades Adicionales

### IA (OpenAI)
- Sugerencias de productos complementarios basadas en características
- Endpoint: `GET /api/productos/{id}/ai_suggestions/`

### Blockchain
- Hash SHA-256 generado para cada transacción de inventario
- Almacenado en el campo `transaccion_hash` del modelo Inventario
- Simula transacciones de blockchain para trazabilidad

## Buenas Prácticas Implementadas

- ✅ Código limpio y estructurado
- ✅ Atomic Design en frontend
- ✅ Separación de responsabilidades
- ✅ Validaciones en backend y frontend
- ✅ Manejo de errores
- ✅ Contraseñas encriptadas (Django Auth)
- ✅ Permisos basados en roles
- ✅ Documentación de código

## Notas Adicionales

- Las contraseñas se encriptan automáticamente usando el sistema de autenticación de Django
- Para usar la funcionalidad de IA, es necesario configurar `OPENAI_API_KEY` en las variables de entorno
- Para el envío de emails, configurar las credenciales SMTP en `.env`
- El hash de blockchain se genera automáticamente al agregar productos al inventario

## Desarrollo

Para desarrollo, ambos servidores (backend y frontend) deben estar ejecutándose simultáneamente.

## Licencia

Este proyecto fue desarrollado como prueba técnica.

