"""Punto de entrada de la API BNE — patrón Application Factory.

Responsabilidad única: crear y configurar la app, enlazar extensiones y
registrar los blueprints (cada uno con su propia responsabilidad). La lógica
vive en:
  - config.py        -> configuración
  - extensions.py    -> instancias de extensiones (db)
  - models/          -> modelos de datos
  - services/        -> lógica externa (scraper)
  - blueprints/      -> rutas HTTP agrupadas por recurso
"""
import os
import logging

from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from extensions import db
import models  # noqa: F401  (registra los modelos en SQLAlchemy)

from blueprints.health import bp as health_bp
from blueprints.obras import bp as obras_bp
from blueprints.estadisticas import bp as estadisticas_bp
from blueprints.importar import bp as importar_bp
from blueprints.autores import bp as autores_bp
from blueprints.datasets import bp as datasets_bp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BLUEPRINTS = (health_bp, obras_bp, estadisticas_bp, importar_bp, autores_bp, datasets_bp)


def create_app(config_class=Config):
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.json.sort_keys = False  # conserva el orden de inserción en las respuestas

    db.init_app(app)
    CORS(app)

    for bp in BLUEPRINTS:
        app.register_blueprint(bp)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint no encontrado'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Error interno del servidor'}), 500

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            logger.warning(f"No se pudo ejecutar create_all al iniciar: {e}")

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_ENV') == 'development', host='0.0.0.0', port=5000)
