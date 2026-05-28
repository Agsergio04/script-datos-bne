import logging
from datetime import datetime
from flask import Blueprint, jsonify, request
from extensions import db
from models import Obra, Autor, Usuario, Proyecto
from services.scraper import scraper

bp = Blueprint("datasets", __name__)
logger = logging.getLogger(__name__)


@bp.route('/api/buscar-datasets/kaggle', methods=['POST'])
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
