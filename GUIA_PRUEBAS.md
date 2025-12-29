# Guía de Pruebas - Capa de Dominio

## 🧪 Cómo Probar el Proyecto

### 1. Verificación Rápida (Sin Django)

Verificar que la capa de dominio funciona independientemente:

```bash
cd backend
python3 setup_domain.py
```

**Salida esperada:**
```
============================================================
Verificación de la Capa de Dominio
============================================================
✓ Ruta del dominio encontrada: /Users/sem/Documents/Prueba/domain/src
✓ Entidades de dominio importadas correctamente

Entidades disponibles:
  - Empresa
  - Producto
  - Inventario

✓ Adaptadores importados correctamente

============================================================
✓ CONFIGURACIÓN CORRECTA
============================================================
```

---

### 2. Prueba de Entidades de Dominio (Python Puro)

**Opción A: Usar el script de prueba (Recomendado)**

```bash
cd backend
python3 test_dominio.py
```

**Opción B: Crear un script de prueba manual**

Crear archivo `test_manual.py`:

```python
from domain_layer.entities import Empresa, Producto, Inventario
from decimal import Decimal

# Probar creación de Empresa
empresa = Empresa(
    nit='123456789',
    nombre='Empresa Test',
    direccion='Calle 123',
    telefono='3001234567'
)
print('✓ Empresa creada:', empresa)

# Probar creación de Producto
producto = Producto(
    codigo='PROD001',
    nombre='Producto Test',
    caracteristicas='Características',
    precio_usd=Decimal('100.00'),
    precio_eur=Decimal('92.00'),
    precio_cop=Decimal('400000.00'),
    empresa_nit='123456789'
)
print('✓ Producto creado:', producto)

# Probar creación de Inventario
inventario = Inventario(
    empresa_nit='123456789',
    producto_codigo='PROD001',
    cantidad=50
)
print('✓ Inventario creado:', inventario)

# Probar validaciones
try:
    empresa_invalida = Empresa(
        nit='123',  # Muy corto
        nombre='Test',
        direccion='Test',
        telefono='123'
    )
except ValueError as e:
    print('✓ Validación funciona:', str(e))

print('\n✅ TODAS LAS PRUEBAS PASARON')
```

Ejecutar:
```bash
cd backend
python3 test_manual.py
```

---

### 3. Prueba de Integración con Django

#### 3.1. Iniciar el servidor Django

```bash
cd backend
source venv/bin/activate  # Si tienes venv
python manage.py runserver
```

#### 3.2. Probar que los modelos Django funcionan

Abrir el shell de Django:

```bash
cd backend
python manage.py shell
```

En el shell:

```python
# Importar modelos Django (deben funcionar igual que antes)
from api.models import Empresa, Producto, Inventario

# Crear una empresa usando el modelo Django (método tradicional)
empresa = Empresa.objects.create(
    nit='987654321',
    nombre='Empresa Django',
    direccion='Dirección Test',
    telefono='3009876543'
)
print('✓ Empresa creada con Django:', empresa)

# Probar conversión a entidad de dominio
domain_empresa = empresa.to_domain()
print('✓ Convertida a dominio:', domain_empresa)
print('✓ Tipo:', type(domain_empresa))

# Probar actualización usando entidad de dominio
domain_empresa.actualizar_datos(nombre='Empresa Actualizada')
empresa_actualizada = Empresa.from_domain(domain_empresa)
print('✓ Empresa actualizada desde dominio:', empresa_actualizada.nombre)

# Verificar que sigue siendo un modelo Django
print('✓ Es modelo Django:', isinstance(empresa_actualizada, Empresa))
```

---

### 4. Prueba de APIs REST (Sin Cambios)

Las APIs deben funcionar exactamente igual que antes:

#### 4.1. Probar Login

```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@test.com", "password": "password123"}'
```

#### 4.2. Probar Crear Empresa

```bash
curl -X POST http://localhost:8000/api/empresas/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "nit": "111222333",
    "nombre": "Empresa Test API",
    "direccion": "Calle Test 123",
    "telefono": "3001112222"
  }'
```

#### 4.3. Probar Listar Empresas

```bash
curl -X GET http://localhost:8000/api/empresas/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Resultado esperado**: Las APIs funcionan exactamente igual que antes.

---

### 5. Prueba de Adaptadores

Crear un script de prueba de adaptadores:

```python
# test_adapters.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import Empresa, Producto, Inventario
from api.domain_adapters import EmpresaAdapter, ProductoAdapter, InventarioAdapter
from domain_layer.entities import Empresa as DomainEmpresa, Producto as DomainProducto, Inventario as DomainInventario
from decimal import Decimal

print("=" * 60)
print("PRUEBA DE ADAPTADORES")
print("=" * 60)

# 1. Crear empresa en Django
django_empresa = Empresa.objects.create(
    nit='555666777',
    nombre='Empresa Adaptador',
    direccion='Dirección Test',
    telefono='3005556666'
)
print(f"✓ Empresa Django creada: {django_empresa}")

# 2. Convertir a dominio
domain_empresa = EmpresaAdapter.to_domain(django_empresa)
print(f"✓ Convertida a dominio: {domain_empresa}")
print(f"  Tipo: {type(domain_empresa)}")

# 3. Modificar en dominio
domain_empresa.actualizar_datos(nombre='Empresa Modificada')
print(f"✓ Modificada en dominio: {domain_empresa.nombre}")

# 4. Convertir de vuelta a Django
django_empresa_actualizada = EmpresaAdapter.to_django(domain_empresa)
django_empresa_actualizada.save()
print(f"✓ Guardada en Django: {django_empresa_actualizada.nombre}")

