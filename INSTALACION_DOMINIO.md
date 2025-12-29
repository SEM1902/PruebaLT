# Instalación de la Capa de Dominio

## ⚠️ IMPORTANTE: Instalación NO Requerida

**La capa de dominio ya está configurada para funcionar sin instalación.**

El archivo `backend/config/settings.py` ya agrega automáticamente la ruta del dominio al PYTHONPATH, por lo que **NO es necesario instalar el paquete**. El proyecto funcionará correctamente sin ejecutar ningún comando de instalación.

Para verificar que funciona:
```bash
cd backend
python3 -c "from domain_layer.entities import Empresa; print('✓ OK')"
```

## Instalación Opcional (Solo si deseas usar Poetry)

Si prefieres instalar el paquete como dependencia gestionada por Poetry:

### Opción 1: Usando Poetry (Recomendado)

1. Navegar a la carpeta del dominio:
```bash
cd domain
```

2. Instalar dependencias con Poetry:
```bash
poetry install
```

3. Instalar el paquete en modo desarrollo desde el backend:
```bash
cd ../backend
poetry install ../domain
```

O si estás usando pip:
```bash
pip install -e ../domain
```

### Opción 2: Usando pip directamente

Desde el backend, con el entorno virtual activado:
```bash
cd backend
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -e ../domain
```

O sin activar el entorno virtual (usando python3):
```bash
cd backend
python3 -m pip install -e ../domain
```

### Opción 3: Configuración Automática

Ejecutar el script de configuración desde el backend:
```bash
cd backend
python setup_domain.py
```

**Nota**: Si tienes problemas con permisos, asegúrate de:
1. Activar el entorno virtual primero
2. O usar `python3 -m pip install --user -e ../domain`

## Verificación

Para verificar que funciona (sin instalación):
```bash
cd backend
python3 -c "from domain_layer.entities import Empresa, Producto, Inventario; print('✓ Capa de dominio importada correctamente')"
```

O desde Python:
```python
from domain_layer.entities import Empresa, Producto, Inventario
print("✓ Capa de dominio importada correctamente")
```

## Notas

- **NO es necesario instalar el paquete**: El backend ya está configurado en `backend/config/settings.py` para importar el dominio directamente desde la ruta
- El paquete de dominio está configurado en `domain/pyproject.toml` (para uso con Poetry si se desea)
- Los adaptadores están en `backend/api/domain_adapters.py`
- La configuración automática en `settings.py` agrega `domain/src` al PYTHONPATH

