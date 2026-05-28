"""Modelos de datos (capa de persistencia).

Importar este paquete registra todos los modelos en SQLAlchemy, necesario
antes de `db.create_all()`.
"""
from .autor import Autor
from .usuario import Usuario
from .obra import Obra
from .proyecto import Proyecto

__all__ = ['Autor', 'Usuario', 'Obra', 'Proyecto']
