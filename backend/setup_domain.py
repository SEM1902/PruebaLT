"""
Script para verificar la configuración de la capa de dominio.
NOTA: La instalación NO es necesaria - el dominio ya está configurado en settings.py
Ejecutar: python setup_domain.py
"""

import sys
from pathlib import Path

# Obtener la ruta del proyecto
project_root = Path(__file__).resolve().parent.parent
domain_path = project_root / "domain" / "src"

print("=" * 60)
print("Verificación de la Capa de Dominio")
print("=" * 60)

# Verificar que la ruta existe
if not domain_path.exists():
    print(f"✗ ERROR: La ruta del dominio no existe: {domain_path}")
    sys.exit(1)

print(f"✓ Ruta del dominio encontrada: {domain_path}")

# Intentar importar el dominio
try:
    # Agregar temporalmente al path
    if str(domain_path) not in sys.path:
        sys.path.insert(0, str(domain_path))
    
    from domain_layer.entities import Empresa, Producto, Inventario
    print("✓ Entidades de dominio importadas correctamente")
    print("\nEntidades disponibles:")
    print(f"  - {Empresa.__name__}")
    print(f"  - {Producto.__name__}")
    print(f"  - {Inventario.__name__}")
    
    # Verificar adaptadores
    try:
        from api.domain_adapters import EmpresaAdapter, ProductoAdapter, InventarioAdapter
        print("\n✓ Adaptadores importados correctamente")
    except ImportError as e:
        print(f"\n⚠ ADVERTENCIA: No se pudieron importar los adaptadores: {e}")
        print("  Esto es normal si Django no está configurado en este contexto.")
    
    print("\n" + "=" * 60)
    print("✓ CONFIGURACIÓN CORRECTA")
    print("=" * 60)
    print("\nLa capa de dominio está lista para usar.")
    print("No es necesario instalar el paquete - settings.py ya lo configura.")
    print("\nPara usar en Django, simplemente importa:")
    print("  from domain_layer.entities import Empresa, Producto, Inventario")
    
except ImportError as e:
    print(f"✗ ERROR: No se pudo importar el dominio: {e}")
    print(f"\nVerifica que la estructura del proyecto sea correcta:")
    print(f"  {domain_path}/domain_layer/entities/")
    sys.exit(1)

