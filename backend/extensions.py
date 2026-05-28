"""Extensiones de Flask compartidas (patrón factory).

Se instancian aquí sin app para evitar imports circulares; se enlazan a la
aplicación en `create_app()` mediante `db.init_app(app)`.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
