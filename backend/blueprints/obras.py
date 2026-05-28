import logging
from datetime import datetime
from flask import Blueprint, jsonify, request
from extensions import db
from models import Obra, Autor, Usuario, Proyecto
from services.scraper import scraper

bp = Blueprint("obras", __name__)
logger = logging.getLogger(__name__)


@bp.route('/api/obras', methods=['GET'])
def get_obras():
    """Obtener todas las obras con paginación y filtros"""
    try:
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Filtros
        tipo = request.args.get('tipo')
        autor = request.args.get('autor')
        tema = request.args.get('tema')
        anio = request.args.get('anio', type=int)
        fecha_desde = request.args.get('fecha_desde', type=str)
        fecha_hasta = request.args.get('fecha_hasta', type=str)
        
        query = Obra.query
        
        if tipo:
            query = query.filter_by(tipo_publicacion=tipo)
        if autor:
            query = query.filter(Obra.nombre_autor.ilike(f'%{autor}%'))
        if tema:
            query = query.filter(Obra.tema_principal.ilike(f'%{tema}%'))
        if anio:
            query = query.filter_by(anio=anio)
        
        # Filtro por rango de fechas
        if fecha_desde:
            try:
                from datetime import datetime
                fecha_desde_obj = datetime.fromisoformat(fecha_desde).date()
                query = query.filter(Obra.fecha >= fecha_desde_obj)
            except:
                pass
        
        if fecha_hasta:
            try:
                from datetime import datetime
                fecha_hasta_obj = datetime.fromisoformat(fecha_hasta).date()
                query = query.filter(Obra.fecha <= fecha_hasta_obj)
            except:
                pass
        
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'data': [obra.to_dict() for obra in paginated.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'pages': paginated.pages
            }
        }), 200
    except Exception as e:
        logger.error(f"Error en GET /api/obras: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/api/obras/<int:obra_id>', methods=['GET'])
def get_obra(obra_id):
    """Obtener obra específica"""
    try:
        obra = Obra.query.get(obra_id)
        if not obra:
            return jsonify({'error': 'Obra no encontrada'}), 404
        return jsonify(obra.to_dict()), 200
    except Exception as e:
        logger.error(f"Error en GET /api/obras/{obra_id}: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/api/obras/<int:obra_id>/detallada', methods=['GET'])
def get_obra_detallada(obra_id):
    """Obtener obra con información completa y especializada"""
    try:
        obra = Obra.query.get(obra_id)
        if not obra:
            return jsonify({'error': 'Obra no encontrada'}), 404
        return jsonify(obra.to_dict_detallado()), 200
    except Exception as e:
        logger.error(f"Error en GET /api/obras/{obra_id}/detallada: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/api/obras', methods=['POST'])
def create_obra():
    """Crear nueva obra"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not data.get('titulo'):
            return jsonify({'error': 'Título es requerido'}), 400
        
        nueva_obra = Obra(
            titulo=data['titulo'],
            tipo_publicacion=data.get('tipo_publicacion'),
            autor_firma=data.get('autor_firma'),
            nombre_autor=data.get('nombre_autor'),
            anio=data.get('anio'),
            enlace=data.get('enlace'),
            tema_principal=data.get('tema_principal'),
            paginas=data.get('paginas'),
            como_citar=data.get('como_citar'),
            imagen_url=data.get('imagen_url')
        )

        db.session.add(nueva_obra)
        db.session.commit()

        logger.info(f"Obra creada: {nueva_obra.id_obra}")
        return jsonify({
            'message': 'Obra creada exitosamente',
            'data': nueva_obra.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error en POST /api/obras: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/api/obras/<int:obra_id>', methods=['PUT'])
def update_obra(obra_id):
    """Actualizar obra"""
    try:
        obra = Obra.query.get(obra_id)
        if not obra:
            return jsonify({'error': 'Obra no encontrada'}), 404
        
        data = request.get_json()
        
        # Actualizar campos
        for key, value in data.items():
            if hasattr(obra, key):
                setattr(obra, key, value)
        
        obra.actualizado_en = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Obra actualizada: {obra_id}")
        return jsonify({
            'message': 'Obra actualizada exitosamente',
            'data': obra.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error en PUT /api/obras/{obra_id}: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/api/obras/<int:obra_id>', methods=['DELETE'])
def delete_obra(obra_id):
    """Eliminar obra"""
    try:
        obra = Obra.query.get(obra_id)
        if not obra:
            return jsonify({'error': 'Obra no encontrada'}), 404
        
        db.session.delete(obra)
        db.session.commit()
        
        logger.info(f"Obra eliminada: {obra_id}")
        return jsonify({'message': 'Obra eliminada exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error en DELETE /api/obras/{obra_id}: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/api/periodicos/rango-fechas', methods=['GET'])
def get_periodicos_rango_fechas():
    """
    Obtener periódicos BIMO en un rango de fechas
    Parámetros:
    - fecha_desde: YYYY-MM-DD
    - fecha_hasta: YYYY-MM-DD
    - page: número de página (default 1)
    - per_page: resultados por página (default 20)
    """
    try:
        fecha_desde = request.args.get('fecha_desde', type=str)
        fecha_hasta = request.args.get('fecha_hasta', type=str)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        if not fecha_desde or not fecha_hasta:
            return jsonify({'error': 'Los parámetros fecha_desde y fecha_hasta son obligatorios'}), 400
        
        try:
            from datetime import datetime
            fecha_desde_obj = datetime.fromisoformat(fecha_desde).date()
            fecha_hasta_obj = datetime.fromisoformat(fecha_hasta).date()
            
            # Validar que las fechas sean razonables (1500-2100)
            if fecha_desde_obj.year < 1500 or fecha_desde_obj.year > 2100:
                return jsonify({'error': f'Año inválido en fecha_desde: {fecha_desde_obj.year}. Use rango 1500-2100'}), 400
            
            if fecha_hasta_obj.year < 1500 or fecha_hasta_obj.year > 2100:
                return jsonify({'error': f'Año inválido en fecha_hasta: {fecha_hasta_obj.year}. Use rango 1500-2100'}), 400
                
            # Validar que fecha_desde <= fecha_hasta
            if fecha_desde_obj > fecha_hasta_obj:
                return jsonify({'error': 'fecha_desde debe ser anterior a fecha_hasta'}), 400
                
        except ValueError as ve:
            return jsonify({'error': f'Formato de fecha inválido. Use YYYY-MM-DD. Detalle: {str(ve)}'}), 400
        
        # Buscar periódicos BIMO (tipo_publicacion contiene "periódico")
        query = Obra.query.filter(
            Obra.fecha >= fecha_desde_obj,
            Obra.fecha <= fecha_hasta_obj,
            (Obra.tipo_publicacion.ilike('%periódico%')) | (Obra.tipo_publicacion.ilike('%prensa%'))
        ).order_by(Obra.fecha.desc(), Obra.titulo.asc())
        
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'data': [obra.to_dict() for obra in paginated.items],
            'rango_fechas': {
                'desde': fecha_desde,
                'hasta': fecha_hasta
            },
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'pages': paginated.pages
            }
        }), 200
    except Exception as e:
        logger.error(f"Error en GET /api/periodicos/rango-fechas: {e}")
        return jsonify({'error': str(e)}), 500
