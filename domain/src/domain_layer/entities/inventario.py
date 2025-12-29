"""
Entidad de dominio: Inventario
Representa un registro de inventario en el sistema sin dependencias de frameworks.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Inventario:
    """
    Entidad de dominio Inventario.
    Representa la cantidad de un producto en el inventario de una empresa.
    """
    empresa_nit: str
    producto_codigo: str
    cantidad: int
    fecha_ingreso: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    transaccion_hash: Optional[str] = None
    id: Optional[int] = None  # ID opcional para compatibilidad con persistencia
    
    def __post_init__(self):
        """Validaciones de negocio para la entidad Inventario"""
        if not self.empresa_nit:
            raise ValueError("El inventario debe estar asociado a una empresa")
        
        if not self.producto_codigo:
            raise ValueError("El inventario debe estar asociado a un producto")
        
        if self.cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
    
    def __str__(self) -> str:
        return f"Empresa: {self.empresa_nit} - Producto: {self.producto_codigo} - Cantidad: {self.cantidad}"
    
    def actualizar_cantidad(self, nueva_cantidad: int):
        """
        Actualiza la cantidad del inventario.
        Aplica las reglas de negocio para la actualización.
        """
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        
        self.cantidad = nueva_cantidad
        self.fecha_actualizacion = datetime.now()
    
    def incrementar_cantidad(self, incremento: int):
        """
        Incrementa la cantidad del inventario.
        """
        if incremento < 0:
            raise ValueError("El incremento no puede ser negativo")
        
        nueva_cantidad = self.cantidad + incremento
        self.actualizar_cantidad(nueva_cantidad)
    
    def decrementar_cantidad(self, decremento: int):
        """
        Decrementa la cantidad del inventario.
        """
        if decremento < 0:
            raise ValueError("El decremento no puede ser negativo")
        
        nueva_cantidad = self.cantidad - decremento
        if nueva_cantidad < 0:
            raise ValueError("La cantidad resultante no puede ser negativa")
        
        self.actualizar_cantidad(nueva_cantidad)
    
    def establecer_hash_transaccion(self, hash_transaccion: str):
        """
        Establece el hash de transacción blockchain.
        """
        if not hash_transaccion:
            raise ValueError("El hash de transacción no puede estar vacío")
        
        if len(hash_transaccion) > 66:
            raise ValueError("El hash de transacción no puede exceder 66 caracteres")
        
        self.transaccion_hash = hash_transaccion

