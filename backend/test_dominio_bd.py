#!/usr/bin/env python
"""
Script para probar guardar entidades de dominio en la base de datos.
Este script DEBE ejecutarse usando Django management command.

Ejecutar:
    python manage.py shell < test_dominio_bd.py
    O mejor:
    python manage.py shell
    >>> exec(open('test_dominio_bd.py').read())
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from domain_layer.entities import Empresa, Producto, Inventario
from decimal import Decimal
from api.domain_adapters import EmpresaAdapter, ProductoAdapter, InventarioAdapter

def guardar_datos_prueba():
    """
    Guarda una empresa, producto e inventario de prueba en la base de datos.
    Estos datos SÍ se verán en la aplicación web.
    """
    print("=" * 60)
    print("GUARDANDO DATOS DE PRUEBA EN LA BASE DE DATOS")
    print("=" * 60)
    print()
    
    try:
        # Crear empresa de dominio
        empresa_domain = Empresa(
            nit='999888777',
            nombre='Empresa de Prueba BD',
            direccion='Calle Test #123',
            telefono='3001112233'
        )
        print(f"✓ Empresa de dominio creada: {empresa_domain}")
        
        # Convertir y guardar en BD usando adapter
        django_empresa = EmpresaAdapter.to_django(empresa_domain)
        django_empresa.save()
        print(f"✓ Empresa guardada en BD: {django_empresa.nombre} (NIT: {django_empresa.nit})")
        
        # Crear producto de dominio
        producto_domain = Producto(
            codigo='PROD-BD-001',
            nombre='Producto de Prueba BD',
            caracteristicas='Producto creado desde test de dominio',
            precio_usd=Decimal('150.00'),
            precio_eur=Decimal('138.00'),
            precio_cop=Decimal('600000.00'),
            empresa_nit='999888777'
        )
        print(f"✓ Producto de dominio creado: {producto_domain}")
        
        # Convertir y guardar en BD usando adapter
        django_producto = ProductoAdapter.to_django(producto_domain, django_empresa)
        django_producto.save()
        print(f"✓ Producto guardado en BD: {django_producto.nombre} (Código: {django_producto.codigo})")
        
        # Crear inventario de dominio
        inventario_domain = Inventario(
            empresa_nit='999888777',
            producto_codigo='PROD-BD-001',
            cantidad=75
        )
        print(f"✓ Inventario de dominio creado: {inventario_domain}")
        
        # Convertir y guardar en BD usando adapter
        django_inventario = InventarioAdapter.to_django(inventario_domain, django_empresa, django_producto)
        django_inventario.save()
        print(f"✓ Inventario guardado en BD: {django_inventario.cantidad} unidades")
        
        print()
        print("=" * 60)
        print("✅ TODOS LOS DATOS FUERON GUARDADOS EXITOSAMENTE")
        print("=" * 60)
        print()
        print("Ahora puedes ver estos datos en la aplicación web:")
        print(f"  - Empresa: {django_empresa.nombre}")
        print(f"  - Producto: {django_producto.nombre}")
        print(f"  - Inventario: {django_inventario.cantidad} unidades")
        print()
        
        return True
        
    except Exception as e:
        import traceback
        print(f"✗ Error al guardar en BD: {e}")
        print()
        print("Detalles del error:")
        traceback.print_exc()
        return False

# Ejecutar automáticamente cuando se ejecuta el script
# Funciona tanto con exec() como con ejecución directa
guardar_datos_prueba()

