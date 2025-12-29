# Ejemplo de Uso de la Capa de Dominio

## Crear una Entidad de Dominio

```python
from domain_layer.entities import Empresa, Producto, Inventario
from decimal import Decimal
from datetime import datetime

# Crear una empresa
empresa = Empresa(
    nit="123456789",
    nombre="Mi Empresa S.A.",
    direccion="Calle 123 #45-67",
    telefono="3001234567"
)

# Crear un producto
producto = Producto(
    codigo="PROD001",
    nombre="Producto Ejemplo",
    caracteristicas="Características del producto",
    precio_usd=Decimal("100.00"),
    precio_eur=Decimal("92.00"),
    precio_cop=Decimal("400000.00"),
    empresa_nit="123456789"
)

# Crear inventario
inventario = Inventario(
    empresa_nit="123456789",
    producto_codigo="PROD001",
    cantidad=50
)
```

## Usar con Django (a través de adaptadores)

```python
from api.domain_adapters import EmpresaAdapter, ProductoAdapter, InventarioAdapter
from api.models import Empresa, Producto, Inventario

# Convertir modelo Django a entidad de dominio
django_empresa = Empresa.objects.get(nit="123456789")
domain_empresa = EmpresaAdapter.to_domain(django_empresa)

# Actualizar datos usando la entidad de dominio
domain_empresa.actualizar_datos(nombre="Nuevo Nombre")

# Guardar cambios de vuelta a Django
django_empresa = EmpresaAdapter.to_django(domain_empresa)
django_empresa.save()

# O usar el método del modelo directamente
django_empresa = Empresa.from_domain(domain_empresa)
```

## Validaciones de Negocio

Las entidades de dominio incluyen validaciones automáticas:

```python
# Esto lanzará ValueError si el NIT no es válido
try:
    empresa = Empresa(
        nit="123",  # Muy corto
        nombre="Test",
        direccion="Test",
        telefono="123"
    )
except ValueError as e:
    print(f"Error de validación: {e}")

# Las validaciones también se aplican en métodos de actualización
empresa = Empresa(...)
try:
    empresa.actualizar_datos(nombre="")  # Nombre vacío
except ValueError as e:
    print(f"Error: {e}")
```

## Ventajas

1. **Independencia**: Las entidades no dependen de Django
2. **Testabilidad**: Fácil de probar sin necesidad de base de datos
3. **Reutilización**: Pueden usarse en otros proyectos
4. **Validaciones**: Reglas de negocio centralizadas
5. **Mantenibilidad**: Cambios en el dominio no afectan la infraestructura

