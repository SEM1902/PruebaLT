"""
Adaptadores para mapear entre entidades de dominio y modelos Django.
Estos adaptadores permiten que el backend use las entidades de dominio
mientras mantiene la compatibilidad con Django ORM.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from domain_layer.entities import Empresa as DomainEmpresa, Producto as DomainProducto, Inventario as DomainInventario
from .models import Empresa as DjangoEmpresa, Producto as DjangoProducto, Inventario as DjangoInventario


class EmpresaAdapter:
    """Adaptador para convertir entre entidad de dominio Empresa y modelo Django"""
    
    @staticmethod
    def to_domain(django_empresa: DjangoEmpresa) -> DomainEmpresa:
        """Convierte un modelo Django a entidad de dominio"""
        return DomainEmpresa(
            nit=django_empresa.nit,
            nombre=django_empresa.nombre,
            direccion=django_empresa.direccion,
            telefono=django_empresa.telefono,
            fecha_creacion=django_empresa.fecha_creacion,
            fecha_actualizacion=django_empresa.fecha_actualizacion
        )
    
    @staticmethod
    def to_django(domain_empresa: DomainEmpresa) -> DjangoEmpresa:
        """Convierte una entidad de dominio a modelo Django"""
        try:
            django_empresa = DjangoEmpresa.objects.get(nit=domain_empresa.nit)
            # Actualizar campos
            django_empresa.nombre = domain_empresa.nombre
            django_empresa.direccion = domain_empresa.direccion
            django_empresa.telefono = domain_empresa.telefono
            if domain_empresa.fecha_actualizacion:
                django_empresa.fecha_actualizacion = domain_empresa.fecha_actualizacion
        except DjangoEmpresa.DoesNotExist:
            # Crear nuevo
            django_empresa = DjangoEmpresa(
                nit=domain_empresa.nit,
                nombre=domain_empresa.nombre,
                direccion=domain_empresa.direccion,
                telefono=domain_empresa.telefono
            )
            if domain_empresa.fecha_creacion:
                django_empresa.fecha_creacion = domain_empresa.fecha_creacion
        
        return django_empresa
    
    @staticmethod
    def from_dict(data: dict) -> DomainEmpresa:
        """Crea una entidad de dominio desde un diccionario"""
        return DomainEmpresa(
            nit=data['nit'],
            nombre=data['nombre'],
            direccion=data['direccion'],
            telefono=data['telefono'],
            fecha_creacion=data.get('fecha_creacion'),
            fecha_actualizacion=data.get('fecha_actualizacion')
        )


class ProductoAdapter:
    """Adaptador para convertir entre entidad de dominio Producto y modelo Django"""
    
    @staticmethod
    def to_domain(django_producto: DjangoProducto) -> DomainProducto:
        """Convierte un modelo Django a entidad de dominio"""
        return DomainProducto(
            id=django_producto.id,
            codigo=django_producto.codigo,
            nombre=django_producto.nombre,
            caracteristicas=django_producto.caracteristicas,
            precio_usd=Decimal(str(django_producto.precio_usd)),
            precio_eur=Decimal(str(django_producto.precio_eur)),
            precio_cop=Decimal(str(django_producto.precio_cop)),
            empresa_nit=django_producto.empresa.nit,
            fecha_creacion=django_producto.fecha_creacion,
            fecha_actualizacion=django_producto.fecha_actualizacion
        )
    
    @staticmethod
    def to_django(domain_producto: DomainProducto, django_empresa: DjangoEmpresa) -> DjangoProducto:
        """Convierte una entidad de dominio a modelo Django"""
        try:
            django_producto = DjangoProducto.objects.get(codigo=domain_producto.codigo)
            # Actualizar campos
            django_producto.nombre = domain_producto.nombre
            django_producto.caracteristicas = domain_producto.caracteristicas
            django_producto.precio_usd = float(domain_producto.precio_usd)
            django_producto.precio_eur = float(domain_producto.precio_eur)
            django_producto.precio_cop = float(domain_producto.precio_cop)
            django_producto.empresa = django_empresa
            if domain_producto.fecha_actualizacion:
                django_producto.fecha_actualizacion = domain_producto.fecha_actualizacion
        except DjangoProducto.DoesNotExist:
            # Crear nuevo
            django_producto = DjangoProducto(
                codigo=domain_producto.codigo,
                nombre=domain_producto.nombre,
                caracteristicas=domain_producto.caracteristicas,
                precio_usd=float(domain_producto.precio_usd),
                precio_eur=float(domain_producto.precio_eur),
                precio_cop=float(domain_producto.precio_cop),
                empresa=django_empresa
            )
            if domain_producto.fecha_creacion:
                django_producto.fecha_creacion = domain_producto.fecha_creacion
        
        return django_producto
    
    @staticmethod
    def from_dict(data: dict) -> DomainProducto:
        """Crea una entidad de dominio desde un diccionario"""
        return DomainProducto(
            codigo=data['codigo'],
            nombre=data['nombre'],
            caracteristicas=data['caracteristicas'],
            precio_usd=Decimal(str(data['precio_usd'])),
            precio_eur=Decimal(str(data.get('precio_eur', 0))),
            precio_cop=Decimal(str(data.get('precio_cop', 0))),
            empresa_nit=data['empresa'],
            fecha_creacion=data.get('fecha_creacion'),
            fecha_actualizacion=data.get('fecha_actualizacion')
        )


class InventarioAdapter:
    """Adaptador para convertir entre entidad de dominio Inventario y modelo Django"""
    
    @staticmethod
    def to_domain(django_inventario: DjangoInventario) -> DomainInventario:
        """Convierte un modelo Django a entidad de dominio"""
        return DomainInventario(
            id=django_inventario.id,
            empresa_nit=django_inventario.empresa.nit,
            producto_codigo=django_inventario.producto.codigo,
            cantidad=django_inventario.cantidad,
            fecha_ingreso=django_inventario.fecha_ingreso,
            fecha_actualizacion=django_inventario.fecha_actualizacion,
            transaccion_hash=django_inventario.transaccion_hash
        )
    
    @staticmethod
    def to_django(domain_inventario: DomainInventario, 
                 django_empresa: DjangoEmpresa, 
                 django_producto: DjangoProducto) -> DjangoInventario:
        """Convierte una entidad de dominio a modelo Django"""
        try:
            django_inventario = DjangoInventario.objects.get(
                empresa=django_empresa,
                producto=django_producto
            )
            # Actualizar campos
            django_inventario.cantidad = domain_inventario.cantidad
            if domain_inventario.transaccion_hash:
                django_inventario.transaccion_hash = domain_inventario.transaccion_hash
            if domain_inventario.fecha_actualizacion:
                django_inventario.fecha_actualizacion = domain_inventario.fecha_actualizacion
        except DjangoInventario.DoesNotExist:
            # Crear nuevo
            django_inventario = DjangoInventario(
                empresa=django_empresa,
                producto=django_producto,
                cantidad=domain_inventario.cantidad,
                transaccion_hash=domain_inventario.transaccion_hash
            )
            if domain_inventario.fecha_ingreso:
                django_inventario.fecha_ingreso = domain_inventario.fecha_ingreso
        
        return django_inventario
    
    @staticmethod
    def from_dict(data: dict, producto_codigo: Optional[str] = None) -> DomainInventario:
        """
        Crea una entidad de dominio desde un diccionario.
        Si se proporciona producto_codigo, se usa ese; de lo contrario, se espera en data.
        """
        # Si se pasa el ID del producto, necesitamos obtener el código
        if 'producto' in data:
            if isinstance(data['producto'], int):
                # Es un ID, obtener el código del producto
                from .models import Producto
                try:
                    producto = Producto.objects.get(id=data['producto'])
                    producto_codigo = producto.codigo
                except Producto.DoesNotExist:
                    raise ValueError(f"Producto con ID {data['producto']} no encontrado")
            else:
                # Es el código directamente o un objeto Producto
                producto_codigo = str(data['producto'])
        elif producto_codigo:
            # Ya se proporcionó el código como parámetro
            pass
        else:
            raise ValueError("Se debe proporcionar el producto (ID o código)")
        
        # Si se pasa el NIT de la empresa como string, usarlo directamente
        empresa_nit = data.get('empresa')
        if empresa_nit:
            if isinstance(empresa_nit, int):
                # Si es un ID numérico, asumir que es el NIT como string
                empresa_nit = str(empresa_nit)
            else:
                # Es el NIT como string o un objeto Empresa
                empresa_nit = str(empresa_nit)
        else:
            raise ValueError("Se debe proporcionar la empresa (NIT)")
        
        return DomainInventario(
            empresa_nit=empresa_nit,
            producto_codigo=producto_codigo,
            cantidad=data['cantidad'],
            fecha_ingreso=data.get('fecha_ingreso'),
            fecha_actualizacion=data.get('fecha_actualizacion'),
            transaccion_hash=data.get('transaccion_hash')
        )

