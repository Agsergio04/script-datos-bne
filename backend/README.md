# Backend — Guía de Desarrollo

API REST en Flask con estructura modular siguiendo principios **SOLID**.

## Estructura

```
backend/
├── app.py               Factory: crea la app y registra blueprints
├── config.py            Configuración (Config)
├── extensions.py        db = SQLAlchemy()  (sin app → evita imports circulares)
├── bne_scraper.py       Cliente HTTP/scraper de datos.bne.es
├── models/              Capa de datos (un archivo por entidad)
│   ├── __init__.py      Reexporta los modelos (registra en SQLAlchemy)
│   ├── autor.py         class Autor
│   ├── obra.py          class Obra (+ to_dict_detallado)
│   ├── usuario.py       class Usuario
│   └── proyecto.py      class Proyecto
├── services/            Lógica externa compartida
│   └── scraper.py       Instancia única de BNEScraper
├── blueprints/          Capa HTTP, agrupada por recurso (Single Responsibility)
│   ├── health.py        /health, /api/version, /api/info
│   ├── obras.py         CRUD de obras + /api/periodicos/rango-fechas
│   ├── autores.py       CRUD de autores
│   ├── importar.py      /api/importar/url|titulo|nombre|lote|edicion/html|autores
│   ├── estadisticas.py  /api/estadisticas/resumen + /api/buscar
│   └── datasets.py      /api/buscar-datasets/kaggle
├── requirements.txt     Dependencias de producción
├── requirements-dev.txt Mínimas para correr la API en local (sin pandas/numpy)
└── Dockerfile
```

### Decisiones SOLID

| Principio | Aplicación |
|---|---|
| **Single Responsibility** | Config, extensiones, modelos, servicios y rutas, cada uno en su módulo. |
| **Open/Closed** | Añadir un recurso = crear un blueprint y registrarlo en `app.py`, sin tocar el resto. |
| **Dependency Inversion** | Los blueprints dependen de abstracciones (`extensions.db`, `services.scraper`), no de implementaciones concretas. |
| **Interface Segregation** | Cada blueprint expone solo los endpoints de su recurso; el frontend solo importa lo que necesita. |

## Arranque rápido

### Con Docker (recomendado)
```bash
docker compose up -d db backend
docker compose logs -f backend
curl http://localhost:5000/api/info
```

### En local (Python 3.11+ y BD en Docker)
```bash
docker compose up -d db                 # solo la BD
cd backend
python -m venv venv && venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt     # minimas; no compila pandas/numpy
python app.py                           # ⇒ http://localhost:5000
```

Por defecto `DATABASE_URL = postgresql+psycopg2://bne_user:bne_password_123@localhost:5432/bne_db`, que apunta a la BD que Docker expone en `localhost:5432`. Sobreescribe con `$env:DATABASE_URL = "..."` si hace falta.

## Endpoints

### Salud
```http
GET /health
GET /api/version
GET /api/info
```

### Obras  ([blueprints/obras.py](blueprints/obras.py))
```http
GET    /api/obras?page=&per_page=&tipo=&autor=&tema=&anio=&fecha_desde=&fecha_hasta=
GET    /api/obras/<id>
GET    /api/obras/<id>/detallada
POST   /api/obras
PUT    /api/obras/<id>          # actualiza cualquier campo, incl. imagen_url (imagen manual)
DELETE /api/obras/<id>
GET    /api/periodicos/rango-fechas?fecha_desde=&fecha_hasta=
```

### Autores  ([blueprints/autores.py](blueprints/autores.py))
```http
GET    /api/autores?page=&per_page=&nombre=&nacionalidad=&ocupacion=
GET    /api/autores/<id>        # incluye sus obras
POST   /api/autores
PUT    /api/autores/<id>
DELETE /api/autores/<id>
```

### Importación  ([blueprints/importar.py](blueprints/importar.py))
```http
POST /api/importar/url          # {"url": "https://datos.bne.es/..."}   (.html → extractor HTML)
POST /api/importar/titulo       # {"titulo": "Quijote"}
POST /api/importar/nombre       # {"nombre": "Quijote", "limite": 20}
POST /api/importar/lote         # {"obras": [{"url": "..."}, {"titulo": "..."}, ...]}
POST /api/importar/edicion/html # {"url": "https://datos.bne.es/edicion/...html"}
POST /api/importar/autores      # {"nombre": "..."}  ó  {"url": "https://datos.bne.es/persona/...html"}
```