# 5. Verificar persistencia
empresa_verificada = Empresa.objects.get(nit='555666777')
print(f"✓ Verificada en BD: {empresa_verificada.nombre}")

print("\n✅ TODAS LAS PRUEBAS DE ADAPTADORES PASARON")
```

Ejecutar:

```bash
cd backend
python test_adapters.py
```

---

### 6. Prueba de Validaciones de Negocio

```python
# test_validations.py
from domain_layer.entities import Empresa, Producto, Inventario
from decimal import Decimal

print("=" * 60)
print("PRUEBA DE VALIDACIONES")
print("=" * 60)

# Test 1: NIT inválido (muy corto)
try:
    empresa = Empresa(nit='123', nombre='Test', direccion='Test', telefono='123')
    print("✗ ERROR: Debería fallar con NIT corto")
except ValueError as e:
    print(f"✓ Validación NIT funciona: {e}")

# Test 2: Precio negativo
try:
    producto = Producto(
        codigo='TEST',
        nombre='Test',
        caracteristicas='Test',
        precio_usd=Decimal('-10'),
        precio_eur=Decimal('0'),
        precio_cop=Decimal('0'),
        empresa_nit='123456789'
    )
    print("✗ ERROR: Debería fallar con precio negativo")
except ValueError as e:
    print(f"✓ Validación precio funciona: {e}")

# Test 3: Cantidad negativa
try:
    inventario = Inventario(
        empresa_nit='123456789',
        producto_codigo='TEST',
        cantidad=-5
    )
    print("✗ ERROR: Debería fallar con cantidad negativa")
except ValueError as e:
    print(f"✓ Validación cantidad funciona: {e}")

print("\n✅ TODAS LAS VALIDACIONES FUNCIONAN")
```

---

### 7. Prueba End-to-End (Flujo Completo)

```python
# test_e2e.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import Empresa, Producto, Inventario
from api.domain_adapters import EmpresaAdapter, ProductoAdapter, InventarioAdapter
from domain_layer.entities import Empresa as DomainEmpresa, Producto as DomainProducto, Inventario as DomainInventario
from decimal import Decimal

print("=" * 60)
print("PRUEBA END-TO-END")
print("=" * 60)

# 1. Crear empresa usando entidad de dominio
domain_empresa = DomainEmpresa(
    nit='999888777',
    nombre='Empresa E2E',
    direccion='Dirección E2E',
    telefono='3009998888'
)
print(f"✓ Empresa dominio creada: {domain_empresa}")

# 2. Persistir usando adaptador
django_empresa = EmpresaAdapter.to_django(domain_empresa)
django_empresa.save()
print(f"✓ Empresa persistida: {django_empresa}")

# 3. Crear producto usando entidad de dominio
domain_producto = DomainProducto(
    codigo='E2E001',
    nombre='Producto E2E',
    caracteristicas='Características E2E',
    precio_usd=Decimal('50.00'),
    precio_eur=Decimal('46.00'),
    precio_cop=Decimal('200000.00'),
    empresa_nit='999888777'
)
print(f"✓ Producto dominio creado: {domain_producto}")

# 4. Persistir producto
django_producto = ProductoAdapter.to_django(domain_producto, django_empresa)
django_producto.save()
print(f"✓ Producto persistido: {django_producto}")

# 5. Crear inventario usando entidad de dominio
domain_inventario = DomainInventario(
    empresa_nit='999888777',
    producto_codigo='E2E001',
    cantidad=100
)
print(f"✓ Inventario dominio creado: {domain_inventario}")

# 6. Persistir inventario
django_inventario = InventarioAdapter.to_django(domain_inventario, django_empresa, django_producto)
django_inventario.save()
print(f"✓ Inventario persistido: {django_inventario}")

# 7. Leer de vuelta y convertir a dominio
empresa_leida = Empresa.objects.get(nit='999888777')
empresa_domain = empresa_leida.to_domain()
print(f"✓ Empresa leída y convertida: {empresa_domain}")

print("\n✅ PRUEBA END-TO-END COMPLETADA")
```

---

## 📋 Checklist de Pruebas

- [ ] Verificación rápida (`setup_domain.py`)
- [ ] Prueba de entidades de dominio (Python puro)
- [ ] Prueba de integración con Django (shell)
- [ ] Prueba de APIs REST (sin cambios)
- [ ] Prueba de adaptadores
- [ ] Prueba de validaciones de negocio
- [ ] Prueba end-to-end (flujo completo)

---

## 🎯 Para la Exposición

### Demostración en Vivo

1. **Mostrar estructura de archivos**
   ```bash
   tree domain/src/domain_layer/
   ```

2. **Mostrar que funciona sin Django**
   ```bash
   python3 -c "from domain_layer.entities import Empresa; print('✓ OK')"
   ```

3. **Mostrar que Django funciona igual**
   ```bash
   python manage.py shell
   # Crear empresa normalmente
   ```

4. **Mostrar adaptadores**
   ```python
   empresa.to_domain()  # Convertir a dominio
   Empresa.from_domain(domain_empresa)  # Crear desde dominio
   ```

5. **Mostrar validaciones**
   ```python
   # Intentar crear con datos inválidos
   # Mostrar que las validaciones funcionan
   ```

---

## ✅ Resultados Esperados

- ✅ Capa de dominio funciona independientemente
- ✅ Django funciona exactamente igual que antes
- ✅ Adaptadores funcionan correctamente
- ✅ Validaciones de negocio funcionan
- ✅ APIs REST funcionan sin cambios
- ✅ No se rompió funcionalidad existente

