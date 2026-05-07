# 📚 Proyecto BNE - Recogida de Datos

Plataforma integrada para recopilar, gestionar y analizar datos de autores y periódicos de la **Biblioteca Nacional de España (BNE)**.

## 🏗️ Estructura del Proyecto

```
Recogida de datos de BNE/
├── backend/                    # API y servicios Python/Flask
│   ├── Dockerfile             # Configuración Docker
│   ├── requirements.txt        # Dependencias Python
│   ├── bne_scraper.py         # Script principal de scraping
│   └── app.py                 # Aplicación Flask (por crear)
├── frontend/                   # Interfaz de usuario (por crear)
├── bd/                         # Base de datos PostgreSQL
│   ├── DataPrensa.sql         # Schema original
│   ├── schema_optimized.sql   # Schema mejorado con índices
│   ├── migrations/            # Scripts de migración
│   └── seeders/               # Datos de ejemplo
├── docs/                       # Documentación del proyecto
├── docker-compose.yml         # Orquestación de contenedores
├── .env.example               # Variables de entorno
└── README.md                  # Este archivo
```

## 🚀 Inicio Rápido

### Requisitos Previos

- Docker Desktop (v4.0+)
- Docker Compose (v1.29+)
- Python 3.11+ (para desarrollo local)
- PostgreSQL 18+ (si ejecutas localmente)

### Instalación

1. **Clonar o descargar el proyecto**

```bash
cd "Recogida de datos de BNE"
```

2. **Configurar variables de entorno**

```bash
cp .env.example .env
# Edita .env con tus configuraciones
```

3. **Iniciar con Docker Compose**

```bash
docker-compose up -d
```

Esto iniciará:
- 🗄️ **PostgreSQL 18** en `localhost:5432`
- 🔙 **Backend Flask** en `http://localhost:5000`
- 🎨 **Frontend** en `http://localhost:3000`
- 🛠️ **pgAdmin** en `http://localhost:5050`

4. **Verificar que todo funciona**

```bash
# Ver logs del backend
docker-compose logs backend

# Acceder a la BD
docker exec -it bne_database psql -U bne_user -d bne_db
```

## 📊 Base de Datos

### Esquema Principal

El proyecto utiliza PostgreSQL con las siguientes tablas principales:

| Tabla | Descripción |
|-------|-------------|
| `usuario` | Usuarios del sistema |
| `laboratorio` | Laboratorios de investigación |
| `proyectos` | Proyectos de investigación |
| `obra` | Obras literarias (tabla central) |
| `teatro` | Obras de teatro |
| `novela` | Obras narrativas |
| `periodico` | Artículos periodísticos |
| `poesia` | Poemas |
| `musica_impresa` | Obras musicales |
| `lugar` | Localizaciones geográficas |
| `personajes` | Personajes de las obras |

### Características del Esquema

✅ **Constraints validados:**
- Claves primarias y foráneas
- Validación de fechas (día/mes/año)
- Restricciones de rango (año de publicación)
- Unicidad de enlaces y correos
- Validación de valores (NO nulos cuando es necesario)

✅ **Índices optimizados:**
- Índices simples en campos de búsqueda común
- Índices compuestos para búsquedas frecuentes
- Índices en claves foráneas

✅ **Vistas útiles:**
- `v_obras_por_proyecto`: Resumen de obras por proyecto
- `v_obras_por_autor`: Estadísticas de autores
- `v_obras_por_tipo`: Estadísticas por tipo de publicación
- `v_periodicos_completos`: Vista de periódicos

✅ **Triggers automáticos:**
- Actualización del timestamp `actualizado_en` en modificaciones

### Consultas Útiles

```sql
-- Obras más recientes
SELECT * FROM obra ORDER BY fecha DESC LIMIT 10;

-- Autores con más obras
SELECT nombre_autor, COUNT(*) as total FROM obra 
GROUP BY nombre_autor ORDER BY total DESC;

-- Obras por tipo de publicación
SELECT * FROM v_obras_por_tipo;

-- Búsqueda por tema
SELECT * FROM obra WHERE tema_principal ILIKE '%amor%';

-- Estadísticas por proyecto
SELECT * FROM v_obras_por_proyecto;
```

## 🐍 Backend - Python/Flask

### Fuente de Datos

El backend obtiene datos del portal de **datos enlazados de la BNE**:
- **Portal:** https://datos.bne.es
- **Licencia:** CC0 (Creative Commons Public Domain)
- **Tecnología:** Linked Data (RDF, JSON-LD)

### Instalación Local

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate

# Instalar dependencias
pip install -r backend/requirements.txt
```

### Scraper de BNE

El scraper `bne_scraper.py` extrae datos de autores y periódicos desde el portal oficial de datos poblados de la BNE.

#### Funcionalidades:

```python
BNEScraper (5 métodos principales):
├── buscar_autores()          # Búsqueda de autores españoles
├── buscar_periodicos()       # Búsqueda de periódicos históricos
├── obtener_obras_autor()     # Obras de un autor específico
├── guardar_csv()             # Exportar a CSV
└── guardar_json()            # Exportar a JSON
```

#### Ejemplo de Uso:

```python
from backend.bne_scraper import BNEScraper

