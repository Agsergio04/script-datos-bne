# 🏗️ Arquitectura del Proyecto

## Descripción General

El proyecto "Recogida de datos de BNE" es una plataforma moderna basada en microservicios que sigue una arquitectura cliente-servidor con contenedores Docker.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Cliente (Frontend)                        │
│                    React.js + TypeScript                         │
│                      Puerto 3000                                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP/REST
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                    API Gateway (Backend)                         │
│                  Flask + SQLAlchemy ORM                          │
│                      Puerto 5000                                 │
│  - Autenticación                                                │
│  - Autorización                                                 │
│  - Validación de datos                                          │
│  - Scraping de BNE                                              │
└──────────────────────────┬──────────────────────────────────────┘
                           │ SQL
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                     Base de Datos                                │
│                PostgreSQL 18                                     │
│                   Puerto 5432                                   │
│  - Tablas optimizadas                                           │
│  - Índices para rendimiento                                     │
│  - Vistas para análisis                                         │
│  - Triggers automáticos                                         │
└─────────────────────────────────────────────────────────────────┘
```

## Componentes

### 1. Frontend (React)
- **Localización:** `/frontend`
- **Puerto:** 3000
- **Tecnologías:** React 18, CSS con metodología BEM (carpeta `src/styles/`, sin Tailwind)
- **Responsabilidades:**
  - Interfaz de usuario interactiva
  - Consumo de API REST
  - Visualización de datos y gráficos
  - Gestión de estado (Redux)

### 2. Backend (Flask)
- **Localización:** `/backend`
- **Puerto:** 5000
- **Tecnologías:** Python 3.11, Flask 3, SQLAlchemy 2, psycopg2
- **Patrón:** Application Factory + Blueprints, separación SOLID por capas
- **Responsabilidades:**
  - Exposición de API REST
  - Lógica de negocio (importación, estadísticas)
  - Integración con scraper de BNE
  - Validación de datos

#### Estructura modular (Single Responsibility)
```
backend/
├── app.py                 Factory: crea la app y registra blueprints
├── config.py              Configuración (Config)
├── extensions.py          db = SQLAlchemy()  (sin app → evita ciclos)
├── bne_scraper.py         Cliente/scraper de datos.bne.es
├── models/                Capa de datos (un archivo por entidad)
│   ├── autor.py · usuario.py · obra.py · proyecto.py
├── services/              Dependencias compartidas
│   └── scraper.py         Instancia única de BNEScraper (DI)
└── blueprints/            Capa HTTP, una responsabilidad por blueprint
    ├── health.py          /health, /api/version, /api/info
    ├── obras.py           CRUD /api/obras + /api/periodicos/rango-fechas
    ├── autores.py         CRUD /api/autores
    ├── importar.py        /api/importar/*
    ├── estadisticas.py    /api/estadisticas/resumen + /api/buscar
    └── datasets.py        /api/buscar-datasets/kaggle
```

#### Cómo se aplican los principios SOLID
- **S**ingle Responsibility — cada módulo cubre una sola responsabilidad (config, datos, lógica externa, rutas).
- **O**pen/Closed — añadir un recurso = crear un blueprint y registrarlo en `app.py`; nada más se toca.
- **D**ependency Inversion — los blueprints dependen de abstracciones (`extensions.db`, `services.scraper`), no de implementaciones concretas.

### 3. Base de Datos (PostgreSQL)

#### Modelo E-R Simplificado:

```
┌─────────────┐         ┌───────────────┐
│   usuario   │────────→│   proyectos   │←─────────┐
├─────────────┤         ├───────────────┤          │
│ id_usuario  │         │ id_proyecto   │          │
│ nombre      │         │ nombre        │          │
│ email       │         │ usuario_id    │          │
└─────────────┘         └───────────────┘          │
                               │                    │
                               ↓                    │
                        ┌──────────────┐            │
                        │ proyecto_obra│────────────┤
                        ├──────────────┤            │
                        │ id_proyecto  │            │
                        │ id_obra      │            │
                        └──────────────┘            │
                               │                    │
                               ↓                    │
┌────────────────────────────────────────────────────┤
│                      obra                          │
├─────────────────────────────────────────────────────┤
│ id_obra (PK)                                       │
│ titulo, tipo_publicacion, autor_firma             │
│ nombre_autor, anio, fecha, enlace                 │
├─────────────────────────────────────────────────────┤
│ Foreign Keys:                                      │
│ └─ id_obra → teatro.id_obra                       │
│ └─ id_obra → novela.id_obra                       │
│ └─ id_obra → periodico.id_obra                    │
└─────────────────────────────────────────────────────┘
        │                           │
        ↓                           ↓
  ┌──────────┐                ┌──────────────┐
  │  teatro  │                │   novela     │
  ├──────────┤                ├──────────────┤
  │ id_obra  │                │ id_obra      │
  │ resumen  │                │ resumen      │
  │ modalidad│                │ modalidad    │
  └──────────┘                └──────────────┘
```

#### Características del Esquema:
- ✅ Normalización 3NF
- ✅ Integridad referencial
- ✅ Constraints validados
- ✅ Índices optimizados
- ✅ Vistas para análisis rápido
- ✅ Triggers automáticos

### 4. Contenedorización (Docker)

#### Docker Compose
`docker-compose.yml` orquesta 4 servicios:

1. **PostgreSQL** (db)
   - Puerto: 5432
   - Volumen: `postgres_data`
   - Health check: Automático

2. **Backend** (backend)
   - Puerto: 5000
   - Dependencia: db
   - Volumen: código local (para desarrollo)

3. **Frontend** (frontend)
   - Puerto: 3000
   - Dependencia: backend
   - Volumen: código local

4. **pgAdmin** (pgAdmin)
   - Puerto: 5050
   - Para administración visual de BD

## Flujo de Datos

### 1. Búsqueda de Obra

```
Usuario digita en frontend
    ↓
Frontend envía GET /api/obras?q=García
    ↓
Backend recibe en app.py
    ↓
SQLAlchemy construye query con filtros
    ↓
PostgreSQL ejecuta búsqueda con índices
    ↓
Resultados paginados retornan a backend
    ↓
JSON serializado al frontend
    ↓
React renderiza resultados
```

### 2. Scraping de BNE

```
Cliente inicia scraper desde frontend
    ↓
Backend llama a BNEScraper.ejecutar_busqueda_completa()
    ↓
BNEScraper.buscar_autores() → Peticiones HTTP a BNE
    ↓
BNEScraper.buscar_periodicos() → Peticiones HTTP a BNE
    ↓
Datos parseados y almacenados en JSON/CSV
    ↓
Incorporar a BD vía API
    ↓
Frontend notificado del progreso
```

## Patrón de Comunicación

### Cliente-Servidor (REST)

```
Request:
  GET /api/obras/123 HTTP/1.1
  Host: localhost:5000
  Accept: application/json

Response:
  HTTP/1.1 200 OK
  Content-Type: application/json
  {
    "id": 123,
    "titulo": "El Quijote",
    "nombre_autor": "Cervantes",
    ...
  }
```

### Servidor-Base de Datos (SQL)

```
Backend → PostgreSQL:
  SELECT * FROM obra 
  WHERE nombre_autor LIKE '%García%' 
  ORDER BY fecha DESC
  LIMIT 20;
```

## Seguridad

### Niveles de Protección:

1. **Transporte (TLS/HTTPS)** - En producción
2. **Aplicación**
   - Validación de entrada
   - Sanitización de SQL
   - CORS configurado
3. **Base de Datos**
   - Contraseñas hasheadas
   - Usuarios con permisos limitados
   - Backups regulares

## Escalabilidad

### Horizontal Scaling:
- Frontend: Múltiples instancias con Nginx (load balancer)
- Backend: Múltiples instancias con Gunicorn
- BD: Replicación y sharding (futuro)

### Vertical Scaling:
- Aumentar memoria asignada a servicios
- Aumentar CPU de PostgreSQL

## Monitoreo

### Herramientas Sugeridas:
- **Logs:** ELK Stack (Elasticsearch, Logstash, Kibana)
- **Métricas:** Prometheus + Grafana
- **APM:** New Relic o Datadog
- **Health Checks:** Integrados en Docker Compose

## Deployment

### Entornos:
- **Desarrollo:** Docker Compose local
- **Staging:** Kubernetes en la nube
- **Producción:** Kubernetes con balanceador de carga

### Servicios Cloud (Sugeridos):
- **Compute:** AWS ECS, Google Cloud Run, Azure Container Instances
- **Database:** AWS RDS, Google Cloud SQL, Azure Database
- **Frontend:** AWS S3 + CloudFront, Vercel, Netlify

---

**Versión:** 1.0.0
**Última actualización:** 14 de abril de 2026
