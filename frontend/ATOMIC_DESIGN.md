# Estructura Atomic Design

Este proyecto sigue la metodología **Atomic Design** para organizar los componentes de React.

## Estructura de Carpetas

```
src/
├── components/
│   ├── atoms/              # Componentes básicos e indivisibles
│   │   ├── Button/
│   │   ├── Input/
│   │   ├── Label/
│   │   ├── Select/
│   │   └── Textarea/
│   │
│   ├── molecules/          # Combinaciones de átomos
│   │   └── FormField/      # Label + Input/Select/Textarea
│   │
│   └── organisms/          # Componentes complejos
│       ├── Layout/         # Header + Navigation + Main
│       └── PrivateRoute/   # Protección de rutas
│
├── pages/                  # Páginas completas (Templates)
│   ├── Login/
│   ├── Empresas/
│   ├── Productos/
│   └── Inventario/
│
├── context/                # Context API
│   └── AuthContext.js
│
└── services/               # Servicios y utilidades
    └── api.js
```

## Niveles de Atomic Design

### Atoms (Átomos)
Componentes básicos que no pueden dividirse más:
- `Button`: Botón reutilizable con variantes (primary, secondary, danger, success)
- `Input`: Campo de entrada de texto
- `Label`: Etiqueta de formulario con soporte para campos requeridos
- `Select`: Selector desplegable
- `Textarea`: Área de texto para entradas largas

### Molecules (Moléculas)
Combinaciones simples de átomos que forman una unidad funcional:
- `FormField`: Combina Label + Input/Select/Textarea para crear campos de formulario completos con validación

### Organisms (Organismos)
Componentes complejos que combinan moléculas y/o átomos:
- `Layout`: Estructura principal de la aplicación (header con navegación, contenido principal)
- `PrivateRoute`: Componente que protege rutas privadas verificando autenticación

### Templates (Páginas)
Combinaciones de organismos que forman páginas completas:
- `Login`: Página de inicio de sesión con formulario de autenticación
- `Empresas`: Página de gestión de empresas con listado, formulario y acciones CRUD
- `Productos`: Página de gestión de productos con precios en múltiples monedas
- `Inventario`: Página de gestión de inventario con tablas, PDF y envío de emails

## Ventajas de Atomic Design

1. **Reutilización**: Los componentes atómicos se reutilizan fácilmente en toda la aplicación
2. **Mantenibilidad**: Fácil encontrar y modificar componentes gracias a la estructura clara
3. **Consistencia**: Diseño uniforme en toda la aplicación mediante componentes compartidos
4. **Escalabilidad**: Fácil agregar nuevos componentes siguiendo la estructura establecida
5. **Testabilidad**: Componentes pequeños son más fáciles de testear de forma unitaria
6. **Colaboración**: Diferentes desarrolladores pueden trabajar en diferentes niveles sin conflictos

## Reglas de Uso

- Los **atoms** no deben importar otros componentes del proyecto (excepto de librerías externas)
- Las **molecules** pueden importar solo atoms
- Los **organisms** pueden importar molecules y atoms
- Las **pages** pueden importar organisms, molecules y atoms
- No crear dependencias circulares entre componentes
- Cada componente debe tener su propio archivo CSS para estilos

## Ejemplo de Flujo

```
Atom (Button) 
  ↓
Molecule (FormField usa Button, Input, Label)
  ↓
Organism (Layout usa múltiples molecules/atoms)
  ↓
Page (Empresas usa Layout y molecules directamente)
```

Esta estructura permite construir interfaces complejas a partir de componentes simples y reutilizables.

