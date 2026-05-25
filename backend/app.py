"""
Aplicación Flask para el proyecto BNE
API REST para gestionar obras, autores y periódicos
Incluye integración con scraper de datos.bne.es
"""

import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging
from bne_scraper import BNEScraper

# Configuración
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql+psycopg2://bne_user:bne_password_123@localhost:5432/bne_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# Inicializar extensiones
db = SQLAlchemy(app)
CORS(app)

# Inicializar scraper (verify_ssl=False para resolver problemas con certificados en Windows)
scraper = BNEScraper(verify_ssl=False)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# MODELOS
# ============================================================

class Autor(db.Model):
    __tablename__ = 'autor'

    id_autor = db.Column(db.BigInteger, primary_key=True)
    nombre_completo = db.Column(db.String(255), nullable=False)
    nombre_firma = db.Column(db.String(255))
    pseudonimos = db.Column(db.Text)
    fecha_nacimiento = db.Column(db.String(100))
    anio_nacimiento = db.Column(db.Integer)
    lugar_nacimiento = db.Column(db.String(255))
    fecha_muerte = db.Column(db.String(100))
    anio_muerte = db.Column(db.Integer)
    lugar_muerte = db.Column(db.String(255))
    nacionalidad = db.Column(db.String(100))
    ocupacion = db.Column(db.String(255))
    genero = db.Column(db.String(50))
    lengua = db.Column(db.String(100))
    biografia = db.Column(db.Text)
    bne_identificador = db.Column(db.String(100), unique=True)
    url_datos_bne = db.Column(db.Text)
    viaf_id = db.Column(db.String(100))
    otros_identificadores = db.Column(db.Text)
    imagen_url = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id_autor,
            'nombre_completo': self.nombre_completo,
            'nombre_firma': self.nombre_firma,
            'pseudonimos': self.pseudonimos,
            'fecha_nacimiento': self.fecha_nacimiento,
            'anio_nacimiento': self.anio_nacimiento,
            'lugar_nacimiento': self.lugar_nacimiento,
            'fecha_muerte': self.fecha_muerte,
            'anio_muerte': self.anio_muerte,
            'lugar_muerte': self.lugar_muerte,
            'nacionalidad': self.nacionalidad,
            'ocupacion': self.ocupacion,
            'genero': self.genero,
            'lengua': self.lengua,
            'biografia': self.biografia,
            'bne_identificador': self.bne_identificador,
            'url_datos_bne': self.url_datos_bne,
            'viaf_id': self.viaf_id,
            'otros_identificadores': self.otros_identificadores,
            'imagen_url': self.imagen_url,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'actualizado_en': self.actualizado_en.isoformat() if self.actualizado_en else None
        }


class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    id_usuario = db.Column(db.BigInteger, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(255), unique=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id_usuario,
            'nombre': self.nombre,
            'email': self.email,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'actualizado_en': self.actualizado_en.isoformat() if self.actualizado_en else None
        }