# Crear instancia
scraper = BNEScraper()

# Buscar autores
autores = scraper.buscar_autores("García Lorca")
print(f"Se encontraron {len(autores)} registros")

# Buscar periódicos
periodicos = scraper.buscar_periodicos("ABC")

# Búsqueda completa
autores_list = ["García Lorca", "Machado", "Cervantes"]
periodicos_list = ["ABC", "La Vanguardia"]
scraper.ejecutar_busqueda_completa(autores_list, periodicos_list)
# Genera 4 archivos: autores.json/csv, periodicos.json/csv
```

#### Datos Exportados:

El scraper genera archivos en formato:
- **JSON:** Estructura completa de datos
- **CSV:** Tabular para importación a BD

```json
{
  "nombre": "Federico García Lorca",
  "identificador": "XX123456",
  "url": "https://datos.bne.es/data/XX123456",
  "tipo": "Persona",
  "fecha_nacimiento": "1898-06-05",
  "fecha_muerte": "1936-08-19"
}
```

#### Documentación Completa:

Ver [SCRAPER.md](docs/SCRAPER.md) para documentación técnica detallada.

### API Endpoints (por implementar)

```
GET  /api/obras               - Listar todas las obras
GET  /api/obras/<id>          - Obtener obra específica
POST /api/obras               - Crear obra nueva
PUT  /api/obras/<id>          - Actualizar obra
DELETE /api/obras/<id>        - Eliminar obra

GET  /api/autores             - Listar autores
GET  /api/periodicos          - Listar periódicos
GET  /api/proyectos           - Listar proyectos

GET  /api/estadisticas        - Estadísticas del repositorio
```

## 🎨 Frontend

**Estado:** Por implementar

Tecnologías sugeridas:
- React.js con TypeScript
- Tailwind CSS para estilos
- Recharts para visualizaciones
- Axios para llamadas API

## 🐳 Docker

### Comandos Útiles

```bash
# Iniciar servicios
docker-compose up

# Iniciar en background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Rebuild de imágenes
docker-compose up --build

# Ejecutar comando en un contenedor
docker exec -it bne_backend bash

# Reset completo (perder datos)
docker-compose down -v
```

### pgAdmin (Interfaz Web para BD)

- **URL:** http://localhost:5050
- **Email:** admin@example.com
- **Contraseña:** admin

## 📝 Migraciones

Las migraciones se encuentran en `bd/migrations/`:

```bash
# Ver migraciones aplicadas
docker exec bne_database psql -U bne_user -d bne_db -c "\dt"

# Crear nueva migración
# 1. Crear archivo: bd/migrations/002_nueva_migracion.sql
# 2. Agregar a docker-compose.yml en volumes

# Aplicar migraciones (automático al iniciar)
docker-compose down -v
docker-compose up
```

## 📊 Datos de Ejemplo

El proyecto incluye seeders con datos de ejemplo en `bd/seeders/seed_data.sql`:

- ✅ 3 Usuarios
- ✅ 3 Laboratorios
- ✅ 2 Proyectos
- ✅ 11 Obras (novelas, periódicos, poesía, teatro)
- ✅ 8 Lugares geográficos
- ✅ 6 Personajes literarios
- ✅ Asociaciones entre tablas

Los seeders se ejecutan automáticamente en Docker.

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=backend

# Solo tests de modelo
pytest tests/models/
```

## 📚 Documentación Adicional

Consulta la carpeta `docs/`:
- `ARQUITECTURA.md` - Arquitectura general del proyecto
- `API.md` - Documentación detallada de API
- `BASE_DATOS.md` - Documentación del esquema
- `DESARROLLO.md` - Guía para desarrolladores

## 🔒 Seguridad

- Todas las credenciales en `.env` (no en código)
- Validación de entrada en todos los endpoints
- SQL Inyection Prevention via SQLAlchemy ORM
- CORS configurado para desarrollo
- Contraseñas hasheadas en base de datos

**⚠️ IMPORTANTE:** Cambiar `SECRET_KEY` en `.env` antes de producción

## 🤝 Contribuciones

1. Fork del repositorio
2. Crear rama: `git checkout -b feature/nombre-feature`
3. Commit: `git commit -am 'Add feature'`
4. Push: `git push origin feature/nombre-feature`
5. Pull Request

## 📞 Contacto y Soporte

- **Email:** contacto@proyecto-bne.es
- **Documentación:** [Wiki del Proyecto]
- **Issues:** Reportar bugs en la sección de Issues

## 📄 Licencia

Este proyecto está bajo licencia **MIT**. Consulta `LICENSE` para más detalles.

## 📋 Estado del Proyecto

- ✅ Base de datos diseñada y optimizada
- ✅ Scraper de BNE implementado
- ✅ Infraestructura Docker lista
- ✅ Datos de ejemplo (seeders)
- ⏳ Backend Flask (en desarrollo)
- ⏳ Frontend React (planificado)
- ⏳ Tests unitarios (planificado)
- ⏳ Deployment a producción (planificado)

---

**Última actualización:** 14 de abril de 2026

Proyecto desarrollado por el equipo de Prácticas INEM - Biblioteca Nacional de España
