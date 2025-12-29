"""
Entidad de dominio: Empresa
Representa una empresa en el sistema sin dependencias de frameworks.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Empresa:
    """
    Entidad de dominio Empresa.
    Representa una empresa con sus datos básicos.
    """
    nit: str
    nombre: str
    direccion: str
    telefono: str
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones de negocio para la entidad Empresa"""
        if not self.nit:
            raise ValueError("El NIT es obligatorio")
        
        if not (9 <= len(self.nit) <= 15):
            raise ValueError("El NIT debe contener entre 9 y 15 dígitos")
        
        if not self.nit.isdigit():
            raise ValueError("El NIT debe contener solo dígitos")
        
        if not self.nombre:
            raise ValueError("El nombre de la empresa es obligatorio")
        
        if len(self.nombre) > 200:
            raise ValueError("El nombre de la empresa no puede exceder 200 caracteres")
        
        if not self.direccion:
            raise ValueError("La dirección es obligatoria")
        
        if not self.telefono:
            raise ValueError("El teléfono es obligatorio")
        
        if len(self.telefono) > 20:
            raise ValueError("El teléfono no puede exceder 20 caracteres")
    
    def __str__(self) -> str:
        return f"{self.nombre} - {self.nit}"
    
    def actualizar_datos(self, nombre: Optional[str] = None, 
                        direccion: Optional[str] = None,
                        telefono: Optional[str] = None):
        """
        Actualiza los datos de la empresa.
        Aplica las reglas de negocio para la actualización.
        """
        if nombre is not None:
            if not nombre:
                raise ValueError("El nombre de la empresa no puede estar vacío")
            if len(nombre) > 200:
                raise ValueError("El nombre de la empresa no puede exceder 200 caracteres")
            self.nombre = nombre
        
        if direccion is not None:
            if not direccion:
                raise ValueError("La dirección no puede estar vacía")
            self.direccion = direccion
        
        if telefono is not None:
            if not telefono:
                raise ValueError("El teléfono no puede estar vacío")
            if len(telefono) > 20:
                raise ValueError("El teléfono no puede exceder 20 caracteres")
            self.telefono = telefono
        
        self.fecha_actualizacion = datetime.now()