class Obra(db.Model):
    __tablename__ = 'obra'
    
    id_obra = db.Column(db.BigInteger, primary_key=True)
    titulo = db.Column(db.String(500), nullable=False)
    tipo_publicacion = db.Column(db.String(100))
    autor_firma = db.Column(db.String(255))
    nombre_autor = db.Column(db.String(255))
    id_autor = db.Column(db.BigInteger, db.ForeignKey('autor.id_autor'), nullable=True)
    anio = db.Column(db.Integer)
    enlace = db.Column(db.Text, unique=True)
    fecha = db.Column(db.Date)
    dia = db.Column(db.Integer)
    mes = db.Column(db.Integer)
    num_periodico = db.Column(db.String(100))
    variante_titulo = db.Column(db.String(255))
    pseudonimos_autor = db.Column(db.String(255))
    tema_principal = db.Column(db.String(255))
    paginas = db.Column(db.String(500))
    como_citar = db.Column(db.Text)
    imprenta = db.Column(db.String(255))
    lugar_impresion = db.Column(db.String(255))
    imagen_url = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id_obra,
            'titulo': self.titulo,
            'tipo_publicacion': self.tipo_publicacion,
            'autor_firma': self.autor_firma,
            'nombre_autor': self.nombre_autor,
            'id_autor': self.id_autor,
            'anio': self.anio,
            'enlace': self.enlace,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'dia': self.dia,
            'mes': self.mes,
            'num_periodico': self.num_periodico,
            'variante_titulo': self.variante_titulo,
            'pseudonimos_autor': self.pseudonimos_autor,
            'tema_principal': self.tema_principal,
            'paginas': self.paginas,
            'como_citar': self.como_citar,
            'imprenta': self.imprenta,
            'lugar_impresion': self.lugar_impresion,
            'imagen_url': self.imagen_url,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'actualizado_en': self.actualizado_en.isoformat() if self.actualizado_en else None
        }
    
    def to_dict_detallado(self):
        """Devuelve información completa incluyendo datos especializados"""
        resultado = self.to_dict()
        
        # Obtener datos especializados según tipo
        from sqlalchemy import text
        
        tipo = self.tipo_publicacion.lower() if self.tipo_publicacion else ''
        
        # Buscar en tabla especializada correspondiente
        if 'teatro' in tipo or 'dramático' in tipo.lower():
            teatro = db.session.execute(
                text("SELECT fuente_procedencia, resumen, modalidad_teatro, otros_motivos FROM teatro WHERE id_obra = :id"),
                {'id': self.id_obra}
            ).fetchone()
            if teatro:
                resultado['especializado'] = {
                    'tipo_especifico': 'Teatro',
                    'fuente_procedencia': teatro[0],
                    'resumen': teatro[1],
                    'modalidad': teatro[2],
                    'otros_motivos': teatro[3]
                }
        
        elif 'novela' in tipo or 'prosa' in tipo.lower():
            novela = db.session.execute(
                text("SELECT fragmento_donde_aparece, modalidad_novela, tipo_de_ubicacion, aspectos_formales, observaciones FROM novela WHERE id_obra = :id"),
                {'id': self.id_obra}
            ).fetchone()
            if novela:
                resultado['especializado'] = {
                    'tipo_especifico': 'Novela',
                    'fragmento': novela[0],
                    'modalidad': novela[1],
                    'tipo_ubicacion': novela[2],
                    'aspectos_formales': novela[3],
                    'observaciones': novela[4]
                }
        
        elif 'periódico' in tipo or 'prensa' in tipo.lower():
            periodico = db.session.execute(
                text("SELECT modalidad_periodico, num_periodico, fragmento_donde_aparece FROM periodico WHERE id_obra = :id"),
                {'id': self.id_obra}
            ).fetchone()
            if periodico:
                resultado['especializado'] = {
                    'tipo_especifico': 'Periódico',
                    'modalidad': periodico[0],
                    'numero': periodico[1],
                    'fragmento': periodico[2]
                }
        
        elif 'poesía' in tipo or 'poema' in tipo.lower() or 'verso' in tipo.lower():
            poesia = db.session.execute(
                text("SELECT aspectos_formales, resumen, fuente_procedencia, modalidad_poesia FROM poesia WHERE id_obra = :id"),
                {'id': self.id_obra}
            ).fetchone()
            if poesia:
                resultado['especializado'] = {
                    'tipo_especifico': 'Poesía',
                    'aspectos_formales': poesia[0],
                    'resumen': poesia[1],
                    'fuente_procedencia': poesia[2],
                    'modalidad': poesia[3]
                }
        
        elif 'música' in tipo or 'música impresa' in tipo.lower():
            musica = db.session.execute(
                text("SELECT resumen, aspectos_formales, observaciones, modalidad_musica_impresa FROM musica_impresa WHERE id_obra = :id"),
                {'id': self.id_obra}
            ).fetchone()
            if musica:
                resultado['especializado'] = {
                    'tipo_especifico': 'Música Impresa',
                    'resumen': musica[0],
                    'aspectos_formales': musica[1],
                    'observaciones': musica[2],
                    'modalidad': musica[3]
                }
        
        return resultado


class Proyecto(db.Model):
    __tablename__ = 'proyectos'
    
    id_proyecto = db.Column(db.BigInteger, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    cita = db.Column(db.Text)
    usuario_id = db.Column(db.BigInteger, db.ForeignKey('usuario.id_usuario'))
    laboratorio_id = db.Column(db.BigInteger, db.ForeignKey('laboratorio.id_laboratorio'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id_proyecto,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'cita': self.cita,
            'usuario_id': self.usuario_id,
            'laboratorio_id': self.laboratorio_id,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'actualizado_en': self.actualizado_en.isoformat() if self.actualizado_en else None
        }


# ============================================================
# RUTAS - SALUD Y ESTADO
# ============================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'BNE Backend API'
    }), 200


