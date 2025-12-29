# Instrucciones de Instalación y Uso

## Configuración Inicial

### 1. Base de Datos PostgreSQL

Crear la base de datos:
```sql
CREATE DATABASE prueba_db;
```

### 2. Configurar Variables de Entorno

En la carpeta `backend`, copiar `env.example` a `.env` y configurar las variables:

```bash
cd backend
cp env.example .env
```

Editar `.env` con tus credenciales:
- `SECRET_KEY`: Generar una clave secreta para Django
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`: Credenciales de PostgreSQL
- `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`: Credenciales para envío de emails
- `OPENAI_API_KEY`: Clave API de OpenAI (opcional, para funcionalidad de IA)

### 3. Instalar Dependencias Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Ejecutar Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear Usuario Administrador

```bash
python manage.py createsuperuser
```

Seguir las instrucciones para crear un usuario administrador.

### 6. Crear Usuario Externo 

Puedes crear usuarios externos desde el admin de Django o usando el shell:

```bash
python manage.py shell
```

```python
from api.models import User

# Crear usuario externo
user = User.objects.create_user(
    email='externo@ejemplo.com',
    password='password123',
    rol='EXTERNO'
)
```

### 7. Instalar Dependencias Frontend

```bash
cd frontend
npm install
```

### 8. Ejecutar Servidores

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

## Uso de la Aplicación

### Login

Acceder a `http://localhost:3000/login` y usar las credenciales del usuario creado.

### Roles

- **Administrador**: Puede crear, editar y eliminar empresas, productos e inventario
- **Externo**: Solo puede visualizar empresas

### Funcionalidades

1. **Empresas**: Gestión completa de empresas (solo Administrador puede crear/editar/eliminar)
2. **Productos**: Gestión de productos con precios en USD, EUR y COP (solo Administrador)
3. **Inventario**: Gestión de inventario por empresa con:
   - Hash de blockchain para cada transacción
   - Descarga de PDF
   - Envío de PDF por email
4. **IA**: Sugerencias de productos (endpoint: `/api/productos/{id}/ai_suggestions/`)

## Notas Importantes

- Las contraseñas se encriptan automáticamente usando Django Auth
- El hash de blockchain se genera automáticamente al agregar productos al inventario
- Para usar la funcionalidad de IA, necesitas configurar `OPENAI_API_KEY`
- Para enviar emails, configurar las credenciales SMTP en `.env`
  - **Gmail**: Requiere una "Contraseña de aplicación" (ver `CONFIGURACION_EMAIL.md`)
  - Consulta `CONFIGURACION_EMAIL.md` para instrucciones detalladas de configuración

