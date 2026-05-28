import logging
from datetime import datetime
from flask import Blueprint, jsonify, request
from extensions import db
from models import Obra, Autor, Usuario, Proyecto
from services.scraper import scraper

bp = Blueprint("estadisticas", __name__)
logger = logging.getLogger(__name__)


@bp.route('/api/estadisticas/resumen', methods=['GET'])
def get_estadisticas():
    """Obtener estadísticas generales"""
    try:
        # Usar raw SQL para vistas
        from sqlalchemy import text
        
        obras_por_tipo = db.session.execute(
            text("SELECT COUNT(*) as total, tipo_publicacion FROM obra GROUP BY tipo_publicacion")
        ).fetchall()
        
        obras_por_autor = db.session.execute(
            text("""
            SELECT nombre_autor, COUNT(*) as total FROM obra
            WHERE nombre_autor IS NOT NULL
            GROUP BY nombre_autor ORDER BY total DESC LIMIT 10
            """)
        ).fetchall()

        total_obras = db.session.execute(text("SELECT COUNT(*) FROM obra")).scalar()

        # El frontend lee bajo la clave "resumen" y espera nombre_autor/tipo/total
        return jsonify({
            'resumen': {
                'total_obras': total_obras,
                'autores_principales': [
                    {'nombre_autor': row[0], 'total': row[1]} for row in obras_por_autor
                ],
                'obras_por_tipo': [
                    {'tipo': row[1], 'total': row[0]} for row in obras_por_tipo
                ],
            }
        }), 200
    except Exception as e:
        logger.error(f"Error en GET /api/estadisticas/resumen: {e}")
        return jsonify({'error': str(e)}), 500
@bp.route('/api/buscar', methods=['GET'])
def search():
    """Búsqueda global optimizada - devuelve información completa"""
    try:
        q = request.args.get('q', '')
        detallada = request.args.get('detallada', 'false').lower() == 'true'
        limite = request.args.get('limite', 50, type=int)
        
        if not q or len(q) < 3:
            return jsonify({'error': 'Búsqueda debe tener al menos 3 caracteres'}), 400
        
        # Búsqueda más completa en múltiples campos
        resultados = Obra.query.filter(
            (Obra.titulo.ilike(f'%{q}%')) |
            (Obra.nombre_autor.ilike(f'%{q}%')) |
            (Obra.autor_firma.ilike(f'%{q}%')) |
            (Obra.tema_principal.ilike(f'%{q}%')) |
            (Obra.variante_titulo.ilike(f'%{q}%')) |
            (Obra.pseudonimos_autor.ilike(f'%{q}%')) |
            (Obra.imprenta.ilike(f'%{q}%'))
        ).order_by(Obra.anio.desc(), Obra.titulo.asc()).limit(limite).all()
        
        # Devolver información detallada si se solicita
        if detallada:
            obras_data = [obra.to_dict_detallado() for obra in resultados]
        else:
            obras_data = [obra.to_dict() for obra in resultados]
        
        # Agrupar por tipo para mejor visualización
        tipos = {}
        for obra in resultados:
            tipo = obra.tipo_publicacion or 'Desconocido'
            if tipo not in tipos:
                tipos[tipo] = 0
            tipos[tipo] += 1
        
        return jsonify({
            'query': q,
            'total_resultados': len(resultados),
            'tipos_encontrados': tipos,
            'resultados': obras_data
        }), 200
    except Exception as e:
        logger.error(f"Error en GET /api/buscar: {e}")
        return jsonify({'error': str(e)}), 500
