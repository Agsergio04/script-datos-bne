# 🔍 Scraper de Datos BNE - Guía Técnica

## Descripción

El scraper BNE permite extraer datos del portal **datos.bne.es** de la Biblioteca Nacional de España.

### Fuente de Datos

- **URL:** https://datos.bne.es
- **Tipo:** Portal de Linked Data (datos enlazados)
- **Formato:** RDF, JSON-LD, HTML
- **Licencia:** CC0 (Dominio público)

---

## 🏗️ Arquitectura del Scraper

```
┌────────────────────────────────────────┐
│         datos.bne.es                  │
│   (Portal de Linked Data)              │
│                                        │
│  - Búsqueda de personas                │
│  - Búsqueda de publicaciones           │
│  - Búsqueda de temas                   │
└────────────────────────────────────────┘
              ↓ HTTP Requests
┌────────────────────────────────────────┐
│       BNEScraper (Python)              │
│                                        │
│  Métodos principales:                  │
│  ├── buscar_autores()                  │
│  ├── buscar_periodicos()               │
│  ├── obtener_obras_autor()             │
│  ├── guardar_json()                    │
│  └── guardar_csv()                     │
└────────────────────────────────────────┘
              ↓ Datos
┌────────────────────────────────────────┐
│    Archivos exportados                 │
│                                        │
│  - bne_autores_YYYYMMDD.json          │
│  - bne_autores_YYYYMMDD.csv           │
│  - bne_periodicos_YYYYMMDD.json       │
│  - bne_periodicos_YYYYMMDD.csv        │
└────────────────────────────────────────┘
              ↓ INSERT
┌────────────────────────────────────────┐
│     PostgreSQL (bd/obra)               │
│                                        │
│  Estructura:                            │
│  - usuario                              │
│  - proyecto                             │
│  - obra                                 │
│  - periodico                            │
│  - teatro, novela, poesia               │
└────────────────────────────────────────┘
```

---

## 📖 Uso del Scraper

### Instalación

```bash
# Instalar dependencias
pip install -r backend/requirements.txt
```

### Uso Básico

#### 1. Ejecutar desde línea de comandos

```bash
cd backend
python bne_scraper.py
```

#### 2. Usar dentro de una aplicación Python

```python
from bne_scraper import BNEScraper

# Crear instancia
scraper = BNEScraper(base_url="https://datos.bne.es", timeout=30)

# Buscar un autor
autores = scraper.buscar_autores("García Lorca")
print(f"Se encontraron {len(autores)} registros")

# Guardar resultados
scraper.guardar_json(autores, "autores.json")
scraper.guardar_csv(autores, "autores.csv")
```

#### 3. Búsqueda completa

```python
autores = ["García Lorca", "Machado", "Cervantes"]
periodicos = ["ABC", "La Vanguardia"]

scraper.ejecutar_busqueda_completa(autores, periodicos)
# Genera 4 archivos: autores JSON+CSV, periódicos JSON+CSV
```

---

## 🔧 Métodos Disponibles

### `__init__(base_url, timeout)`

Inicializa el scraper.

```python
scraper = BNEScraper(
    base_url="https://datos.bne.es",
    timeout=30  # segundos
)
```

---

### `buscar_autores(nombre, limite)`

Busca autores por nombre en el portal.

```python
autores = scraper.buscar_autores("García Lorca", limite=50)

# Retorna lista de diccionarios:
# [
#   {
#     'nombre': 'Federico García Lorca',
#     'identificador': 'xyz123',
#     'url': 'https://...',
#     'tipo': 'Persona',
#     'fecha_nacimiento': '1898-06-05',
#     'fecha_muerte': '1936-08-19',
#     'enlace': 'https://datos.bne.es/...'
#   },
#   ...
# ]
```

---

### `buscar_periodicos(titulo, limite)`

Busca periódicos por título.

```python
periodicos = scraper.buscar_periodicos("ABC", limite=50)

# Retorna lista de diccionarios:
# [
#   {
#     'titulo': 'ABC',
#     'identificador': 'abc123',
#     'url': 'https://...',
#     'tipo': 'Periódico',
#     'fecha_inicio': '1903-01-01',
#     'fecha_fin': '2024-present',
#     'lugar_publicacion': 'Madrid',
#     'enlace': 'https://datos.bne.es/...'
#   },
#   ...
# ]
```

---

### `obtener_obras_autor(id_autor)`

Obtiene obras de un autor específico.

```python
obras = scraper.obtener_obras_autor("author123")

# Retorna lista de obras del autor
```

---

### `guardar_json(datos, nombre_archivo)`

Guarda datos en formato JSON.

```python
scraper.guardar_json(autores, "autores_2024.json")
# Genera: autores_2024.json con encoding UTF-8
```

---

### `guardar_csv(datos, nombre_archivo)`

Guarda datos en formato CSV.

```python
scraper.guardar_csv(autores, "autores_2024.csv")
# Genera: autores_2024.csv con encoding UTF-8
```

---

### `ejecutar_busqueda_completa(autores, periodicos)`

