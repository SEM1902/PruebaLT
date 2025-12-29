# Configuración de Email para Envío de PDFs

Para que la funcionalidad de envío de PDFs por email funcione correctamente, necesitas configurar las credenciales de email en el archivo `.env` del backend.

## Configuración para Gmail

### 1. Generar una Contraseña de Aplicación

Gmail requiere una "Contraseña de aplicación" en lugar de tu contraseña normal por motivos de seguridad.

**Pasos:**

1. Ve a tu cuenta de Google: https://myaccount.google.com/
2. Activa la verificación en dos pasos (si no está activada):
   - Ve a Seguridad → Verificación en dos pasos
   - Sigue las instrucciones para activarla
3. Genera una contraseña de aplicación:
   - Ve a Seguridad → Verificación en dos pasos
   - Al final de la página, busca "Contraseñas de aplicaciones"
   - Selecciona "Correo" y el dispositivo (puedes elegir "Otro" y escribir "Django")
   - Copia la contraseña de 16 caracteres que se genera

### 2. Configurar el archivo .env

Edita el archivo `backend/.env` y agrega/modifica estas líneas:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=la-contraseña-de-aplicación-de-16-caracteres
```

**⚠️ IMPORTANTE - No confundir estas variables:**
- `EMAIL_HOST`: Debe ser el servidor SMTP (ej: `smtp.gmail.com`) - NO tu email
- `EMAIL_HOST_USER`: Tu dirección de email de Gmail completa (ej: `tu-email@gmail.com`)
- `EMAIL_HOST_PASSWORD`: La contraseña de aplicación de 16 caracteres generada en el paso anterior (NO tu contraseña normal de Gmail)

**Ejemplo correcto:**
```env
EMAIL_HOST=smtp.gmail.com                    # ✅ Correcto: servidor SMTP
EMAIL_HOST_USER=estradamontoyasimon803@gmail.com  # ✅ Correcto: tu email
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop      # ✅ Correcto: contraseña de aplicación
```

**Ejemplo incorrecto:**
```env
EMAIL_HOST=estradamontoyasimon803@gmail.com  # ❌ INCORRECTO: esto debe ser smtp.gmail.com
```

### 3. Reiniciar el servidor

Después de configurar el `.env`, reinicia el servidor de Django:

```bash
# Detener el servidor (Ctrl+C) y volver a iniciarlo
python manage.py runserver
```

## Configuración para Otros Proveedores

### Outlook/Hotmail

```env
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@outlook.com
EMAIL_HOST_PASSWORD=tu-contraseña
```

### Yahoo

```env
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@yahoo.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicación
```

### SendGrid (Recomendado para producción)

```env
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=tu-api-key-de-sendgrid
```

## Solución de Problemas

### Error: "Authentication Required"

- Asegúrate de estar usando una contraseña de aplicación (no tu contraseña normal)
- Verifica que la verificación en dos pasos esté activada en tu cuenta de Google
- Verifica que `EMAIL_HOST_USER` y `EMAIL_HOST_PASSWORD` estén correctamente configurados en `.env`

### Error: "EMAIL_HOST_USER no está configurado"

- Verifica que el archivo `.env` exista en la carpeta `backend/`
- Asegúrate de que las variables `EMAIL_HOST_USER` y `EMAIL_HOST_PASSWORD` estén definidas
- Reinicia el servidor de Django después de modificar el `.env`

### Error: "webmaster@localhost"

- Esto significa que `EMAIL_HOST_USER` no se está leyendo correctamente
- Verifica que el archivo `.env` esté en la ubicación correcta (`backend/.env`)
- Asegúrate de que no haya espacios antes o después del signo `=` en las variables del `.env`

## Nota de Seguridad

- **NUNCA** subas el archivo `.env` a un repositorio Git
- El archivo `.env` ya está incluido en `.gitignore` para proteger tus credenciales
- Para producción, usa variables de entorno del sistema o servicios de gestión de secretos