### Estadísticas y búsqueda  ([blueprints/estadisticas.py](blueprints/estadisticas.py))
```http
GET /api/estadisticas/resumen   # {"resumen": {total_obras, autores_principales, obras_por_tipo}}
GET /api/buscar?q=&detallada=
```

### Kaggle  ([blueprints/datasets.py](blueprints/datasets.py))
```http
POST /api/buscar-datasets/kaggle
```

## Scraper (`bne_scraper.py`)

Cliente HTTP de datos.bne.es. Métodos clave:

- `extraer_datos_edicion_html(url)` — parsea cualquier página HTML de datos.bne.es (`/edicion/`, `/obra/`, `/resource/`) y extrae título, autor, editorial, lugar, fecha, **imagen** (portada digitalizada BDH validada y en HTTPS), etc.
- `buscar_obras_por_titulo_bne(titulo, limit)` — busca obras por título en datos.bne.es.
- `buscar_prensa_bne(termino, limite)` — usa el filtro real `find/resultados/?resourceType=Prensa+y+revistas`.
- `extraer_datos_autor_html(url)` — parsea `/persona/...html`.
- `buscar_autores_bne(nombre, limite)` — busca personas en datos.bne.es.

### Estrategia de extracción de imagen

`_extraer_imagen_principal` (helper interno):
1. Prioriza la **portada digitalizada** (`low.raw`/`high.raw` del servidor BDH).
2. Cae a `og:image` / `twitter:image` solo si parecen imágenes reales.
3. Descarta el *chrome* del sitio (logo de marca, `/img/`, iconos, sprites).
4. Normaliza http→https en hosts `bne.es` (evita *mixed-content*).
5. Si no encuentra imagen válida, devuelve `None` → la UI muestra el placeholder.

## Modelos

Cada modelo en `models/<entidad>.py` con header:
```python
from datetime import datetime
from extensions import db

class Mi(db.Model):
    __tablename__ = 'mi'
    ...
```
Y reexportado en `models/__init__.py` para que `db.create_all()` los registre.

## Cómo añadir un endpoint o blueprint nuevo

1. Si el recurso ya existe, añade `@bp.route(...)` en el blueprint correspondiente.
2. Si es nuevo, crea `blueprints/<recurso>.py`:
   ```python
   import logging
   from flask import Blueprint, jsonify, request
   from extensions import db
   from models import Obra
   
   bp = Blueprint('<recurso>', __name__)
   logger = logging.getLogger(__name__)
   
   @bp.route('/api/<recurso>', methods=['GET'])
   def listar():
       ...
   ```
3. Regístralo en `app.py` añadiéndolo a la tupla `BLUEPRINTS`.

## Configuración

`config.py`:
```python
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '...localhost...')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key_change_in_production')
```
Variables de entorno en el `.env` de la raíz (no se commitea).

## Dependencias

- **producción** (`requirements.txt`): Flask, Flask-CORS, Flask-SQLAlchemy, SQLAlchemy, psycopg2-binary, requests, beautifulsoup4, pandas, numpy, kaggle, …
- **local mínimo** (`requirements-dev.txt`): sin pandas/numpy/kaggle (no los usa la API; pandas/numpy fallan al compilar en Python 3.13 si pip no encuentra wheels).

## Migraciones

En [bd/migrations/](../bd/migrations/):
- `001_initial_schema.sql` — esquema base
- `002_add_autor_table.sql` — tabla `autor` + FK en `obra` + vista
- `003_add_imagen_url.sql` — columnas `imagen_url` en `obra` y `autor`
- `004_paginas_a_500.sql` — amplía `obra.paginas` a `VARCHAR(500)`

Se aplican manualmente con `psql`:
```bash
docker compose exec -T db psql -U bne_user -d bne_db < bd/migrations/00X_xxx.sql
```
En un volumen limpio, `schema_optimized.sql` ya incluye todo.

---
**Última actualización:** 28 de mayo de 2026