Ejecuta búsqueda completa y guarda resultados.

```python
autores = ["García Lorca", "Machado", "Cervantes"]
periodicos = ["ABC", "La Vanguardia", "El País"]

scraper.ejecutar_busqueda_completa(autores, periodicos)

# Genera 4 archivos:
# - bne_autores_20240414_103000.json
# - bne_autores_20240414_103000.csv
# - bne_periodicos_20240414_103000.json
# - bne_periodicos_20240414_103000.csv
```

---

## 📊 Estructura de Datos Retornados

### Autor

```json
{
  "nombre": "Federico García Lorca",
  "identificador": "XX123456",
  "url": "https://datos.bne.es/data/XX123456",
  "tipo": "Persona",
  "descripcion": "Escritor español (1898-1936)",
  "fecha_nacimiento": "1898-06-05",
  "fecha_muerte": "1936-08-19",
  "enlace": "https://datos.bne.es/persona/XX123456"
}
```

### Periódico

```json
{
  "titulo": "ABC",
  "identificador": "XX654321",
  "url": "https://datos.bne.es/data/XX654321",
  "tipo": "Periódico",
  "fecha_inicio": "1903-01-01",
  "fecha_fin": "present",
  "lugar_publicacion": "Madrid",
  "enlace": "https://datos.bne.es/publication/XX654321"
}
```

---

## ⚙️ Configuración

Editar `backend/scraper_config.ini`:

```ini
[OPCIONES_BUSQUEDA]
limite_resultados = 50
timeout_segundos = 30
reintentos = 3
espera_entre_peticiones = 2

[AUTORES]
autores = [lista de autores a buscar]

[PERIODICOS]
periodicos = [lista de periódicos a buscar]
```

---

## 🌐 Integración con API Flask

El scraper está integrado en la API Flask. Para usarlo desde HTTP:

```bash
# (Futuro) Iniciar scraping desde API
curl -X POST http://localhost:5000/api/scraper/start \
  -H "Content-Type: application/json" \
  -d '{
    "autores": ["García Lorca", "Machado"],
    "periodicos": ["ABC"]
  }'
```

---

## 📈 Manejo de Errores

El scraper incluye manejo robusto de errores:

```python
try:
    autores = scraper.buscar_autores("García Lorca")
except requests.RequestException as e:
    logger.error(f"Error de conexión: {e}")
except json.JSONDecodeError as e:
    logger.error(f"Error parseando JSON: {e}")
except Exception as e:
    logger.error(f"Error inesperado: {e}")
```

### Logs

Los errores se registran en:
- **Consola:** INFO, WARNING, ERROR
- **Archivo:** `bne_scraper.log`

---

## 🔐 Consideraciones de Seguridad

1. **Rate Limiting:** Se aplica delay de 2 segundos entre peticiones
2. **User-Agent:** Identificado como navegador legítimo
3. **Timeouts:** 30 segundos por defecto para evitar cuelgues
4. **Errores de Conexión:** Reintentos automáticos (configurables)

---

## 📊 Estructura de Exportación

### JSON

```json
[
  {
    "nombre": "García Lorca",
    "tipo": "Persona",
    ...
  },
  ...
]
```

### CSV

```csv
nombre,identificador,url,tipo,fecha_nacimiento,fecha_muerte,enlace
García Lorca,XX123456,https://...,Persona,1898-06-05,1936-08-19,https://...
```

---

## 🎯 Casos de Uso

### Caso 1: Búsqueda de Obras de un Autor

```python
# 1. Buscar autor
autores = scraper.buscar_autores("Miguel de Cervantes")
autor_id = autores[0]['identificador']

# 2. Obtener obras del autor
obras = scraper.obtener_obras_autor(autor_id)

# 3. Guardar
scraper.guardar_json(obras, "cervantes_obras.json")
```

### Caso 2: Exportación Completa de Periódicos

```python
periodicos = scraper.buscar_periodicos("", limite=100)
scraper.guardar_csv(periodicos, "todos_periodicos.csv")
```

### Caso 3: Importar a Base de Datos

```python
# 1. Scraping
autores = scraper.buscar_autores("García Lorca")

# 2. Guardar
scraper.guardar_json(autores, "autores.json")

# 3. Importar a BD (en app.py)
# INSERT INTO usuario (nombre, email) VALUES (...)
```

---

## 🚀 Optimizaciones

- **Caché:** Los resultados se guardan en JSON (reutilizable)
- **Batch Processing:** Procesa lotes de búsquedas
- **Async Requests:** (Futuro) Usar `aiohttp` para paralelización
- **Índices BD:** La BD tiene índices en campos de búsqueda

---

## 📞 Contacto y Recursos

- **Email BNE:** info.datosenlazados@bne.es
- **Portal:** https://datos.bne.es
- **Documentación:** https://www.bne.es/es/catalogos/datos-enlazados-bne
- **Licencia:** CC0 (Creative Commons Public Domain)

---

**Versión:** 1.0.0
**Última actualización:** 14 de abril de 2026
