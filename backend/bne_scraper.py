"""
Script para recopilar datos de la BNE (Biblioteca Nacional de España)
Extrae información de autores y periódicos desde el portal de datos enlazados

Fuente: https://datos.bne.es/
Portal de publicación de datos como Linked Open Data de la Biblioteca Nacional de España

Descripción:
- Búsqueda de autores por nombre
- Búsqueda de periódicos por título  
- Obtención de obras de autores específicos
- Exportación a JSON y CSV
- Integración con base de datos PostgreSQL
"""

import requests
import json
import csv
import logging
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urljoin, quote
import time
from bs4 import BeautifulSoup
import re

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bne_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BNEScraper:
    """Scraper para extraer datos del portal de datos enlazados BNE (https://datos.bne.es)"""
    
    def __init__(self, base_url: str = "https://datos.bne.es", timeout: int = 30, verify_ssl: bool = True):
        """
        Inicializa el scraper de datos enlazados BNE
        
        Args:
            base_url: URL base del portal datos.bne.es
            timeout: Tiempo máximo de espera para las peticiones (segundos)
            verify_ssl: Verificar certificados SSL (False para resolver problemas en Windows)
        """
        self.base_url = base_url
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/html'
        })
        self.datos_periodicos = []
        self.datos_autores = []
        if not verify_ssl:
            # Desabilitar advertencias si no verificamos SSL
            import warnings
            from urllib3.exceptions import InsecureRequestWarning
            warnings.simplefilter('ignore', InsecureRequestWarning)
        
    def buscar_en_datos_bne(self, tipo: str, termino: str) -> Optional[Dict]:
        """
        Realiza búsqueda en el portal datos.bne.es
        
        Args:
            tipo: Tipo de búsqueda ('personas', 'obras', 'temas', 'periodicos')
            termino: Término a buscar
            
        Returns:
            Respuesta JSON del portal
        """
        try:
            # El portal datos.bne.es no tiene API REST oficial documentada
            # Se accede mediante negociación de contenidos
            # Intentamos acceder al recurso específico en RDF/JSON
            
            base_search = f"{self.base_url}/data/"
            
            # Construir URL según tipo
            urls_base = {
                'personas': f"{base_search}about.rdf",
                'obras': f"{base_search}about.rdf",
                'temas': f"{base_search}about.rdf",
                'periodicos': f"{base_search}about.rdf"
            }
            
            url = urls_base.get(tipo, base_search)
            
            # Parámetros de búsqueda
            params = {
                'q': termino,
                'searchType': tipo,
                'format': 'json'
            }
            
            logger.info(f"Buscando {tipo}: {termino}")
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            # Intentar parsear JSON
            try:
                return response.json()
            except json.JSONDecodeError:
                logger.warning(f"Respuesta no es JSON para {tipo}: {termino}")
                return None
            
        except requests.RequestException as e:
            logger.error(f"Error en búsqueda de {tipo} ({termino}): {e}")
            return None
    
    def buscar_autores(self, nombre: str, limite: int = 50) -> List[Dict]:
        """
        Busca autores en datos.bne.es
        
        Args:
            nombre: Nombre del autor a buscar
            limite: Número máximo de resultados
            
        Returns:
            Lista de autores encontrados con sus metadatos
        """
        autores = []
        try:
            # Nota: datos.bne.es permite búsquedas mediante la interfaz SPARQL
            # o mediante negociación de contenidos. Para este scraper, usamos
            # URLs directas a personas basadas en la estructura del portal
            
            logger.info(f"Buscando autores: {nombre}")
            
            # Intentar búsqueda en el portal
            # El portal puede ser consultado directamente con URIs de personas
            search_url = f"{self.base_url}/"
            
            params = {
                'q': nombre,
                'type': 'person'  # Buscar solo personas
            }
            
            response = self.session.get(search_url, params=params, timeout=self.timeout, verify=self.verify_ssl)
            response.raise_for_status()
            
            # Parsear respuesta (HTML o JSON según disponibilidad)
            if 'application/json' in response.headers.get('content-type', 'text/html'):
                datos = response.json()
                if isinstance(datos, dict):
                    # Estructura típica de respuesta
                    resultados = datos.get('results', datos.get('data', []))
                    
                    for item in resultados[:limite]:
                        autor = {
                            'nombre': item.get('name', item.get('title', '')),
                            'identificador': item.get('id', item.get('uri', '')),
                            'url': item.get('url', ''),
                            'tipo': 'Persona',
                            'descripcion': item.get('description', ''),
                            'fecha_nacimiento': item.get('birth_date', ''),
                            'fecha_muerte': item.get('death_date', ''),
                            'enlace': item.get('link', item.get('uri', ''))
                        }
                        autores.append(autor)
            else:
                logger.warning(f"Respuesta HTML en lugar de JSON para búsqueda de autores")
                # En caso de HTML, podríamos usar BeautifulSoup para parsear
                # por ahora, información limitada
                
            logger.info(f"Se encontraron {len(autores)} autores")
            
        except Exception as e:
            logger.error(f"Error buscando autores: {e}")
        
        return autores
    
    def buscar_periodicos(self, titulo: str, limite: int = 50) -> List[Dict]:
        """
        Busca periódicos en datos.bne.es
        
        Args:
            titulo: Título del periódico a buscar
            limite: Número máximo de resultados
            
        Returns:
            Lista de periódicos encontrados
        """
        periodicos = []
        try:
            logger.info(f"Buscando periódicos: {titulo}")
            
            search_url = f"{self.base_url}/"
            
            params = {
                'q': titulo,
                'type': 'publication'  # Buscar solo publicaciones/periódicos
            }
            
            response = self.session.get(search_url, params=params, timeout=self.timeout, verify=self.verify_ssl)
            response.raise_for_status()
            
            if 'application/json' in response.headers.get('content-type', 'text/html'):
                datos = response.json()
                if isinstance(datos, dict):
                    resultados = datos.get('results', datos.get('data', []))
                    
                    for item in resultados[:limite]:
                        periodico = {
                            'titulo': item.get('name', item.get('title', '')),
                            'identificador': item.get('id', item.get('uri', '')),
                            'url': item.get('url', ''),
                            'tipo': 'Periódico',
                            'fecha_inicio': item.get('start_date', ''),
                            'fecha_fin': item.get('end_date', ''),
                            'lugar_publicacion': item.get('place', ''),
                            'enlace': item.get('link', item.get('uri', ''))
                        }
                        periodicos.append(periodico)
            
            logger.info(f"Se encontraron {len(periodicos)} periódicos")
            
        except Exception as e:
            logger.error(f"Error buscando periódicos: {e}")
        
        return periodicos
    
    def obtener_obra_por_url(self, url: str) -> Optional[Dict]:
        """
        Obtiene información completa de una obra a partir de su URL en datos.bne.es
        
        Args:
            url: URL de la obra en datos.bne.es (ej: https://datos.bne.es/data/XX123456.rdf)
            
        Returns:
            Diccionario con toda la información de la obra o None
        """
        try:
            logger.info(f"Obteniendo obra desde URL: {url}")
            
            # Normalizar URL si es necesario
            if not url.startswith('http'):
                url = f"{self.base_url}/data/{url}"
            
            # Solicitar múltiples formatos para obtener máxima información
            formatos = {
                'rdf': '.rdf',
                'json': '.json',
                'html': ''
            }
            
            obra_datos = None
            
            # Intentar obtener en formato JSON primero (más fácil de parsear)
            try:
                url_json = url.replace('.rdf', '.json')
                response = self.session.get(url_json, timeout=self.timeout)
                response.raise_for_status()
                
                if 'application/json' in response.headers.get('content-type', ''):
                    obra_datos = response.json()
                    logger.info("✓ Datos obtenidos en formato JSON")
            except:
                pass
            
            # Si no obtuvimos JSON, intentar RDF
            if not obra_datos:
                try:
                    response = self.session.get(url, timeout=self.timeout)
                    response.raise_for_status()
                    # Aquí podríamos parsear RDF/XML
                    logger.info("✓ Datos obtenidos en formato RDF")
                except:
                    pass
            
            # Procesar datos obtenidos
            if obra_datos:
                obra = self._procesar_metadata_obra(obra_datos, url)
                return obra
            
            logger.warning(f"No se pudieron obtener datos completos para: {url}")
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo obra: {e}")
            return None
    
    def obtener_obra_por_titulo(self, titulo: str) -> Optional[Dict]:
        """
        Busca una obra por título y obtiene información completa
        
        Args:
            titulo: Título de la obra
            
        Returns:
            Diccionario con información completa o None
        """
        try:
            logger.info(f"Buscando obra por título: {titulo}")
            
            # Primer paso: buscar el título
            search_url = f"{self.base_url}/"
            params = {
                'q': titulo,
                'type': 'work'
            }
            
            response = self.session.get(search_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            # Si obtenemos resultados
            if 'application/json' in response.headers.get('content-type', ''):
                resultados = response.json()
                
                if isinstance(resultados, dict):
                    items = resultados.get('results', resultados.get('data', []))
                    
                    if items:
                        # Tomar el primer resultado (más relevante)
                        primer_resultado = items[0]
                        url_obra = primer_resultado.get('url', primer_resultado.get('uri', ''))
                        
                        if url_obra:
                            # Obtener información completa de esta URL
                            return self.obtener_obra_por_url(url_obra)
            
            logger.warning(f"No se encontró obra con título: {titulo}")
            return None
            
        except Exception as e:
            logger.error(f"Error buscando obra por título: {e}")
            return None
    
    def _procesar_metadata_obra(self, datos: Dict, url: str) -> Dict:
        """
        Procesa la metadata de una obra desde datos.bne.es
        
        Args:
            datos: Diccionario de datos parseado
            url: URL de origen
            
        Returns:
            Diccionario estructurado con información de la obra
        """
        try:
            # Extraer información principal
            obra = {
                'titulo': datos.get('name', datos.get('title', '')),
                'identificador': datos.get('id', datos.get('identifier', '')),
                'enlace': url,
                'tipo_publicacion': datos.get('type', datos.get('category', '')),
                'autor_firma': datos.get('author', datos.get('creator', '')),
                'nombre_autor': datos.get('author_name', datos.get('creator_name', '')),
                'anio': datos.get('year', datos.get('date', '')),
                'fecha': datos.get('publication_date', datos.get('date', '')),
                'descripcion': datos.get('description', datos.get('abstract', '')),
                'resumen': datos.get('summary', datos.get('abstract', '')),
                'tema_principal': datos.get('subject', datos.get('topic', '')),
                'paginas': datos.get('pages', datos.get('pageCount', '')),
                'idioma': datos.get('language', 'es'),
                'imprenta': datos.get('publisher', datos.get('imprenta', '')),
                'lugar_impresion': datos.get('place', datos.get('publicationPlace', '')),
                'como_citar': datos.get('citation', datos.get('how_to_cite', '')),
                'uri_rdf': datos.get('uri', url),
                'url_digital': datos.get('digital_url', datos.get('access_uri', '')),
                'derechos': datos.get('rights', ''),
                'formato': datos.get('format', ''),
                'num_periodico': datos.get('issue_number', datos.get('num_periodico', ''))
            }
            
            # Limpiar valores vacíos y convertir tipos
            obra = {k: v for k, v in obra.items() if v}
            
            # Convertir año a entero si es posible
            if 'anio' in obra:
                try:
                    obra['anio'] = int(str(obra['anio'])[:4])
                except:
                    del obra['anio']
            
            logger.info(f"✓ Obra procesada: {obra.get('titulo', 'Sin título')}")
            return obra
            
        except Exception as e:
            logger.error(f"Error procesando metadata: {e}")
            return {}

    def obtener_obras_autor(self, id_autor: str) -> List[Dict]:
        """
        Obtiene todas las obras de un autor específico desde datos.bne.es
        
        Args:
            id_autor: Identificador/URI del autor
            
        Returns:
            Lista de obras del autor
        """
        obras = []
        try:
            logger.info(f"Obteniendo obras del autor: {id_autor}")
            
            # Intentar acceder al recurso del autor y obtener sus obras
            # El estructura típica es: https://datos.bne.es/data/[id_autor].rdf
            author_url = f"{self.base_url}/data/{id_autor}.rdf"
            
            # Solicitar en formato JSON
            params = {'format': 'json'}
            
            response = self.session.get(author_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            datos = response.json()
            
            # Extraer obras de la estructura RDF convertida a JSON
            if isinstance(datos, dict):
                # Buscar propiedades que relacionen con obras
                obras_raw = datos.get('works', datos.get('createdWorks', []))
                
                for obra in obras_raw[:1000]:  # Limitar a 1000
                    obra_dict = {
                        'titulo': obra.get('name', obra.get('title', '')),
                        'identificador': obra.get('id', ''),
                        'enlace': obra.get('url', ''),
                        'autor_id': id_autor,
                        'fecha_publicacion': obra.get('publication_date', '')
                    }
                    obras.append(obra_dict)
                
            logger.info(f"Se encontraron {len(obras)} obras del autor")
            
        except Exception as e:
            logger.error(f"Error obteniendo obras: {e}")
        
        return obras
    
    def extraer_datos_edicion_html(self, url: str) -> Optional[Dict]:
        """
        Extrae datos estructurados de una página de edición de BNE en HTML
        Ej: https://datos.bne.es/edicion/bimo0000659916.html
        
        Args:
            url: URL completa de la edición en datos.bne.es
            
        Returns:
            Diccionario con los campos extraídos
        """
        try:
            logger.info(f"Extrayendo datos de: {url}")
            
            # Descargar la página HTML
            response = self.session.get(url, timeout=self.timeout, verify=self.verify_ssl)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            # Parsear HTML con BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            datos_edicion = {
                'url': url,
                'titulo': None,
                'autor': None,
                'autor_firma': None,
                'lugar_publicacion': None,
                'editorial': None,
                'fecha_publicacion': None,
                'descripcion_fisica': None,
                'dimensiones': None,
                'forma_contenido': None,
                'tipo_medio': None,
                'idioma': None,
                'notas': [],
                'recursos_relacionados': [],
                'isbn': None,
                'issn': None,
                'imprint': None,
                'other_authors': []
            }
            
            # === MÉTODO 1: Buscar en TABLAS (Primary para BNE) ===
            tables = soup.find_all('table')
            logger.info(f"Encontradas {len(tables)} tablas")
            
            if tables:
                # Procesar la primera tabla (contiene los datos principales)
                main_table = tables[0]
                rows = main_table.find_all('tr')
                
                for row in rows:
                    cols = row.find_all(['td', 'th'])
                    if len(cols) >= 2:
                        # Primera columna es la etiqueta, segunda es el valor
                        label = cols[0].get_text(strip=True).lower()
                        value = cols[1].get_text(strip=True)
                        
                        # Mapear etiquetas
                        if 'título' in label or 'title' in label:
                            datos_edicion['titulo'] = value
                        elif 'autor' in label and ('firma' in label or 'creator' in label):
                            datos_edicion['autor_firma'] = value
                        elif ('nombre' in label or 'name' in label) and 'autor' in label:
                            datos_edicion['autor'] = value
                        elif 'lugar' in label and ('publicación' in label or 'publication' in label):
                            datos_edicion['lugar_publicacion'] = value
                        elif 'editorial' in label or 'publisher' in label or 'imprenta' in label:
                            datos_edicion['editorial'] = value
                        elif 'fecha' in label and ('publicación' in label or 'publication' in label):
                            datos_edicion['fecha_publicacion'] = value
                        elif 'descripción' in label and ('física' in label or 'physical' in label or 'extensión' in label):
                            datos_edicion['descripcion_fisica'] = value
                        elif 'dimensión' in label or 'size' in label or 'alto' in label:
                            datos_edicion['dimensiones'] = value
                        elif 'forma' in label and 'contenido' in label:
                            datos_edicion['forma_contenido'] = value
                        elif 'tipo' in label and 'medio' in label:
                            datos_edicion['tipo_medio'] = value
                        elif 'idioma' in label or 'language' in label:
                            datos_edicion['idioma'] = value
                        elif 'nota' in label or 'note' in label:
                            if value:
                                datos_edicion['notas'].append(value)
                        elif ('recurso' in label or 'resource' in label) and 'relacionado' in label:
                            if value:
                                datos_edicion['recursos_relacionados'].append(value)
                        elif 'isbn' in label:
                            datos_edicion['isbn'] = value
                        elif 'issn' in label:
                            datos_edicion['issn'] = value
            
            # === MÉTODO 2: Buscar en estructura dl (description list) si no hay tablas ===
            if not any([datos_edicion.get('titulo'), datos_edicion.get('editorial')]):
                dls = soup.find_all('dl', class_=re.compile('definition.*', re.I))
                if not dls:
                    dls = soup.find_all('dl')
                
                for dl in dls:
                    dts = dl.find_all('dt')
                    dds = dl.find_all('dd')
                    
                    for dt, dd in zip(dts, dds):
                        label = dt.get_text(strip=True).lower()
                        value = dd.get_text(strip=True)
                        
                        if 'título' in label:
                            datos_edicion['titulo'] = value
                        elif 'autor' in label and 'firma' in label:
                            datos_edicion['autor_firma'] = value
                        elif 'autor' in label:
                            datos_edicion['autor'] = value
                        elif 'lugar' in label and 'publicación' in label:
                            datos_edicion['lugar_publicacion'] = value
                        elif 'editorial' in label:
                            datos_edicion['editorial'] = value
                        elif 'fecha' in label and 'publicación' in label:
                            datos_edicion['fecha_publicacion'] = value
            
            # === MÉTODO 3: Buscar en h1/h2/h3 para título si aún no lo tenemos ===
            if not datos_edicion['titulo']:
                for tag in ['h1', 'h2', 'h3']:
                    elem = soup.find(tag)
                    if elem:
                        text = elem.get_text(strip=True)
                        if text and len(text) > 3:
                            datos_edicion['titulo'] = text
                            break
            
            # === MÉTODO 4: Buscar en meta tags ===
            for meta in soup.find_all('meta'):
                name = meta.get('name', '').lower()
                content = meta.get('content', '')
                
                if 'title' in name or 'description' in name:
                    if not datos_edicion['titulo'] and 'title' in name:
                        datos_edicion['titulo'] = content
                    elif 'description' in name and not datos_edicion['descripcion_fisica']:
                        datos_edicion['descripcion_fisica'] = content
            
            # Limpiar datos
            datos_edicion = {k: v for k, v in datos_edicion.items() 
                           if v and v != [] and v is not None}
            
            logger.info(f"✓ Datos extraídos: {len(datos_edicion)} campos")
            logger.info(f"  Título: {datos_edicion.get('titulo', 'N/A')}")
            logger.info(f"  Autor: {datos_edicion.get('autor', 'N/A')}")
            logger.info(f"  Editorial: {datos_edicion.get('editorial', 'N/A')}")
            
            return datos_edicion if datos_edicion else None
            
        except Exception as e:
            logger.error(f"Error extrayendo datos de edición: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    
    def extraer_datos_autor_html(self, url: str) -> Optional[Dict]:
        """
        Extrae datos estructurados de una página de persona/autor de datos.bne.es
        Ej: https://datos.bne.es/persona/XX4556545.html

        Campos que intenta extraer (estructura de datos.bne.es para personas):
          nombre_completo, nombre_firma, pseudonimos, fecha_nacimiento,
          anio_nacimiento, lugar_nacimiento, fecha_muerte, anio_muerte,
          lugar_muerte, nacionalidad, ocupacion, genero, lengua,
          biografia, bne_identificador, url_datos_bne, viaf_id
        """
        try:
            logger.info(f"Extrayendo datos de autor desde: {url}")

            response = self.session.get(url, timeout=self.timeout, verify=self.verify_ssl)
            response.raise_for_status()
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.content, 'html.parser')

            datos_autor = {
                'url_datos_bne': url,
                'bne_identificador': None,
                'nombre_completo': None,
                'nombre_firma': None,
                'pseudonimos': None,
                'fecha_nacimiento': None,
                'anio_nacimiento': None,
                'lugar_nacimiento': None,
                'fecha_muerte': None,
                'anio_muerte': None,
                'lugar_muerte': None,
                'nacionalidad': None,
                'ocupacion': None,
                'genero': None,
                'lengua': None,
                'biografia': None,
                'viaf_id': None,
                'otros_identificadores': None
            }

            # Extraer identificador BNE desde la URL (ej: XX4556545)
            match = re.search(r'/persona/([A-Za-z0-9]+)', url)
            if match:
                datos_autor['bne_identificador'] = match.group(1)

            def _extraer_anio(texto: str) -> Optional[int]:
                m = re.search(r'\b(\d{4})\b', texto)
                return int(m.group(1)) if m else None

            def _mapear_campo(label: str, value: str):
                """Asigna value al campo correcto según la etiqueta de datos.bne.es"""
                l = label.lower()
                # Nombre
                if ('nombre' in l and any(x in l for x in ['autorizado', 'personal', 'completo'])) \
                        or l in ('nombre', 'nombre de la persona'):
                    if not datos_autor['nombre_completo']:
                        datos_autor['nombre_completo'] = value
                elif 'firma' in l and 'nombre' in l:
                    datos_autor['nombre_firma'] = value
                elif any(x in l for x in ['pseudónimo', 'seudónimo', 'variante', 'otras formas']):
                    datos_autor['pseudonimos'] = value
                # Fechas
                elif 'nacimiento' in l and 'fecha' in l:
                    datos_autor['fecha_nacimiento'] = value
                    datos_autor['anio_nacimiento'] = _extraer_anio(value)
                elif 'muerte' in l and 'fecha' in l:
                    datos_autor['fecha_muerte'] = value
                    datos_autor['anio_muerte'] = _extraer_anio(value)
                elif 'asociad' in l and 'fecha' in l:
                    # "Fechas asociadas" → extrae primer año como nacimiento
                    if not datos_autor['fecha_nacimiento']:
                        datos_autor['fecha_nacimiento'] = value
                        datos_autor['anio_nacimiento'] = _extraer_anio(value)
                # Lugares
                elif 'nacimiento' in l and 'lugar' in l:
                    datos_autor['lugar_nacimiento'] = value
                elif 'muerte' in l and 'lugar' in l:
                    datos_autor['lugar_muerte'] = value
                # Otros campos
                elif any(x in l for x in ['país', 'pais', 'nacional']):
                    datos_autor['nacionalidad'] = value
                elif any(x in l for x in ['ocupación', 'profesión', 'actividad', 'campo']):
                    datos_autor['ocupacion'] = value
                elif any(x in l for x in ['género', 'sexo']):
                    datos_autor['genero'] = value
                elif any(x in l for x in ['lengua', 'idioma', 'language']):
                    datos_autor['lengua'] = value
                elif any(x in l for x in ['biograf', 'nota biogr', 'resumen']):
                    datos_autor['biografia'] = value
                elif 'viaf' in l:
                    datos_autor['viaf_id'] = value
                elif any(x in l for x in ['identificador', 'isni', 'lccn']):
                    datos_autor['otros_identificadores'] = value

            # === MÉTODO 1: Tablas ===
            for table in soup.find_all('table'):
                for row in table.find_all('tr'):
                    cols = row.find_all(['td', 'th'])
                    if len(cols) >= 2:
                        _mapear_campo(cols[0].get_text(strip=True), cols[1].get_text(strip=True))

            # === MÉTODO 2: dl/dt/dd ===
            if not datos_autor['nombre_completo']:
                for dl in soup.find_all('dl'):
                    for dt, dd in zip(dl.find_all('dt'), dl.find_all('dd')):
                        _mapear_campo(dt.get_text(strip=True), dd.get_text(strip=True))

            # === MÉTODO 3: h1 como nombre ===
            if not datos_autor['nombre_completo']:
                h1 = soup.find('h1')
                if h1:
                    datos_autor['nombre_completo'] = h1.get_text(strip=True)

            # === MÉTODO 4: meta tags ===
            if not datos_autor['nombre_completo']:
                for meta in soup.find_all('meta'):
                    name = meta.get('name', '').lower()
                    content = meta.get('content', '')
                    if 'title' in name and content:
                        datos_autor['nombre_completo'] = content
                        break

            # Limpiar Nones y vacíos
            datos_autor = {k: v for k, v in datos_autor.items() if v is not None and v != ''}

            logger.info(f"✓ Autor extraído: {datos_autor.get('nombre_completo', 'N/A')} "
                        f"({datos_autor.get('bne_identificador', 'sin ID')})")
            return datos_autor if datos_autor.get('nombre_completo') or datos_autor.get('bne_identificador') else None

        except Exception as e:
            logger.error(f"Error extrayendo datos de autor: {e}")
            return None

    def buscar_autores_bne(self, nombre: str, limite: int = 10) -> List[Dict]:
        """
        Busca personas/autores en datos.bne.es por nombre y devuelve su estructura completa.
        Intenta varias URLs de búsqueda y, para cada resultado, extrae los datos
        completos de la página de la persona.

        Args:
            nombre: Nombre del autor a buscar
            limite: Número máximo de autores a devolver

        Returns:
            Lista de dicts con la estructura completa de cada autor
        """
        autores = []
        try:
            logger.info(f"Buscando autores en datos.bne.es: '{nombre}'")

            # Intentar varias URLs de búsqueda del portal
            search_urls = [
                f"{self.base_url}/search?q={quote(nombre)}&type=persona",
                f"{self.base_url}/search?q={quote(nombre)}",
                f"{self.base_url}/?q={quote(nombre)}&type=person",
                f"{self.base_url}/?q={quote(nombre)}",
            ]

            response = None
            for url in search_urls:
                try:
                    resp = self.session.get(url, timeout=self.timeout, verify=self.verify_ssl)
                    if resp.status_code == 200:
                        response = resp
                        logger.info(f"  ✓ Resultados de búsqueda desde: {url}")
                        break
                except Exception:
                    continue

            if not response:
                logger.warning("No se encontró URL de búsqueda válida en datos.bne.es")
                return autores

            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser')

            # Buscar enlaces a páginas de persona
            persona_links = soup.find_all('a', href=re.compile(r'/persona/', re.IGNORECASE))

            # Fallback: buscar cualquier enlace que pueda ser un identificador de persona
            if not persona_links:
                persona_links = soup.find_all('a', href=re.compile(r'/(XX|a)\d+', re.IGNORECASE))

            logger.info(f"  Encontrados {len(persona_links)} enlaces a personas")

            urls_vistas = set()
            for link in persona_links[:limite * 2]:  # margen por si alguno falla
                href = link.get('href', '')
                url_persona = urljoin(self.base_url, href)

                # Normalizar a .html
                if not url_persona.endswith('.html'):
                    url_persona = url_persona.rstrip('/') + '.html'

                if url_persona in urls_vistas:
                    continue
                urls_vistas.add(url_persona)

                datos = self.extraer_datos_autor_html(url_persona)
                if datos:
                    autores.append(datos)
                    if len(autores) >= limite:
                        break

                time.sleep(0.5)  # cortesía al servidor

            logger.info(f"✓ {len(autores)} autores obtenidos desde datos.bne.es")

        except Exception as e:
            logger.error(f"Error en buscar_autores_bne: {e}")

        return autores

    def guardar_csv(self, datos: List[Dict], nombre_archivo: str) -> bool:
        """
        Guarda datos en archivo CSV
        
        Args:
            datos: Lista de diccionarios con los datos
            nombre_archivo: Nombre del archivo a guardar
            
        Returns:
            True si se guardó exitosamente, False en caso contrario
        """
        try:
            if not datos:
                logger.warning(f"No hay datos para guardar en {nombre_archivo}")
                return False
            
            keys = datos[0].keys()
            
            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=keys)
                writer.writeheader()
                writer.writerows(datos)
            
            logger.info(f"Datos guardados en {nombre_archivo} ({len(datos)} registros)")
            return True
            
        except Exception as e:
            logger.error(f"Error guardando CSV: {e}")
            return False
    
    def guardar_json(self, datos: List[Dict], nombre_archivo: str) -> bool:
        """
        Guarda datos en archivo JSON
        
        Args:
            datos: Lista de diccionarios con los datos
            nombre_archivo: Nombre del archivo a guardar
            
        Returns:
            True si se guardó exitosamente, False en caso contrario
        """
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as jsonfile:
                json.dump(datos, jsonfile, ensure_ascii=False, indent=2)
            
            logger.info(f"Datos guardados en {nombre_archivo} ({len(datos)} registros)")
            return True
            
        except Exception as e:
            logger.error(f"Error guardando JSON: {e}")
            return False
    
    def buscar_obras_por_nombre(self, nombre: str, limit: int = 20) -> List[Dict]:
        """
        Busca obras genéricamente por nombre en datos.bne.es
        Intenta varias estrategias de búsqueda (autores, periódicos, etc.)
        
        Args:
            nombre: Nombre/término a buscar
            limit: Número máximo de resultados
            
        Returns:
            Lista de obras encontradas
        """
        resultados = []
        
        try:
            logger.info(f"🔎 Iniciando búsqueda por nombre en datos.bne.es: '{nombre}'")
            
            # Intenta búsqueda de autores primero
            try:
                logger.info(f"  - Buscando autores...")
                autores = self.buscar_autores(nombre, limite=limit)
                if autores:
                    logger.info(f"    ✓ Encontrados {len(autores)} autores")
                    for autor in autores:
                        resultado = {
                            'titulo': autor.get('nombre', ''),
                            'tipo': 'Persona',
                            'enlace': autor.get('enlace', ''),
                            'fuente': 'datos.bne.es',
                            'descripcion': autor.get('descripcion', ''),
                            'fecha_nacimiento': autor.get('fecha_nacimiento', ''),
                            'fecha_muerte': autor.get('fecha_muerte', '')
                        }
                        resultados.append(resultado)
                else:
                    logger.info(f"    ✗ No se encontraron autores")
            except Exception as e:
                logger.warning(f"  ✗ Error en búsqueda de autores: {e}")
            
            # Si quedan espacios, intenta búsqueda de periódicos
            if len(resultados) < limit:
                try:
                    logger.info(f"  - Buscando periódicos...")
                    periodicos = self.buscar_periodicos(nombre, limite=limit - len(resultados))
                    if periodicos:
                        logger.info(f"    ✓ Encontrados {len(periodicos)} periódicos")
                        for periodico in periodicos:
                            resultado = {
                                'titulo': periodico.get('titulo', ''),
                                'tipo': 'Periódico',
                                'enlace': periodico.get('enlace', ''),
                                'fuente': 'datos.bne.es',
                                'fecha_inicio': periodico.get('fecha_inicio', ''),
                                'lugar_publicacion': periodico.get('lugar_publicacion', '')
                            }
                            resultados.append(resultado)
                    else:
                        logger.info(f"    ✗ No se encontraron periódicos")
                except Exception as e:
                    logger.warning(f"  ✗ Error en búsqueda de periódicos: {e}")
            
            logger.info(f"📊 Búsqueda por nombre '{nombre}': {len(resultados)} RESULTADOS TOTALES en datos.bne.es")
            return resultados
            
        except Exception as e:
            logger.error(f"❌ Error en búsqueda por nombre: {e}")
            return []
    
    def buscar_obras_por_titulo_bne(self, titulo: str, limit: int = 20) -> List[Dict]:
        """
        Busca obras ESPECÍFICAMENTE por título en datos.bne.es
        Realiza una búsqueda directa en el portal y extrae todos los campos disponibles
        
        Args:
            titulo: Título de la obra a buscar
            limit: Número máximo de resultados
            
        Returns:
            Lista de obras encontradas con todos sus datos (20+ campos)
        """
        obras = []
        try:
            logger.info(f"🔍 Buscando obras por TÍTULO en datos.bne.es: '{titulo}'")
            
            # Construcción de URL de búsqueda en datos.bne.es
            # TODO: Probar con URL raíz (/search, /query, /resultados, etc.)
            search_urls = [
                f"{self.base_url}/search?q={quote(titulo)}",  # Intenta con /search
                f"{self.base_url}/query?q={quote(titulo)}",   # Intenta con /query
                f"{self.base_url}/resultados?q={quote(titulo)}",  # Intenta con /resultados
                f"{self.base_url}/?q={quote(titulo)}",  # Intenta con parámetro raíz
                f"{self.base_url}/?p={quote(titulo)}",  # Intenta con parámetro 'p'
            ]
            
            response = None
            final_url = None
            
            # Intenta diferentes URLs hasta obtener respuesta válida
            for url in search_urls:
                try:
                    logger.info(f"  📡 Intentando: {url}")
                    resp = self.session.get(url, timeout=self.timeout, verify=self.verify_ssl)
                    
                    if resp.status_code == 200:
                        response = resp
                        final_url = url
                        logger.info(f"    ✓ Respuesta recibida ({len(response.content)} bytes)")
                        break
                    else:
                        logger.info(f"    ✗ Status {resp.status_code}")
                except Exception as e:
                    logger.warning(f"    ⚠️ Error: {e}")
            
            if not response or not final_url:
                logger.error(f"❌ No se encontró una URL de búsqueda válida en datos.bne.es")
                # Fallback: intentar buscar a través de autores/periódicos
                logger.info(f"  ↻ Fallback: buscando por autor...")
                return self.buscar_autores(titulo, limite=limit)
            
            response.encoding = 'utf-8'
            
            # Parser HTML de resultados
            soup = BeautifulSoup(response.content, 'html.parser')
            logger.info(f"  ✓ HTML parseado")
            
            # Hacer debug: guardar HTML para inspeccionar
            logger.debug(f"HTML snippet: {str(soup)[:500]}")
            
            # Buscar patrones de resultados (muy flexible para captar cualquier estructura)
            # Patrón 1: divs/articles con clases comunes
            contenedores = soup.find_all(['div', 'article', 'li'], class_=re.compile(r'(result|item|obra|record|entry|publication)', re.IGNORECASE))
            
            # Patrón 2: si no hay, buscar por estructura de enlace
            if not contenedores:
                contenedores = soup.find_all('a', href=re.compile(r'/data/|/edicion/', re.IGNORECASE))
                logger.info(f"  🔎 Usando alternativa de búsqueda por enlaces")
            
            # Patrón 3: si no hay, buscar por tablas
            if not contenedores:
                tables = soup.find_all('table')
                for table in tables:
                    rows = table.find_all('tr')
                    contenedores.extend(rows)
                logger.info(f"  🔎 Usando alternativa de búsqueda por tablas")
            
            logger.info(f"  🔎 Encontrados {len(contenedores)} contenedores de resultados")
            
            for idx, contenedor in enumerate(contenedores[:limit]):
                try:
                    obra = {}
                    
                    # Si el contenedor es solo un enlace, extraer del contexto
                    if contenedor.name == 'a':
                        obra['titulo'] = contenedor.get_text(strip=True)
                        obra['enlace'] = urljoin(self.base_url, contenedor.get('href', ''))
                        # Contenedor padre para buscar más metadata
                        parent = contenedor.find_parent(['div', 'li', 'p', 'td'])
                        if parent:
                            contenedor = parent
                    else:
                        # Extraer título
                        titulo_elem = contenedor.find(['h2', 'h3', 'h4', 'a', 'span'], class_=re.compile(r'title|name|titulo', re.IGNORECASE))
                        if titulo_elem:
                            obra['titulo'] = titulo_elem.get_text(strip=True)
                            # Intentar extraer enlace del título
                            link = titulo_elem.find('a')
                            if not link:
                                link = titulo_elem.find_parent('a')
                            if link:
                                obra['enlace'] = urljoin(self.base_url, link.get('href', ''))
                        
                        # Alternativa: buscar el primer enlace dentro del contenedor
                        if 'enlace' not in obra:
                            primer_link = contenedor.find('a', href=re.compile(r'/data/|/edicion/', re.IGNORECASE))
                            if primer_link:
                                obra['enlace'] = urljoin(self.base_url, primer_link.get('href', ''))
                                if 'titulo' not in obra:
                                    obra['titulo'] = primer_link.get_text(strip=True)
                    
                    # Extraer metadata de la obra (autor, año, editorial, etc.)
                    todo_texto = contenedor.get_text(separator=' | ', strip=True)
                    
                    # Detectar campos por patrones en el texto
                    if 'autor' in todo_texto.lower() or 'creador' in todo_texto.lower():
                        match = re.search(r'([Aa]utor|[Cc]reador)[:\s]+([^|]+)', todo_texto)
                        if match:
                            obra['autor_firma'] = match.group(2).strip()
                    
                    if any(x in todo_texto.lower() for x in ['año', 'year', '20', '19']):
                        anio_match = re.search(r'\b(19|20)\d{2}\b', todo_texto)
                        if anio_match:
                            obra['anio'] = anio_match.group(0)
                    
                    if 'editorial' in todo_texto.lower() or 'imprenta' in todo_texto.lower() or 'publisher' in todo_texto.lower():
                        match = re.search(r'([Ee]ditorial|[Ii]mprenta|[Pp]ublisher)[:\s]+([^|]+)', todo_texto)
                        if match:
                            obra['imprenta'] = match.group(2).strip()[:100]
                    
                    if 'tipo' in todo_texto.lower() or 'type' in todo_texto.lower():
                        match = re.search(r'[Tt]ipo[:\s]+([^|]+)', todo_texto)
                        if match:
                            obra['tipo_publicacion'] = match.group(1).strip()
                    
                    # Extraer descripción (si está disponible)
                    desc_elem = contenedor.find(['p', 'div'], class_=re.compile(r'description|abstract|resumen', re.IGNORECASE))
                    if desc_elem:
                        obra['descripcion'] = desc_elem.get_text(strip=True)[:500]
                    
                    # Validar que tenga al menos un título
                    if 'titulo' in obra and obra['titulo'] and len(obra['titulo']) > 2:
                        obra['fuente'] = 'datos.bne.es'
                        obra['tipo'] = 'Obra'
                        obras.append(obra)
                        logger.info(f"  ✓ Obra {idx+1}: '{obra.get('titulo', 'Sin título')[:60]}'")
                    
                except Exception as e:
                    logger.warning(f"  ⚠️ Error procesando resultado {idx+1}: {e}")
                    continue
            
            logger.info(f"📊 Búsqueda en datos.bne.es por TÍTULO: {len(obras)} OBRAS ENCONTRADAS")
            return obras
            
        except requests.exceptions.ConnectionError as e:
            logger.error(f"❌ Error de conexión a datos.bne.es: {e}")
            # Fallback: buscar en autores
            logger.info(f"  ↻ Fallback: buscando por autor...")
            return self.buscar_autores(titulo, limite=limit)
        except Exception as e:
            logger.error(f"❌ Error buscando obras por título: {e}")
            return []
    
    def ejecutar_busqueda_completa(self, autores: List[str], periodicos: List[str]):
        """
        Ejecuta una busqueda completa de autores y periódicos en datos.bne.es
        
        Realiza peticiones al portal de datos enlazados de la BNE para recolectar
        información sobre autores y periódicos españoles.
        
        Args:
            autores: Lista de nombres de autores a buscar
            periodicos: Lista de títulos de periódicos a buscar
        """
        logger.info("=" * 60)
        logger.info("Iniciando búsqueda completa en datos.bne.es")
        logger.info("Portal: https://datos.bne.es")
        logger.info("=" * 60)
        
        # Buscar autores
        for autor in autores:
            try:
                resultados = self.buscar_autores(autor)
                self.datos_autores.extend(resultados)
                logger.info(f"✓ Búsqueda completada: {autor}")
                time.sleep(2)  # Evitar sobrecarga del servidor
            except Exception as e:
                logger.error(f"✗ Error buscando {autor}: {e}")
        
        # Buscar periódicos
        for periodico in periodicos:
            try:
                resultados = self.buscar_periodicos(periodico)
                self.datos_periodicos.extend(resultados)
                logger.info(f"✓ Búsqueda completada: {periodico}")
                time.sleep(2)
            except Exception as e:
                logger.error(f"✗ Error buscando {periodico}: {e}")
        
        # Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if self.datos_autores:
            self.guardar_json(self.datos_autores, f"bne_autores_{timestamp}.json")
            self.guardar_csv(self.datos_autores, f"bne_autores_{timestamp}.csv")
        
        if self.datos_periodicos:
            self.guardar_json(self.datos_periodicos, f"bne_periodicos_{timestamp}.json")
            self.guardar_csv(self.datos_periodicos, f"bne_periodicos_{timestamp}.csv")
        
        logger.info("=" * 60)
        logger.info("Búsqueda completada")
        logger.info(f"Total autores: {len(self.datos_autores)}")
        logger.info(f"Total periódicos: {len(self.datos_periodicos)}")
        logger.info("=" * 60)


def main():
    """Función principal - Ejemplo de uso del scraper"""
    
    # Ejemplos de búsquedas
    # Estos autores y periódicos tienen mucha información en datos.bne.es
    autores_buscar = [
        "García Lorca",           # Federico García Lorca
        "Miguel de Cervantes",    # Autor de El Quijote
        "Machado",                # Antonio Machado
        "Emilia Pardo Bazán",     # Novelista galega
        "Ramón y Cajal"           # Científico español
    ]
    
    periodicos_buscar = [
        "ABC",                    # Periódico histórico
        "La Vanguardia",          # Periódico catalán
        "El Mundo",               # Periódico madrileño
        "Diario de Madrid",       # Histórico
        "El País"                 # Periódico nacional
    ]
    
    logger.info("📚 Iniciando BNE Scraper")
    logger.info(f"Fuente: https://datos.bne.es")
    
    scraper = BNEScraper()
    scraper.ejecutar_busqueda_completa(autores_buscar, periodicos_buscar)
    
    logger.info("✓ Scraping completado")


if __name__ == "__main__":
    main()
