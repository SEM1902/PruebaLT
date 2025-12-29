# Actualizar librería OpenAI

Para resolver el error `__init__() got an unexpected keyword argument 'proxies'`, necesitas actualizar la librería OpenAI.

## Pasos para actualizar:

1. **Activar el entorno virtual:**
   ```bash
   cd backend
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. **Actualizar la librería OpenAI:**
   ```bash
   pip install --upgrade openai
   ```

   O si prefieres instalar desde requirements.txt:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Verificar la instalación:**
   ```bash
   pip show openai
   ```

4. **Reiniciar el servidor Django:**
   - Detén el servidor si está corriendo (Ctrl+C)
   - Inícialo de nuevo: `python manage.py runserver`

## ¿Por qué ocurre este error?

El error se debe a una incompatibilidad entre la versión antigua de OpenAI (1.3.0) y la librería `httpx`. Las versiones más recientes de OpenAI (1.12.0+) han solucionado este problema.

Después de actualizar, la funcionalidad de sugerencias de IA debería funcionar correctamente.

