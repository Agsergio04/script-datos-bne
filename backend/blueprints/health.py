import logging
from datetime import datetime
from flask import Blueprint, jsonify, request
from extensions import db
from models import Obra, Autor, Usuario, Proyecto
from services.scraper import scraper

bp = Blueprint("health", __name__)
logger = logging.getLogger(__name__)


@bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'BNE Backend API'
    }), 200


@bp.route('/api/version', methods=['GET'])
def get_version():
    """Obtener versión de la API"""
    return jsonify({
        'version': '1.0.0',
        'name': 'BNE Data Collection API',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@bp.route('/api/info', methods=['GET'])
def get_info():
    """Información del proyecto"""
    try:
        # Contar registros
        usuarios_count = Usuario.query.count()
        obras_count = Obra.query.count()
        proyectos_count = Proyecto.query.count()
        autores_count = Autor.query.count()

        return jsonify({
            'proyecto': 'Recogida de datos BNE',
            'descripcion': 'Plataforma para recopilar datos de autores y periódicos de la Biblioteca Nacional de España',
            'estadisticas': {
                'usuarios': usuarios_count,
                'obras': obras_count,
                'proyectos': proyectos_count,
                'autores': autores_count
            },
            'version': '1.0.0'
        }), 200
    except Exception as e:
        logger.error(f"Error en /api/info: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================
# RUTAS - OBRAS
# ============================================================
