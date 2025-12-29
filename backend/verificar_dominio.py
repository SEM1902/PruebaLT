#!/usr/bin/env python3
"""
Script para verificar que la capa de dominio se puede importar correctamente.
Puede ejecutarse directamente sin Django.
"""

import sys
from pathlib import Path

# Agregar la ruta del dominio al PYTHONPATH
backend_dir = Path(__file__).resolve().parent
project_root = backend_dir.parent
domain_path = project_root / "domain" / "src"

if str(domain_path) not in sys.path:
    sys.path.insert(0, str(domain_path))

try:
    from domain_layer.entities import Empresa, Producto, Inventario
    print("✓ Capa de dominio importada correctamente")
    print(f"\nEntidades disponibles:")
    print(f"  - {Empresa.__name__}")
    print(f"  - {Producto.__name__}")
    print(f"  - {Inventario.__name__}")
    sys.exit(0)
except ImportError as e:
    print(f"✗ Error al importar dominio: {e}")
    print(f"\nRuta intentada: {domain_path}")
    sys.exit(1)

