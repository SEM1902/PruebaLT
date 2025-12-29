"""
Setup script para instalar el paquete de dominio.
Este archivo permite instalar el paquete con pip install -e .
"""

from setuptools import setup, find_packages

setup(
    name="domain-layer",
    version="0.1.0",
    description="Capa de dominio independiente para modelos y entidades de negocio",
    author="Sistema de Gestión",
    author_email="sistema@ejemplo.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[],
)

