# Capa de Dominio

Esta es la capa de dominio independiente del proyecto, desarrollada siguiendo principios de Arquitectura Limpia.

## Descripción

La capa de dominio contiene únicamente las entidades y reglas de negocio, sin dependencias de frameworks como Django, Flask u otros. Esta separación permite:

- Mantener la lógica de negocio desacoplada de la infraestructura
- Facilitar pruebas unitarias puras
- Permitir reutilización en diferentes contextos
- Seguir principios SOLID y Arquitectura Limpia

## Estructura

```
domain/
├── src/
│   └── domain_layer/
│       ├── __init__.py
│       └── entities/
│           ├── __init__.py
│           ├── empresa.py
│           ├── producto.py
│           └── inventario.py
├── tests/
├── pyproject.toml
└── README.md
```

## Entidades

### Empresa
Representa una empresa con validaciones de negocio para NIT, nombre, dirección y teléfono.

### Producto
Representa un producto con sus características y precios en múltiples monedas (USD, EUR, COP).

### Inventario
Representa la cantidad de un producto en el inventario de una empresa, con soporte para hash de transacciones blockchain.

## Instalación

Este paquete se gestiona con Poetry:

```bash
cd domain
poetry install
```

## Uso desde el Backend

El backend Django consume este paquete como dependencia. Ver `backend/requirements.txt` o configuración de Poetry en el backend.

## Principios Aplicados

- **Arquitectura Limpia**: Separación clara entre capas
- **Domain-Driven Design**: Entidades ricas con lógica de negocio
- **SOLID**: Cada entidad tiene responsabilidades bien definidas
- **Independencia de Frameworks**: Sin dependencias de Django u otros frameworks web

