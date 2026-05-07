# 🔙 Backend - Guía de Desarrollo

## Estructura del Backend

```
backend/
├── app.py                  # Aplicación Flask principal (API REST)
├── bne_scraper.py          # Scraper para datos.bne.es
├── scraper_config.ini      # Configuración del scraper
├── Dockerfile              # Imagen Docker
├── requirements.txt        # Dependencias Python
└── tests/                  # Tests unitarios (futuro)
```

## 🚀 Inicio Rápido

### Opción 1: Con Docker

```bash
# Desde la carpeta raíz del proyecto
docker-compose up -d backend

# Ver logs en vivo
docker-compose logs -f backend

# Acceder a la API
curl http://localhost:5000/api/info
```

### Opción 2: Desarrollo Local

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar (Windows)
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r backend/requirements.txt

# 4. Configurar base de datos
# Asegúrate de que PostgreSQL está corriendo

# 5. Ejecutar aplicación
python app.py

# 6. Probar API
curl http://localhost:5000/api/info
```

---

## 🌐 API REST Endpoints

### Verificación

```bash
# Health check
curl http://localhost:5000/health

# Versión
curl http://localhost:5000/api/version

# Información del proyecto
curl http://localhost:5000/api/info
```

### Gestión de Obras

```bash
# Listar obras
curl "http://localhost:5000/api/obras?page=1&per_page=10"

# Filtrar por tipo
curl "http://localhost:5000/api/obras?tipo=Novela"

# Filtrar por autor
curl "http://localhost:5000/api/obras?autor=Cervantes"

# Obtener obra específica
curl http://localhost:5000/api/obras/1

# Crear nueva obra (POST)
curl -X POST http://localhost:5000/api/obras \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Nueva Obra",
    "tipo_publicacion": "Novela",
    "nombre_autor": "Autor Nombre",
    "anio": 2024
  }'

# Actualizar obra (PUT)
curl -X PUT http://localhost:5000/api/obras/1 \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Nuevo Título"}'

# Eliminar obra (DELETE)
curl -X DELETE http://localhost:5000/api/obras/1
```

### Estadísticas

```bash
# Resumen general
curl http://localhost:5000/api/estadisticas/resumen
```

### Búsqueda

```bash
# Búsqueda global (mínimo 3 caracteres)
curl "http://localhost:5000/api/buscar?q=Quijote"
```

---

## 🔍 Scraper - Extracción de Datos

### Ejecutar Scraper

```bash
# Desde la carpeta backend
python bne_scraper.py

# Genera archivos:
# - bne_autores_YYYYMMDD_HHMMSS.json
# - bne_autores_YYYYMMDD_HHMMSS.csv
# - bne_periodicos_YYYYMMDD_HHMMSS.json
# - bne_periodicos_YYYYMMDD_HHMMSS.csv
```

### Script Personalizado

```python
#!/usr/bin/env python
from bne_scraper import BNEScraper

# Crear scraper
scraper = BNEScraper()

# Búsquedas personalizadas
autores = ["García Lorca", "Machado"]
periodicos = ["ABC", "La Vanguardia"]

# Ejecutar
scraper.ejecutar_busqueda_completa(autores, periodicos)
```

### Integración con BD

Los datos exportados por el scraper pueden importarse a la BD:

```python
import json
from app import db, Obra

# Cargar datos
with open('bne_autores_20240414_103000.json') as f:
    autores = json.load(f)

# Importar a BD
for autor in autores:
    obra = Obra(
        nombre_autor=autor['nombre'],
        enlace=autor['enlace'],
        # ... otros campos
    )
    db.session.add(obra)

db.session.commit()
```

---

## 📊 Estructura de Datos

### Modelo Obra (app.py)

```python
class Obra(db.Model):
    id_obra = db.Column(db.BigInteger, primary_key=True)
    titulo = db.Column(db.String(500), nullable=False)
    tipo_publicacion = db.Column(db.String(100))
    nombre_autor = db.Column(db.String(255))
    anio = db.Column(db.Integer)
    enlace = db.Column(db.Text, unique=True)
    # ... más campos
```

---

## 🧪 Testing

```bash
# Ejecutar tests (instalado con pytest)
pytest

# Con cobertura
pytest --cov=backend

# Solo tests del scraper
pytest tests/test_scraper.py
```

---

## 🔧 Configuración

### Variables de Entorno (.env)

```env
FLASK_ENV=development
FLASK_APP=app.py
DATABASE_URL=postgres://bne_user:password@localhost:5432/bne_db
SECRET_KEY=dev_secret_key
SQLALCHEMY_TRACK_MODIFICATIONS=False
```

### Configuración del Scraper (scraper_config.ini)

```ini
[FUENTE]
portal = https://datos.bne.es

[OPCIONES_BUSQUEDA]
limite_resultados = 50
timeout_segundos = 30

[AUTORES]
autores = ["García Lorca", "Machado", ...]

[PERIODICOS]
periodicos = ["ABC", "La Vanguardia", ...]
```

---

## 📈 Desarrollo

### Agregar Nuevo Endpoint

```python
@app.route('/api/nuevo', methods=['GET'])
def nuevo_endpoint():
    """Documentación del endpoint"""
    try:
        # Lógica aquí
        return jsonify({'resultado': 'éxito'}), 200
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
```

### Agregar Nuevo Modelo

```python
class NuevoModelo(db.Model):
    __tablename__ = 'nuevo_modelo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    
    def to_dict(self):
        return {'id': self.id, 'nombre': self.nombre}
```

---

## 🐛 Debugging

### Modo Debug de Flask

```bash
export FLASK_ENV=development
python app.py

# O windows:
set FLASK_ENV=development
python app.py
```

### Logs en Consola

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Mensaje de información")
logger.warning("Mensaje de advertencia")
logger.error("Mensaje de error")
```

### Inspeccionar Base de Datos

```bash
# Acceder a PostgreSQL
psql -U bne_user -d bne_db

# Listar tablas
\dt

# Ver schema
\d obra

# Consultas útiles
SELECT COUNT(*) FROM obra;
SELECT * FROM obra LIMIT 5;
```

---

## 📦 Dependencias

Ver `requirements.txt` para lista completa:

- **Flask:** Framework web
- **SQLAlchemy:** ORM para BD
- **Psycopg2:** Driver PostgreSQL
- **Requests:** Cliente HTTP (scraper)
- **Pytest:** Testing
- **Pandas:** Procesamiento de datos

---

## 🚀 Deployment

### Producción con Gunicorn

```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar con 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Con archivo de configuración
gunicorn --config gunicorn_config.py app:app
```

### Con Docker

```bash
docker build -t bne-backend -f backend/Dockerfile .
docker run -p 5000:5000 bne-backend
```

---

## 📞 Ayuda y Recursos

- **Flask Docs:** https://flask.palletsprojects.com/
- **SQLAlchemy Docs:** https://docs.sqlalchemy.org/
- **datos.bne.es:** https://datos.bne.es
- **BNE Datos Enlazados:** https://www.bne.es/es/catalogos/datos-enlazados-bne

---

**Versión:** 1.0.0
**Última actualización:** 14 de abril de 2026
