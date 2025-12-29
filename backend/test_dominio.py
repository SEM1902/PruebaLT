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
    """Prueba creación de entidades (solo en memoria, sin guardar en BD)"""
    print("\n" + "=" * 60)
    print("PRUEBA 2: Creación de Entidades (Solo en Memoria)")
    print("=" * 60)
    print("⚠️  NOTA: Estas entidades se crean solo en memoria.")
    print("    Para guardarlas en la base de datos, usa los adapters de Django.")
    print("    Ver función test_guardar_en_bd() para ejemplo de persistencia.\n")
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
        print(f"✓ Empresa creada (en memoria): {empresa}")
        print(f"  → Esta empresa NO está guardada en la base de datos")
        
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
        print(f"✓ Producto creado (en memoria): {producto}")
        print(f"  → Este producto NO está guardado en la base de datos")
        
        # Crear inventario
        inventario = Inventario(
            empresa_nit='123456789',
            producto_codigo='PROD001',
            cantidad=50
        )
        print(f"✓ Inventario creado (en memoria): {inventario}")
        print(f"  → Este inventario NO está guardado en la base de datos")
        
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

def test_guardar_en_bd():
    """
    Prueba guardar entidades de dominio en la base de datos usando adapters.
    Esta función SÍ guarda los datos y se reflejarán en la aplicación.
    """
    print("\n" + "=" * 60)
    print("PRUEBA 5: Guardar Entidades en Base de Datos")
    print("=" * 60)
    print("⚠️  Esta prueba SÍ guarda datos en la BD y se verán en la app.\n")
    
    try:
        # Configurar Django correctamente
        import os
        import sys
        from pathlib import Path
        
        # Agregar el directorio backend al path
        backend_path = Path(__file__).resolve().parent
        if str(backend_path) not in sys.path:
            sys.path.insert(0, str(backend_path))
        
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        
        try:
            import django
            django.setup()
        except ImportError:
            print("✗ Error: Django no está instalado o no está en el entorno virtual.")
            print("   Solución: Activa el entorno virtual o ejecuta:")
            print("   python manage.py shell")
            print("   Luego ejecuta manualmente la función test_guardar_en_bd()")
            return False
        
        from domain_layer.entities import Empresa, Producto, Inventario
        from decimal import Decimal
        from api.domain_adapters import EmpresaAdapter, ProductoAdapter, InventarioAdapter
        from api.models import Empresa as DjangoEmpresa, Producto as DjangoProducto, Inventario as DjangoInventario
        
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
        
        print("\n✅ Todos los datos fueron guardados en la base de datos.")
        print("   Ahora deberías poder verlos en la aplicación web.")
        
        return True
    except Exception as e:
        import traceback
        print(f"✗ Error al guardar en BD: {e}")
        print(f"\n   Detalles del error:")
        print(f"   {str(e)}")
        
        # Mensaje de ayuda
        if "No module named 'django'" in str(e) or "ModuleNotFoundError" in str(e):
            print(f"\n   💡 Solución:")
            print(f"   Para guardar datos en la BD, ejecuta uno de estos comandos:")
            print(f"   ")
            print(f"   Opción 1 (Recomendada):")
            print(f"   python manage.py shell")
            print(f"   >>> exec(open('test_dominio_bd.py').read())")
            print(f"   ")
            print(f"   Opción 2:")
            print(f"   python manage.py shell < test_dominio_bd.py")
            print(f"   ")
            print(f"   Opción 3:")
            print(f"   1. Activa el entorno virtual: source venv/bin/activate")
            print(f"   2. Ejecuta: python manage.py shell")
            print(f"   3. Luego: from test_dominio import test_guardar_en_bd; test_guardar_en_bd()")
        else:
            print(f"\n   Traceback completo:")
            traceback.print_exc()
        
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
    
    # Preguntar si quiere guardar en BD (opcional)
    print("\n" + "=" * 60)
    print("PRUEBA OPCIONAL: Guardar en Base de Datos")
    print("=" * 60)
    print("¿Deseas ejecutar la prueba que guarda datos en la BD?")
    print("(Esto creará una empresa, producto e inventario que se verán en la app)")
    respuesta = input("Escribe 'si' para ejecutar, o Enter para omitir: ").strip().lower()
    
    if respuesta in ['si', 'sí', 'yes', 'y']:
        resultados.append(("Guardar en BD", test_guardar_en_bd()))
    else:
        print("Prueba de guardado en BD omitida.")
        print("💡 Para guardar datos en la BD, ejecuta: test_guardar_en_bd()")
    
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

