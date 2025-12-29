#!/usr/bin/env python3
"""
Script de prueba rápida de la capa de dominio
Ejecutar: python3 test_dominio.py
"""

import sys
from pathlib import Path

# Agregar ruta del dominio
domain_path = Path(__file__).resolve().parent.parent / "domain" / "src"
if str(domain_path) not in sys.path:
    sys.path.insert(0, str(domain_path))

def test_imports():
    """Prueba que las importaciones funcionen"""
    print("=" * 60)
    print("PRUEBA 1: Importaciones")
    print("=" * 60)
    try:
        from domain_layer.entities import Empresa, Producto, Inventario
        print("✓ Entidades importadas correctamente")
        print(f"  - {Empresa.__name__}")
        print(f"  - {Producto.__name__}")
        print(f"  - {Inventario.__name__}")
        return True
    except ImportError as e:
        print(f"✗ Error al importar: {e}")
        return False

def test_creacion_entidades():
    """Prueba creación de entidades"""
    print("\n" + "=" * 60)
    print("PRUEBA 2: Creación de Entidades")
    print("=" * 60)
    try:
        from domain_layer.entities import Empresa, Producto, Inventario
        from decimal import Decimal
        
        # Crear empresa
        empresa = Empresa(
            nit='123456789',
            nombre='Empresa Test',
            direccion='Calle 123 #45-67',
            telefono='3001234567'
        )
        print(f"✓ Empresa creada: {empresa}")
        
        # Crear producto
        producto = Producto(
            codigo='PROD001',
            nombre='Producto Test',
            caracteristicas='Características del producto',
            precio_usd=Decimal('100.00'),
            precio_eur=Decimal('92.00'),
            precio_cop=Decimal('400000.00'),
            empresa_nit='123456789'
        )
        print(f"✓ Producto creado: {producto}")
        
        # Crear inventario
        inventario = Inventario(
            empresa_nit='123456789',
            producto_codigo='PROD001',
            cantidad=50
        )
        print(f"✓ Inventario creado: {inventario}")
        
        return True
    except Exception as e:
        print(f"✗ Error al crear entidades: {e}")
        return False

def test_validaciones():
    """Prueba validaciones de negocio"""
    print("\n" + "=" * 60)
    print("PRUEBA 3: Validaciones de Negocio")
    print("=" * 60)
    try:
        from domain_layer.entities import Empresa, Producto, Inventario
        from decimal import Decimal
        
        # Test 1: NIT inválido (muy corto)
        try:
            empresa = Empresa(nit='123', nombre='Test', direccion='Test', telefono='123')
            print("✗ ERROR: Debería fallar con NIT corto")
            return False
        except ValueError as e:
            print(f"✓ Validación NIT funciona: {str(e)[:50]}...")
        
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
            return False
        except ValueError as e:
            print(f"✓ Validación precio funciona: {str(e)[:50]}...")
        
        # Test 3: Cantidad negativa
        try:
            inventario = Inventario(
                empresa_nit='123456789',
                producto_codigo='TEST',
                cantidad=-5
            )
            print("✗ ERROR: Debería fallar con cantidad negativa")
            return False
        except ValueError as e:
            print(f"✓ Validación cantidad funciona: {str(e)[:50]}...")
        
        return True
    except Exception as e:
        print(f"✗ Error en validaciones: {e}")
        return False

def test_metodos_negocio():
    """Prueba métodos de negocio"""
    print("\n" + "=" * 60)
    print("PRUEBA 4: Métodos de Negocio")
    print("=" * 60)
    try:
        from domain_layer.entities import Empresa, Producto, Inventario
        from decimal import Decimal
        
        # Test actualizar_datos de Empresa
        empresa = Empresa(
            nit='987654321',
            nombre='Empresa Original',
            direccion='Dirección Original',
            telefono='3009876543'
        )
        empresa.actualizar_datos(nombre='Empresa Actualizada')
        print(f"✓ Empresa.actualizar_datos() funciona: {empresa.nombre}")
        
        # Test actualizar_precios de Producto
        producto = Producto(
            codigo='PROD002',
            nombre='Producto Test',
            caracteristicas='Test',
            precio_usd=Decimal('50.00'),
            precio_eur=Decimal('46.00'),
            precio_cop=Decimal('200000.00'),
            empresa_nit='987654321'
        )
        producto.actualizar_precios(precio_usd=Decimal('75.00'))
        print(f"✓ Producto.actualizar_precios() funciona: ${producto.precio_usd}")
        
        # Test actualizar_cantidad de Inventario
        inventario = Inventario(
            empresa_nit='987654321',
            producto_codigo='PROD002',
            cantidad=100
        )
        inventario.actualizar_cantidad(150)
        print(f"✓ Inventario.actualizar_cantidad() funciona: {inventario.cantidad}")
        
        return True
    except Exception as e:
        print(f"✗ Error en métodos de negocio: {e}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "=" * 60)
    print("PRUEBAS DE CAPA DE DOMINIO")
    print("=" * 60 + "\n")
    
    resultados = []
    
    resultados.append(("Importaciones", test_imports()))
    resultados.append(("Creación de Entidades", test_creacion_entidades()))
    resultados.append(("Validaciones", test_validaciones()))
    resultados.append(("Métodos de Negocio", test_metodos_negocio()))
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    total = len(resultados)
    exitosas = sum(1 for _, resultado in resultados if resultado)
    
    for nombre, resultado in resultados:
        estado = "✓ PASÓ" if resultado else "✗ FALLÓ"
        print(f"{estado}: {nombre}")
    
    print(f"\nTotal: {exitosas}/{total} pruebas exitosas")
    
    if exitosas == total:
        print("\n✅ TODAS LAS PRUEBAS PASARON")
        print("La capa de dominio está funcionando correctamente.")
        return 0
    else:
        print("\n⚠️ ALGUNAS PRUEBAS FALLARON")
        return 1

if __name__ == "__main__":
    sys.exit(main())

