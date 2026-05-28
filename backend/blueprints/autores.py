import logging
from datetime import datetime
from flask import Blueprint, jsonify, request
from extensions import db
from models import Obra, Autor, Usuario, Proyecto
from services.scraper import scraper

bp = Blueprint("autores", __name__)
logger = logging.getLogger(__name__)


@bp.route('/api/autores', methods=['GET'])
def get_autores():
    """Listar autores con paginación y filtros opcionales"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        nombre = request.args.get('nombre')
        nacionalidad = request.args.get('nacionalidad')
        ocupacion = request.args.get('ocupacion')

        query = Autor.query

        if nombre:
            query = query.filter(Autor.nombre_completo.ilike(f'%{nombre}%'))
        if nacionalidad:
            query = query.filter(Autor.nacionalidad.ilike(f'%{nacionalidad}%'))
        if ocupacion:
            query = query.filter(Autor.ocupacion.ilike(f'%{ocupacion}%'))

        paginated = query.order_by(Autor.nombre_completo).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            'data': [a.to_dict() for a in paginated.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'pages': paginated.pages
            }
        }), 200
    except Exception as e:
        logger.error(f"Error en GET /api/autores: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/api/autores/<int:autor_id>', methods=['GET'])
def get_autor(autor_id):
    """Obtener un autor por id, incluyendo sus obras"""
    try:
        autor = Autor.query.get(autor_id)
        if not autor:
            return jsonify({'error': 'Autor no encontrado'}), 404

        datos = autor.to_dict()
        obras = Obra.query.filter_by(id_autor=autor_id).all()
        datos['obras'] = [{'id': o.id_obra, 'titulo': o.titulo, 'anio': o.anio,
                           'tipo_publicacion': o.tipo_publicacion} for o in obras]
        return jsonify(datos), 200
    except Exception as e:
        logger.error(f"Error en GET /api/autores/{autor_id}: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/api/autores', methods=['POST'])
def create_autor():
    """Crear un autor manualmente"""
    try:
        data = request.get_json()
        if not data or not data.get('nombre_completo'):
            return jsonify({'error': 'nombre_completo es obligatorio'}), 400

        # Evitar duplicados por identificador BNE
        bne_id = data.get('bne_identificador')
        if bne_id and Autor.query.filter_by(bne_identificador=bne_id).first():
            return jsonify({'error': f'Ya existe un autor con bne_identificador {bne_id}'}), 409

        autor = Autor(
            nombre_completo=data['nombre_completo'].strip(),
            nombre_firma=data.get('nombre_firma'),
            pseudonimos=data.get('pseudonimos'),
            fecha_nacimiento=data.get('fecha_nacimiento'),
            anio_nacimiento=data.get('anio_nacimiento'),
            lugar_nacimiento=data.get('lugar_nacimiento'),
            fecha_muerte=data.get('fecha_muerte'),
            anio_muerte=data.get('anio_muerte'),
            lugar_muerte=data.get('lugar_muerte'),
            nacionalidad=data.get('nacionalidad'),
            ocupacion=data.get('ocupacion'),
            genero=data.get('genero'),
            lengua=data.get('lengua'),
            biografia=data.get('biografia'),
            bne_identificador=bne_id,
            url_datos_bne=data.get('url_datos_bne'),
            viaf_id=data.get('viaf_id'),
            otros_identificadores=data.get('otros_identificadores'),
            imagen_url=data.get('imagen_url')
        )
        db.session.add(autor)
        db.session.commit()
        return jsonify(autor.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error en POST /api/autores: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/api/autores/<int:autor_id>', methods=['PUT'])
def update_autor(autor_id):
    """Actualizar datos de un autor"""
    try:
        autor = Autor.query.get(autor_id)
        if not autor:
            return jsonify({'error': 'Autor no encontrado'}), 404

        data = request.get_json()
        campos = [
            'nombre_completo', 'nombre_firma', 'pseudonimos',
            'fecha_nacimiento', 'anio_nacimiento', 'lugar_nacimiento',
            'fecha_muerte', 'anio_muerte', 'lugar_muerte',
            'nacionalidad', 'ocupacion', 'genero', 'lengua',
            'biografia', 'bne_identificador', 'url_datos_bne',
            'viaf_id', 'otros_identificadores', 'imagen_url'
        ]
        for campo in campos:
            if campo in data:
                setattr(autor, campo, data[campo])

        db.session.commit()
        return jsonify(autor.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error en PUT /api/autores/{autor_id}: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/api/autores/<int:autor_id>', methods=['DELETE'])
def delete_autor(autor_id):
    """Eliminar un autor (las obras quedan con id_autor = NULL)"""
    try:
        autor = Autor.query.get(autor_id)
        if not autor:
            return jsonify({'error': 'Autor no encontrado'}), 404

        db.session.delete(autor)
        db.session.commit()
        return jsonify({'message': f'Autor {autor_id} eliminado'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error en DELETE /api/autores/{autor_id}: {e}")
        return jsonify({'error': str(e)}), 500

