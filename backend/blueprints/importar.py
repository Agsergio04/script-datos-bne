import logging
from datetime import datetime
from flask import Blueprint, jsonify, request
from extensions import db
from models import Obra, Autor, Usuario, Proyecto
from services.scraper import scraper

bp = Blueprint("importar", __name__)
logger = logging.getLogger(__name__)


@bp.route('/api/importar/url', methods=['POST'])
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
        
        # Cualquier página HTML de datos.bne.es (/edicion/, /obra/, /recurso/...)
        # se procesa con el extractor HTML (tablas, h1, og:image).
        if url.endswith('.html'):
            logger.info("Detectada URL HTML de datos.bne.es")
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


@bp.route('/api/importar/titulo', methods=['POST'])
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

                # Completar datos (incl. imagen_url) para cualquier HTML de datos.bne.es
                if enlace and enlace.endswith('.html'):
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


@bp.route('/api/importar/nombre', methods=['POST'])
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

                # Completar datos (incl. imagen_url) para cualquier HTML de datos.bne.es
                if enlace and enlace.endswith('.html'):
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


@bp.route('/api/importar/lote', methods=['POST'])
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
                    # Cualquier página HTML de datos.bne.es usa el extractor HTML
                    if url.endswith('.html'):
                        logger.info(f"[LOTE {i+1}] Detectada URL HTML de datos.bne.es")
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


@bp.route('/api/importar/edicion/html', methods=['POST'])
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
@bp.route('/api/importar/autores', methods=['POST'])
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