@app.route('/api/version', methods=['GET'])
def get_version():
    """Obtener versión de la API"""
    return jsonify({
        'version': '1.0.0',
        'name': 'BNE Data Collection API',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/api/info', methods=['GET'])
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

@app.route('/api/obras', methods=['GET'])
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


@app.route('/api/obras/<int:obra_id>', methods=['GET'])
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


@app.route('/api/obras/<int:obra_id>/detallada', methods=['GET'])
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


@app.route('/api/obras', methods=['POST'])
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


@app.route('/api/obras/<int:obra_id>', methods=['PUT'])
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


@app.route('/api/obras/<int:obra_id>', methods=['DELETE'])
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


# ============================================================
# RUTAS - ESTADÍSTICAS
# ============================================================

@app.route('/api/estadisticas/resumen', methods=['GET'])
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
        
        return jsonify({
            'obras_por_tipo': [{'tipo': row[1], 'total': row[0]} for row in obras_por_tipo],
            'top_autores': [{'autor': row[0], 'obras': row[1]} for row in obras_por_autor]
        }), 200
    except Exception as e:
        logger.error(f"Error en GET /api/estadisticas/resumen: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================
# RUTAS - BÚSQUEDA
# ============================================================

@app.route('/api/buscar', methods=['GET'])
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


# ============================================================
# RUTAS - PERIÓDICOS POR RANGO DE FECHAS
# ============================================================

@app.route('/api/periodicos/rango-fechas', methods=['GET'])
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


# ============================================================
# RUTAS - SCRAPER E IMPORTACIÓN
# ============================================================

@app.route('/api/importar/url', methods=['POST'])
def importar_obra_url():
    """
    Importa una obra desde su URL en datos.bne.es
    Soporta dos tipos de URLs:
    1. URLs de edición HTML: https://datos.bne.es/edicion/bimo0000659916.html
    2. URLs de datos RDF: https://datos.bne.es/data/XX123456
    
    Body: {"url": "https://datos.bne.es/edicion/bimo0000659916.html"}
    """
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL es requerida'}), 400
        
        logger.info(f"Importando obra desde URL: {url}")
        
        # 1. Verificar si ya existe en BD
        existente = Obra.query.filter_by(enlace=url).first()
        if existente:
            logger.info(f"✓ Obra encontrada en BD: {existente.id_obra}")
            return jsonify({
                'message': 'Obra ya existe en base de datos',
                'data': existente.to_dict(),
                'fuente': 'BD local'
            }), 200
        
        # 2. Determinar tipo de URL y extraer datos
        obra_datos = None
        
        # Detectar si es URL de edición HTML
        if '/edicion/' in url and url.endswith('.html'):
            logger.info("Detectada URL de edición HTML")
            obra_datos = scraper.extraer_datos_edicion_html(url)
        else:
            # Intentar como URL RDF/datos
            logger.info("Intentando como URL de datos RDF")
            obra_datos = scraper.obtener_obra_por_url(url)
        
        if not obra_datos:
            return jsonify({
                'error': 'No se pudo obtener información de la URL',
                'tipo_url': 'edicion' if '/edicion/' in url else 'datos',
                'url': url
            }), 400
        
        # Validar que tiene título
        if not obra_datos.get('titulo'):
            return jsonify({
                'error': 'No se pudo extraer el título de la URL',
                'datos_obtenidos': list(obra_datos.keys())
            }), 400
        
        # Crear nueva obra (mapear campos)
        titulo = obra_datos.get('titulo', '')
        # Limpiar título si tiene punto y coma
        if ';' in titulo:
            titulo = titulo.split(';')[0].strip()
        
        nueva_obra = Obra(
            titulo=titulo,
            tipo_publicacion=obra_datos.get('tipo_publicacion', 'Edición'),
            autor_firma=obra_datos.get('autor_firma') or obra_datos.get('autor'),
            nombre_autor=obra_datos.get('autor'),
            anio=obra_datos.get('anio'),
            enlace=url,
            tema_principal=obra_datos.get('forma_contenido') or obra_datos.get('tema_principal'),
            paginas=obra_datos.get('descripcion_fisica'),
            como_citar=obra_datos.get('como_citar'),
            imprenta=obra_datos.get('editorial'),
            lugar_impresion=obra_datos.get('lugar_publicacion'),
            imagen_url=obra_datos.get('imagen_url')
        )
        
        db.session.add(nueva_obra)
        db.session.commit()
        
        logger.info(f"✓ Obra importada: {nueva_obra.id_obra}")
        
        return jsonify({
            'message': 'Obra importada exitosamente',
            'data': nueva_obra.to_dict(),
            'datos_extraidos': {
                'titulo': obra_datos.get('titulo'),
                'autor': obra_datos.get('autor'),
                'editorial': obra_datos.get('editorial'),
                'lugar_publicacion': obra_datos.get('lugar_publicacion'),
                'fecha_publicacion': obra_datos.get('fecha_publicacion'),
                'descripcion_fisica': obra_datos.get('descripcion_fisica'),
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error en POST /api/importar/url: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/importar/titulo', methods=['POST'])
def importar_obra_titulo():
    """
    Busca obras cuyo título contenga la frase indicada e importa todas las que hagan match.
    Acepta múltiples frases separadas por comas.

    Body: {"titulo": "La Vanguardia, periódico de damas"}
    """
    try:
        from sqlalchemy import or_

        data = request.get_json()
        titulo = data.get('titulo')

        if not titulo or len(titulo) < 2:
            return jsonify({'error': 'Se requiere al menos un término de búsqueda'}), 400

        # Dividir por comas para permitir múltiples frases de título
        keywords = [k.strip() for k in titulo.split(',') if len(k.strip()) >= 2]
        if not keywords:
            keywords = [titulo.strip()]

        logger.info(f"Buscando obras cuyos títulos contienen: {keywords}")

        resultados = {'importadas': [], 'existentes': [], 'errores': []}

        # 1. Registrar todas las que ya existen en BD (match con cualquier keyword)
        filtros = [Obra.titulo.ilike(f'%{kw}%') for kw in keywords]
        existentes_bd = Obra.query.filter(or_(*filtros)).all()
        for obra in existentes_bd:
            resultados['existentes'].append({
                'id': obra.id_obra,
                'titulo': obra.titulo,
                'fuente': 'BD local'
            })
        logger.info(f"  ✓ {len(existentes_bd)} obras existentes en BD")

        # 2. Buscar TODAS las obras en datos.bne.es
        logger.info(f"  Buscando en datos.bne.es...")
        obras_bne = []
        try:
            obras_bne = scraper.buscar_obras_por_titulo_bne(titulo, limit=50)
            logger.info(f"  ✓ {len(obras_bne)} obras encontradas en BNE")
        except Exception as e:
            logger.warning(f"  ⚠️ Error al buscar en datos.bne.es: {e}")

        # 3. Importar las nuevas de BNE
        for obra_datos in obras_bne:
            try:
                enlace = obra_datos.get('enlace') or obra_datos.get('url')

                # Verificar si ya existe por enlace
                if enlace:
                    existente = Obra.query.filter_by(enlace=enlace).first()
                    if existente:
                        if not any(e['id'] == existente.id_obra for e in resultados['existentes']):
                            resultados['existentes'].append({
                                'id': existente.id_obra,
                                'titulo': existente.titulo,
                                'fuente': 'BD local'
                            })
                        continue

                # Obtener datos completos si es URL de edición HTML
                if enlace and '/edicion/' in enlace:
                    try:
                        datos_completos = scraper.extraer_datos_edicion_html(enlace)
                        if datos_completos:
                            obra_datos.update(datos_completos)
                    except Exception as e:
                        logger.warning(f"  ⚠️ No se pudieron completar datos de {obra_datos.get('titulo', '')}: {e}")

                titulo_limpio = obra_datos.get('titulo', '').strip()
                if ';' in titulo_limpio:
                    titulo_limpio = titulo_limpio.split(';')[0].strip()
                titulo_limpio = titulo_limpio.strip('"').strip().rstrip(':').strip()
                titulo_limpio = ' '.join(titulo_limpio.split())

                nueva_obra = Obra(
                    titulo=titulo_limpio if titulo_limpio else 'Sin título',
                    tipo_publicacion=obra_datos.get('tipo_publicacion'),
                    autor_firma=obra_datos.get('autor_firma'),
                    nombre_autor=obra_datos.get('nombre_autor') or obra_datos.get('autor'),
                    anio=obra_datos.get('anio'),
                    enlace=enlace,
                    tema_principal=obra_datos.get('tema_principal') or obra_datos.get('forma_contenido'),
                    paginas=obra_datos.get('paginas') or obra_datos.get('descripcion_fisica'),
                    como_citar=obra_datos.get('como_citar'),
                    imprenta=obra_datos.get('imprenta') or obra_datos.get('editorial'),
                    lugar_impresion=obra_datos.get('lugar_impresion') or obra_datos.get('lugar_publicacion'),
                    imagen_url=obra_datos.get('imagen_url')
                )

                db.session.add(nueva_obra)
                db.session.commit()

                resultados['importadas'].append({
                    'id': nueva_obra.id_obra,
                    'titulo': nueva_obra.titulo,
                    'fuente': 'datos.bne.es'
                })
                logger.info(f"  ✓ Importada: {nueva_obra.titulo}")

            except Exception as e:
                db.session.rollback()
                logger.error(f"  ✗ Error importando '{obra_datos.get('titulo', '')}': {e}")
                resultados['errores'].append({
                    'titulo': obra_datos.get('titulo', 'Desconocido'),
                    'error': str(e)
                })

        total = len(resultados['importadas']) + len(resultados['existentes']) + len(resultados['errores'])
        logger.info(f"✓ Título completado: {total} obras (✓{len(resultados['importadas'])}, 📚{len(resultados['existentes'])}, ✗{len(resultados['errores'])})")

        return jsonify({
            'message': f'Búsqueda por título "{titulo}" completada',
            'estadisticas': {
                'importadas': len(resultados['importadas']),
                'existentes': len(resultados['existentes']),
                'errores': len(resultados['errores']),
                'total': total
            },
            'resultados': resultados
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error en POST /api/importar/titulo: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/importar/nombre', methods=['POST'])
def importar_por_nombre():
    """
    Busca obras por TÍTULO en BD local y datos.bne.es.
    Las obras encontradas en BNE que no estén en BD se guardan automáticamente.

    Body: {"nombre": "Quijote", "limite": 10}
    """
    try:
        data = request.get_json()
        nombre = data.get('nombre', '').strip()
        limite = data.get('limite', 20)

        if not nombre or len(nombre) < 2:
            return jsonify({'error': 'Nombre requerido (mínimo 2 caracteres)'}), 400

        logger.info(f"📋 [NOMBRE] Buscando obras por título: '{nombre}'")

        # 1. Buscar en BD local
        logger.info(f"  1️⃣ Buscando en BD local...")
        resultados_bd = Obra.query.filter(
            Obra.titulo.ilike(f'%{nombre}%')
        ).order_by(Obra.anio.desc(), Obra.titulo.asc()).limit(limite).all()
        logger.info(f"     ✓ Encontradas {len(resultados_bd)} obras en BD local")

        # 2. Buscar en datos.bne.es
        logger.info(f"  2️⃣ Buscando en datos.bne.es...")
        obras_bne_raw = []
        try:
            obras_bne_raw = scraper.buscar_obras_por_titulo_bne(nombre, limit=limite)
            logger.info(f"     ✓ Encontradas {len(obras_bne_raw)} obras en datos.bne.es")
        except Exception as e:
            logger.warning(f"     ⚠️ Error al buscar en datos.bne.es: {e}")

        # 3. Para cada obra de BNE: comprobar si existe en BD y guardar si no está
        guardadas = []
        ya_en_bd = []
        errores_bne = []

        for obra_datos in obras_bne_raw:
            try:
                enlace = obra_datos.get('enlace') or obra_datos.get('url')

                # Comprobar si ya existe en BD por enlace
                if enlace:
                    existente = Obra.query.filter_by(enlace=enlace).first()
                    if existente:
                        ya_en_bd.append({
                            'id': existente.id_obra,
                            'titulo': existente.titulo,
                            'enlace': enlace,
                            'fuente': 'BD local'
                        })
                        logger.info(f"     📚 Ya existe: {existente.titulo}")
                        continue

                # Intentar obtener datos completos desde HTML si es URL de edición
                if enlace and '/edicion/' in enlace:
                    try:
                        datos_completos = scraper.extraer_datos_edicion_html(enlace)
                        if datos_completos:
                            obra_datos.update(datos_completos)
                    except Exception as e:
                        logger.warning(f"     ⚠️ No se pudieron completar datos de '{obra_datos.get('titulo', '')}': {e}")

                # Limpiar título
                titulo_limpio = obra_datos.get('titulo', '').strip()
                if ';' in titulo_limpio:
                    titulo_limpio = titulo_limpio.split(';')[0].strip()
                titulo_limpio = titulo_limpio.strip('"').strip().rstrip(':').strip()
                titulo_limpio = ' '.join(titulo_limpio.split())

                if not titulo_limpio:
                    continue

                # Guardar en BD
                nueva_obra = Obra(
                    titulo=titulo_limpio,
                    tipo_publicacion=obra_datos.get('tipo_publicacion'),
                    autor_firma=obra_datos.get('autor_firma'),
                    nombre_autor=obra_datos.get('nombre_autor') or obra_datos.get('autor'),
                    anio=obra_datos.get('anio'),
                    enlace=enlace,
                    tema_principal=obra_datos.get('tema_principal') or obra_datos.get('forma_contenido'),
                    paginas=obra_datos.get('paginas') or obra_datos.get('descripcion_fisica'),
                    como_citar=obra_datos.get('como_citar'),
                    imprenta=obra_datos.get('imprenta') or obra_datos.get('editorial'),
                    lugar_impresion=obra_datos.get('lugar_impresion') or obra_datos.get('lugar_publicacion'),
                    imagen_url=obra_datos.get('imagen_url')
                )
                db.session.add(nueva_obra)
                db.session.commit()

                guardadas.append({
                    'id': nueva_obra.id_obra,
                    'titulo': nueva_obra.titulo,
                    'enlace': enlace or '',
                    'fuente': 'datos.bne.es'
                })
                logger.info(f"     ✓ Guardada nueva obra: {nueva_obra.titulo}")

            except Exception as e:
                db.session.rollback()
                logger.error(f"     ✗ Error guardando '{obra_datos.get('titulo', '')}': {e}")
                errores_bne.append({
                    'titulo': obra_datos.get('titulo', 'Desconocido'),
                    'error': str(e)
                })

        total_bne = len(guardadas) + len(ya_en_bd) + len(errores_bne)
        logger.info(f"✓ Completado: {len(resultados_bd)} en BD local, {len(guardadas)} nuevas guardadas, {len(ya_en_bd)} ya existían")

        return jsonify({
            'nombre_buscado': nombre,
            'total_encontrados': len(resultados_bd) + total_bne,
            'estadisticas': {
                'en_bd_local': len(resultados_bd),
                'en_datos_bne': total_bne,
                'guardadas_nuevas': len(guardadas),
                'ya_existentes': len(ya_en_bd),
                'errores': len(errores_bne)
            },
            'resultados_bd_local': [
                {**obra.to_dict_detallado(), 'fuente': 'BD local'}
                for obra in resultados_bd
            ],
            'guardadas': guardadas,
            'ya_en_bd': ya_en_bd,
            'errores_bne': errores_bne,
            'mensaje': f'✅ {len(resultados_bd)} en BD local · {len(guardadas)} nuevas guardadas · {len(ya_en_bd)} ya existían en BNE'
        }), 200

    except Exception as e:
        logger.error(f"❌ Error en /api/importar/nombre: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/importar/lote', methods=['POST'])
def importar_obras_lote():
    """
    Importa múltiples obras desde títulos o URLs (HTML o RDF)
    Soporta:
    - URLs de edición: https://datos.bne.es/edicion/bimo0000659916.html
    - URLs de datos: https://datos.bne.es/data/XX123456
    - Títulos: "El Quijote"
    
    Body: {
      "obras": [
        {"url": "https://datos.bne.es/edicion/bimo...html"},
        {"titulo": "El Quijote"},
        {"url": "https://datos.bne.es/data/XX123456"}
      ]
    }
    """
    try:
        data = request.get_json()
        obras_input = data.get('obras', [])
        
        if not obras_input or not isinstance(obras_input, list):
            return jsonify({'error': 'Se requiere array de obras'}), 400
        
        resultados = {
            'importadas': [],
            'existentes': [],
            'errores': []
        }
        
        for i, item in enumerate(obras_input):
            try:
                existente_bd = None
                obra_datos = None
                origen = None
                
                # PASO 1: Buscar en BD
                if 'url' in item:
                    url = item['url'].strip()
                    existente_bd = Obra.query.filter_by(enlace=url).first()
                    origen = f"URL: {url[:60]}..."
                
                elif 'titulo' in item:
                    titulo = item['titulo'].strip()
                    existente_bd = Obra.query.filter(
                        Obra.titulo.ilike(f'%{titulo}%')
                    ).first()
                    origen = f"Título: {titulo}"
                
                # Si existe en BD, no hacer scraping
                if existente_bd:
                    resultados['existentes'].append({
                        'id': existente_bd.id_obra,
                        'titulo': existente_bd.titulo,
                        'origen': origen,
                        'fuente': 'BD local'
                    })
                    continue
                
                # PASO 2: Si no existe en BD, buscar en datos.bne.es
                if 'url' in item:
                    url = item['url'].strip()
                    # Detectar tipo de URL
                    if '/edicion/' in url and url.endswith('.html'):
                        logger.info(f"[LOTE {i+1}] Detectada URL de edición HTML")
                        obra_datos = scraper.extraer_datos_edicion_html(url)
                    else:
                        logger.info(f"[LOTE {i+1}] Detectada URL de datos RDF")
                        obra_datos = scraper.obtener_obra_por_url(url)
                
                elif 'titulo' in item:
                    titulo = item['titulo'].strip()
                    logger.info(f"[LOTE {i+1}] Buscando por título: {titulo}")
                    obra_datos = scraper.obtener_obra_por_titulo(titulo)
                
                if not obra_datos:
                    resultados['errores'].append({
                        'indice': i + 1,
                        'origen': origen or 'Desconocido',
                        'error': 'No se pudo obtener información'
                    })
                    continue
                
                # PASO 3: Verificación final por enlace (URL exacta)
                url_verificar = item.get('url') if 'url' in item else None
                if url_verificar:
                    existente_final = Obra.query.filter_by(enlace=url_verificar).first()
                    if existente_final:
                        resultados['existentes'].append({
                            'id': existente_final.id_obra,
                            'titulo': existente_final.titulo,
                            'origen': origen,
                            'fuente': 'BD local'
                        })
                        continue
                
                # PASO 4: Limpiar título y crear obra
                titulo_limpio = obra_datos.get('titulo', '').strip()
                # Limpiar caracteres especiales y separadores
                if ';' in titulo_limpio:
                    titulo_limpio = titulo_limpio.split(';')[0].strip()
                # Remover comillas al inicio y final
                titulo_limpio = titulo_limpio.strip('"').strip()
                # Remover dos puntos finales
                titulo_limpio = titulo_limpio.rstrip(':').strip()
                # Remover espacios extras
                titulo_limpio = ' '.join(titulo_limpio.split())
                
                nueva_obra = Obra(
                    titulo=titulo_limpio if titulo_limpio else 'Sin título',
                    tipo_publicacion=obra_datos.get('tipo_publicacion', 'Edición'),
                    autor_firma=obra_datos.get('autor_firma') or obra_datos.get('autor'),
                    nombre_autor=obra_datos.get('autor') or obra_datos.get('nombre_autor'),
                    anio=obra_datos.get('anio'),
                    enlace=item.get('url', ''),
                    tema_principal=obra_datos.get('forma_contenido') or obra_datos.get('tema_principal'),
                    paginas=obra_datos.get('descripcion_fisica') or obra_datos.get('paginas'),
                    como_citar=obra_datos.get('como_citar'),
                    imprenta=obra_datos.get('editorial') or obra_datos.get('imprenta'),
                    lugar_impresion=obra_datos.get('lugar_publicacion'),
                    imagen_url=obra_datos.get('imagen_url')
                )
                
                db.session.add(nueva_obra)
                db.session.commit()
                
                resultados['importadas'].append({
                    'id': nueva_obra.id_obra,
                    'titulo': nueva_obra.titulo,
                    'origen': origen,
                    'fuente': 'datos.bne.es'
                })
                
                logger.info(f"[LOTE {i+1}] ✓ Importada: {nueva_obra.titulo}")
                
            except Exception as e:
                logger.error(f"[LOTE {i+1}] Error: {e}")
                resultados['errores'].append({
                    'indice': i + 1,
                    'origen': origen or 'Desconocido',
                    'error': str(e)
                })
        
        total = len(resultados['importadas']) + len(resultados['existentes']) + len(resultados['errores'])
        
        logger.info(f"📊 LOTE COMPLETADO: {total} obras (✓{len(resultados['importadas'])}, 📚{len(resultados['existentes'])}, ✗{len(resultados['errores'])})")
        
        return jsonify({
            'message': f'Procesadas {total} obras',
            'estadisticas': {
                'importadas': len(resultados['importadas']),
                'existentes': len(resultados['existentes']),
                'errores': len(resultados['errores']),
                'total': total
            },
            'resultados': resultados
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Error fatal en POST /api/importar/lote: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/importar/edicion/html', methods=['POST'])
def importar_edicion_html():
    """
    Importa una edición desde una página HTML de datos.bne.es
    Extrae datos estructurados de URLs como:
    https://datos.bne.es/edicion/bimo0000659916.html
    
    Body: {"url": "https://datos.bne.es/edicion/bimo0000659916.html"}
    """
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL es requerida'}), 400
        
        if '/edicion/' not in url:
            return jsonify({'error': 'URL debe ser de una edición de datos.bne.es (contener /edicion/)'}), 400
        
        logger.info(f"Importando edición desde HTML: {url}")
        
        # Verificar si ya existe por URL
        existente = Obra.query.filter_by(enlace=url).first()
        if existente:
            logger.info(f"✓ Edición ya importada: {existente.id_obra}")
            return jsonify({
                'message': 'Edición ya existe en base de datos',
                'data': existente.to_dict(),
                'fuente': 'BD local'
            }), 200
        
        # Extraer datos del HTML
        logger.info("Extrayendo datos del HTML...")
        datos_edicion = scraper.extraer_datos_edicion_html(url)
        
        if not datos_edicion:
            return jsonify({
                'error': 'No se pudo extraer información de la página',
                'url': url
            }), 400
        
        # Validar que tiene título
        if not datos_edicion.get('titulo'):
            return jsonify({
                'error': 'No se pudo extraer el título de la edición',
                'url': url,
                'datos_obtenidos': list(datos_edicion.keys())
            }), 400
        
        # Crear nueva obra
        nueva_obra = Obra(
            titulo=datos_edicion.get('titulo'),
            tipo_publicacion='Edición',
            autor_firma=datos_edicion.get('autor_firma'),
            nombre_autor=datos_edicion.get('autor'),
            anio=None,  # Extraer de fecha si es posible
            enlace=url,
            tema_principal=datos_edicion.get('forma_contenido'),
            paginas=datos_edicion.get('descripcion_fisica'),
            como_citar=None,
            imagen_url=datos_edicion.get('imagen_url')
        )
        
        db.session.add(nueva_obra)
        db.session.commit()
        
        logger.info(f"✓ Edición importada: {nueva_obra.id_obra}")
        
        return jsonify({
            'message': 'Edición importada exitosamente',
            'data': nueva_obra.to_dict(),
            'datos_extraidos': {
                'titulo': datos_edicion.get('titulo'),
                'autor': datos_edicion.get('autor'),
                'autor_firma': datos_edicion.get('autor_firma'),
                'editorial': datos_edicion.get('editorial'),
                'lugar_publicacion': datos_edicion.get('lugar_publicacion'),
                'fecha_publicacion': datos_edicion.get('fecha_publicacion'),
                'descripcion_fisica': datos_edicion.get('descripcion_fisica'),
                'dimensiones': datos_edicion.get('dimensiones'),
                'forma_contenido': datos_edicion.get('forma_contenido'),
                'tipo_medio': datos_edicion.get('tipo_medio'),
                'notas': datos_edicion.get('notas', []),
                'recursos_relacionados': datos_edicion.get('recursos_relacionados', [])
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error en POST /api/importar/edicion/html: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ============================================================
# MANEJO DE ERRORES
# ============================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404


# ============================================================
# RUTAS - BÚSQUEDA DE DATASETS EN KAGGLE
# ============================================================

@app.route('/api/buscar-datasets/kaggle', methods=['POST'])
def buscar_datasets_kaggle():
    """
    Busca datasets en Kaggle usando la API oficial
    
    REQUISITO: Credenciales de Kaggle configuradas
    - Crear cuenta en https://www.kaggle.com
    - Ir a Settings → API → Create New API Token
    - Guardar archivo en ~/.kaggle/kaggle.json (auto-detectado)
    
    Body: {
        "query": "periódicos historia españa",
        "num_resultados": 10,
        "sort_by": "votes",  # votes, newest, downloads
        "license": "all"     # all, cc, cc0, gpl, odb, etc
    }
    
    Response: {
        "query": "periódicos",
        "fuente": "kaggle",
        "cantidad": 5,
        "resultados": [
            {
                "titulo": "user/dataset-name",
                "descripcion": "Spanish Newspapers Collection",
                "url": "https://www.kaggle.com/datasets/user/dataset-name",
                "descargas": 1245,
                "votos": 89,
                "tamaño": "2.5 GB",
                "actualizado": "2024-01-15"
            },
            ...
        ],
        "mensaje": "✅ Búsqueda completada: 5 datasets encontrados"
    }
    """
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        num_resultados = data.get('num_resultados', 10)
        sort_by = data.get('sort_by', 'votes')  # votes, newest, downloads
        license_filter = data.get('license', 'all')
        
        if not query or len(query) < 3:
            return jsonify({'error': 'Query debe tener al menos 3 caracteres'}), 400
        
        if num_resultados < 1 or num_resultados > 100:
            return jsonify({'error': 'num_resultados debe estar entre 1 y 100'}), 400
        
        logger.info(f"🔍 [KAGGLE] Buscando datasets: '{query}'")
        
        try:
            from kaggle.api.kaggle_api_extended import KaggleApi
            
            # Inicializar API de Kaggle (requiere ~/.kaggle/kaggle.json)
            api = KaggleApi()
            api.authenticate()
            
            logger.info(f"  ✓ Autenticación en Kaggle exitosa")
            
            # Realizar búsqueda
            logger.info(f"  ⏳ Buscando {num_resultados} datasets...")
            
            datasets = api.dataset_list(
                search=query,
                sort_by=sort_by,
                max_size=None,
                file_type='all',
                license=license_filter,
                page_size=num_resultados
            )
            
            # Procesar resultados
            resultados = []
            for idx, dataset in enumerate(datasets):
                if idx >= num_resultados:
                    break
                
                try:
                    # Obtener información detallada del dataset
                    resultado = {
                        'indice': idx + 1,
                        'titulo': dataset.ref,  # "user/dataset-name"
                        'descripcion': dataset.title,
                        'url': f"https://www.kaggle.com/datasets/{dataset.ref}",
                        'descargas': getattr(dataset, 'download_count', 0),
                        'votos': getattr(dataset, 'voteCount', 0),
                        'likes': getattr(dataset, 'medalCount', 0),
                        'actualizado': str(getattr(dataset, 'lastUpdated', 'N/A')),
                        'creador': dataset.ref.split('/')[0],  # Extraer usuario
                        'tamaño': getattr(dataset, 'datasetSize', 'N/A'),
                        'topicTags': getattr(dataset, 'topicTags', [])
                    }
                    resultados.append(resultado)
                except Exception as e:
                    logger.warning(f"  ⚠️ Error procesando dataset {idx + 1}: {e}")
                    continue
            
            logger.info(f"  ✓ Encontrados {len(resultados)} datasets")
            
            return jsonify({
                'query': query,
                'fuente': 'kaggle',
                'cantidad': len(resultados),
                'parametros': {
                    'sort_by': sort_by,
                    'license': license_filter,
                    'solicitados': num_resultados
                },
                'resultados': resultados,
                'mensaje': f'✅ Búsqueda completada: {len(resultados)} datasets encontrados en Kaggle'
            }), 200
        
        except ImportError:
            return jsonify({
                'error': 'Librería kaggle no instalada',
                'instrucciones': 'Ejecuta: pip install kaggle'
            }), 501
        
        except Exception as e:
            error_msg = str(e)
            
            # Detectar si es error de autenticación
            if 'kaggle.json' in error_msg or 'Credentials' in error_msg:
                return jsonify({
                    'error': 'Credenciales de Kaggle no configuradas',
                    'instrucciones': [
                        '1. Crear cuenta en https://www.kaggle.com',
                        '2. Ir a Settings → Account → API → Create New API Token',
                        '3. Descargar kaggle.json',
                        '4. Guardar en ~/.kaggle/kaggle.json',
                        '5. En Windows: C:\\Users\\{usuario}\\.kaggle\\kaggle.json'
                    ]
                }), 401
            
            logger.error(f"❌ Error en búsqueda Kaggle: {error_msg}")
            return jsonify({'error': f'Error buscando en Kaggle: {error_msg}'}), 500
    
    except Exception as e:
        logger.error(f"❌ Error en POST /api/buscar-datasets/kaggle: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================
# RUTAS - AUTORES
# ============================================================

@app.route('/api/autores', methods=['GET'])
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


@app.route('/api/autores/<int:autor_id>', methods=['GET'])
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


@app.route('/api/autores', methods=['POST'])
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


@app.route('/api/autores/<int:autor_id>', methods=['PUT'])
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


@app.route('/api/autores/<int:autor_id>', methods=['DELETE'])
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


@app.route('/api/importar/autores', methods=['POST'])
def importar_autores():
    """
    Busca un autor en datos.bne.es por nombre o URL y lo guarda en la BD de autores.

    Body:
      {"nombre": "García Lorca"}          → busca por nombre en datos.bne.es
      {"url": "https://datos.bne.es/persona/XX4556545.html"}  → extrae directamente
    """
    try:
        data = request.get_json()
        nombre = data.get('nombre', '').strip()
        url = data.get('url', '').strip()

        if not nombre and not url:
            return jsonify({'error': 'Se requiere nombre o url'}), 400

        resultados = {'importados': [], 'existentes': [], 'errores': []}

        autores_datos = []

        if url:
            # Extracción directa desde una URL de persona BNE
            logger.info(f"Extrayendo autor desde URL: {url}")
            datos = scraper.extraer_datos_autor_html(url)
            if datos:
                autores_datos.append(datos)
            else:
                return jsonify({'error': 'No se pudieron extraer datos del autor desde la URL'}), 422
        else:
            # Búsqueda por nombre
            logger.info(f"Buscando autor por nombre: {nombre}")
            autores_datos = scraper.buscar_autores_bne(nombre)

        for datos_autor in autores_datos:
            try:
                bne_id = datos_autor.get('bne_identificador')

                # Comprobar si ya existe
                existente = None
                if bne_id:
                    existente = Autor.query.filter_by(bne_identificador=bne_id).first()
                if not existente:
                    nombre_bne = datos_autor.get('nombre_completo', '')
                    if nombre_bne:
                        existente = Autor.query.filter_by(nombre_completo=nombre_bne).first()

                if existente:
                    resultados['existentes'].append({'id': existente.id_autor,
                                                     'nombre': existente.nombre_completo})
                    continue

                nuevo = Autor(
                    nombre_completo=datos_autor.get('nombre_completo', nombre or 'Desconocido'),
                    nombre_firma=datos_autor.get('nombre_firma'),
                    pseudonimos=datos_autor.get('pseudonimos'),
                    fecha_nacimiento=datos_autor.get('fecha_nacimiento'),
                    anio_nacimiento=datos_autor.get('anio_nacimiento'),
                    lugar_nacimiento=datos_autor.get('lugar_nacimiento'),
                    fecha_muerte=datos_autor.get('fecha_muerte'),
                    anio_muerte=datos_autor.get('anio_muerte'),
                    lugar_muerte=datos_autor.get('lugar_muerte'),
                    nacionalidad=datos_autor.get('nacionalidad'),
                    ocupacion=datos_autor.get('ocupacion'),
                    genero=datos_autor.get('genero'),
                    lengua=datos_autor.get('lengua'),
                    biografia=datos_autor.get('biografia'),
                    bne_identificador=bne_id,
                    url_datos_bne=datos_autor.get('url_datos_bne'),
                    viaf_id=datos_autor.get('viaf_id'),
                    otros_identificadores=datos_autor.get('otros_identificadores'),
                    imagen_url=datos_autor.get('imagen_url')
                )
                db.session.add(nuevo)
                db.session.commit()
                resultados['importados'].append({'id': nuevo.id_autor,
                                                 'nombre': nuevo.nombre_completo})
                logger.info(f"Autor importado: {nuevo.nombre_completo}")

            except Exception as e:
                db.session.rollback()
                logger.error(f"Error importando autor '{datos_autor.get('nombre_completo', '')}': {e}")
                resultados['errores'].append({'nombre': datos_autor.get('nombre_completo', ''),
                                              'error': str(e)})

        return jsonify({
            'mensaje': f"{len(resultados['importados'])} autores importados, "
                       f"{len(resultados['existentes'])} ya existían, "
                       f"{len(resultados['errores'])} errores",
            'estadisticas': {
                'importados': len(resultados['importados']),
                'existentes': len(resultados['existentes']),
                'errores': len(resultados['errores'])
            },
            'resultados': resultados
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error en POST /api/importar/autores: {e}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Error interno del servidor'}), 500


# ============================================================
# INICIALIZACIÓN
# ============================================================

def create_app():
    """Factory function para crear la aplicación"""
    with app.app_context():
        db.create_all()
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=os.environ.get('FLASK_ENV') == 'development', host='0.0.0.0', port=5000)
