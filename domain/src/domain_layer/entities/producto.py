"""
Entidad de dominio: Producto
Representa un producto en el sistema sin dependencias de frameworks.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class Producto:
    """
    Entidad de dominio Producto.
    Representa un producto con sus características y precios.
    """
    codigo: str
    nombre: str
    caracteristicas: str
    precio_usd: Decimal
    precio_eur: Decimal
    precio_cop: Decimal
    empresa_nit: str  # Referencia a la empresa por NIT
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    id: Optional[int] = None  # ID opcional para compatibilidad con persistencia
    
    def __post_init__(self):
        """Validaciones de negocio para la entidad Producto"""
        if not self.codigo:
            raise ValueError("El código del producto es obligatorio")
        
        if len(self.codigo) > 50:
            raise ValueError("El código no puede exceder 50 caracteres")
        
        if not self.nombre:
            raise ValueError("El nombre del producto es obligatorio")
        
        if len(self.nombre) > 200:
            raise ValueError("El nombre del producto no puede exceder 200 caracteres")
        
        if not self.caracteristicas:
            raise ValueError("Las características del producto son obligatorias")
        
        if not self.empresa_nit:
            raise ValueError("El producto debe estar asociado a una empresa")
        
        if self.precio_usd < 0:
            raise ValueError("El precio USD no puede ser negativo")
        
        if self.precio_eur < 0:
            raise ValueError("El precio EUR no puede ser negativo")
        
        if self.precio_cop < 0:
            raise ValueError("El precio COP no puede ser negativo")
    
    def __str__(self) -> str:
        return f"{self.nombre} ({self.codigo})"
    
    def actualizar_precios(self, precio_usd: Optional[Decimal] = None,
                          precio_eur: Optional[Decimal] = None,
                          precio_cop: Optional[Decimal] = None):
        """
        Actualiza los precios del producto.
        Aplica las reglas de negocio para la actualización.
        """
        if precio_usd is not None:
            if precio_usd < 0:
                raise ValueError("El precio USD no puede ser negativo")
            self.precio_usd = precio_usd
        
        if precio_eur is not None:
            if precio_eur < 0:
                raise ValueError("El precio EUR no puede ser negativo")
            self.precio_eur = precio_eur
        
        if precio_cop is not None:
            if precio_cop < 0:
                raise ValueError("El precio COP no puede ser negativo")
            self.precio_cop = precio_cop
        
        self.fecha_actualizacion = datetime.now()
    
    def actualizar_datos(self, nombre: Optional[str] = None,
                        caracteristicas: Optional[str] = None):
        """
        Actualiza los datos del producto.
        Aplica las reglas de negocio para la actualización.
        """
        if nombre is not None:
            if not nombre:
                raise ValueError("El nombre del producto no puede estar vacío")
            if len(nombre) > 200:
                raise ValueError("El nombre del producto no puede exceder 200 caracteres")
            self.nombre = nombre
        
        if caracteristicas is not None:
            if not caracteristicas:
                raise ValueError("Las características no pueden estar vacías")
            self.caracteristicas = caracteristicas
        
        self.fecha_actualizacion = datetime.now()

