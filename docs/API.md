# API REST - Documentación Técnica

## Base URL

```
http://localhost:5000
```

## Autenticación

Actualmente, la API no requiere autenticación. En producción, implementar JWT o OAuth2.

## Convenciones

- Método HTTP: Indica la acción (GET, POST, PUT, DELETE)
- Content-Type: `application/json`
- Codificación: UTF-8
- Códigos HTTP estándar

## Status Codes

| Código | Significado |
|--------|------------|
| 200 | OK - Solicitud exitosa |
| 201 | Created - Recurso creado |
| 400 | Bad Request - Entrada inválida |
| 404 | Not Found - Recurso no encontrado |
| 500 | Server Error - Error interno |

---

## Endpoints

### 1. Salud del Servicio

#### GET /health
Verificar que el servicio está operativo.

**Respuesta:**
```json
{
  "status": "healthy",
  "timestamp": "2024-04-14T10:30:00Z",
  "service": "BNE Backend API"
}
```

---

#### GET /api/version
Obtener versión de la API.

**Respuesta:**
```json
{
  "version": "1.0.0",
  "name": "BNE Data Collection API",
  "timestamp": "2024-04-14T10:30:00Z"
}
```

---

#### GET /api/info
Información del proyecto.

**Respuesta:**
```json
{
  "proyecto": "Recogida de datos BNE",
  "descripcion": "Plataforma para recopilar datos...",
  "estadisticas": {
    "usuarios": 3,
    "obras": 11,
    "proyectos": 2
  },
  "version": "1.0.0"
}
```

---

### 2. Gestión de Obras

#### GET /api/obras
Listar obras con paginación y filtros.

**Parámetros de Query:**
| Parámetro | Tipo | Descripción |
|-----------|------|------------|
| page | int | Página (default: 1) |
| per_page | int | Registros por página (default: 20) |
| tipo | string | Filtrar por tipo de publicación |
| autor | string | Filtrar por autor (búsqueda) |
| tema | string | Filtrar por tema (búsqueda) |
| anio | int | Filtrar por año |

**Ejemplo:**
```bash
curl "http://localhost:5000/api/obras?page=1&per_page=10&tipo=Novela&autor=Cervantes"
```

**Respuesta:**
```json
{
  "data": [
    {
      "id": 1,
      "titulo": "El Quijote",
      "tipo_publicacion": "Novela",
      "nombre_autor": "Miguel de Cervantes Saavedra",
      "anio": 1605,
      "tema_principal": "Aventuras caballerescas",
      "paginas": "620",
      "fecha_creacion": "2024-04-14T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 45,
    "pages": 5
  }
}
```

---

#### GET /api/obras/<obra_id>
Obtener una obra específica.

**Parámetros:**
| Parámetro | Tipo | Descripción |
|-----------|------|------------|
| obra_id | int | ID de la obra |

**Ejemplo:**
```bash
curl http://localhost:5000/api/obras/1
```

**Respuesta:**
```json
{
  "id": 1,
  "titulo": "El Quijote",
  "tipo_publicacion": "Novela",
  "autor_firma": "Cervantes",
  "nombre_autor": "Miguel de Cervantes Saavedra",
  "anio": 1605,
  "enlace": "https://...",
  "fecha": "1605-01-16",
  "tema_principal": "Aventuras caballerescas",
  "paginas": "620",
  "como_citar": "Cervantes, M. (1605). El Quijote...",
  "fecha_creacion": "2024-04-14T10:00:00Z",
  "actualizado_en": "2024-04-14T10:00:00Z"
}
```

---

#### POST /api/obras
Crear una nueva obra.

**Body (JSON):**
```json
{
  "titulo": "Nueva Obra",
  "tipo_publicacion": "Novela",
  "autor_firma": "Autor",
  "nombre_autor": "Nombre Completo Autor",
  "anio": 2024,
  "enlace": "https://...",
  "tema_principal": "Tema",
  "paginas": "100",
  "como_citar": "Cita APA"
}
```

**Respuesta (201 Created):**
```json
{
  "message": "Obra creada exitosamente",
  "data": {
    "id": 12,
    "titulo": "Nueva Obra",
    ...
  }
}
```

---

#### PUT /api/obras/<obra_id>
Actualizar una obra existente.

**Body (JSON):**
```json
{
  "titulo": "Nuevo Título",
  "anio": 2024,
  "tema_principal": "Nuevo Tema"
}
```

**Respuesta:**
```json
{
  "message": "Obra actualizada exitosamente",
  "data": {
    "id": 1,
    "titulo": "Nuevo Título",
    ...
  }
}
```

---

#### DELETE /api/obras/<obra_id>
Eliminar una obra.

**Ejemplo:**
```bash
curl -X DELETE http://localhost:5000/api/obras/1
```

**Respuesta:**
```json
{
  "message": "Obra eliminada exitosamente"
}
```

---

### 3. Estadísticas

#### GET /api/estadisticas/resumen
Obtener estadísticas generales del repositorio.

**Respuesta:**
```json
{
  "obras_por_tipo": [
    {
      "tipo": "Novela",
      "total": 4
    },
    {
      "tipo": "Periódico",
      "total": 3
    },
    {
      "tipo": "Poesía",
      "total": 3
    },
    {
      "tipo": "Teatro",
      "total": 2
    }
  ],
  "top_autores": [
    {
      "autor": "Federico García Lorca",
      "obras": 2
    },
    {
      "autor": "Miguel de Cervantes Saavedra",
      "obras": 1
    }
  ]
}
```

---

### 4. Búsqueda

#### GET /api/buscar
Búsqueda global en obras.

**Parámetros:**
| Parámetro | Tipo | Descripción |
|-----------|------|------------|
| q | string | Término de búsqueda (mínimo 3 caracteres) |

**Ejemplo:**
```bash
curl "http://localhost:5000/api/buscar?q=Quijote"
```

**Respuesta:**
```json
{
  "query": "Quijote",
  "total_resultados": 1,
  "resultados": [
    {
      "id": 1,
      "titulo": "El Quijote",
      "nombre_autor": "Miguel de Cervantes Saavedra",
      ...
    }
  ]
}
```

---

### 5. Importación desde datos.bne.es

#### POST /api/importar/url
Importa una obra directamente desde su URL en datos.bne.es.

**Body (JSON):**
```json
{
  "url": "https://datos.bne.es/data/XX123456"
}
```

**Ejemplo:**
```bash
curl -X POST http://localhost:5000/api/importar/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://datos.bne.es/data/XX123456"}'
```

**Respuesta (201 Created):**
```json
{
  "message": "Obra importada exitosamente",
  "data": {
    "id": 12,
    "titulo": "El Quijote",
    "nombre_autor": "Miguel de Cervantes",
    "enlace": "https://datos.bne.es/data/XX123456",
    ...
  }
}
```

**Posibles Respuestas:**
- `201 Created` - Obra importada correctamente
- `200 OK` - Obra ya existe en BD
- `400 Bad Request` - URL no válida o sin información
- `500 Server Error` - Error interno

---

#### POST /api/importar/titulo
Busca una obra por título en datos.bne.es e importa toda su información.

**Body (JSON):**
```json
{
  "titulo": "El Quijote"
}
```

**Ejemplo:**
```bash
curl -X POST http://localhost:5000/api/importar/titulo \
  -H "Content-Type: application/json" \
  -d '{"titulo": "El Quijote"}'
```

**Respuesta (201 Created):**
```json
{
  "message": "Obra importada exitosamente",
  "data": {
    "id": 12,
    "titulo": "El Quijote",
    "nombre_autor": "Miguel de Cervantes",
    "tipo_publicacion": "Novela",
    "anio": 1605,
    "tema_principal": "Aventuras caballerescas",
    "enlace": "https://datos.bne.es/data/XX123456",
    ...
  }
}
```

**Validaciones:**
- Título mínimo 3 caracteres
- Si no se encuentra en datos.bne.es, devuelve 404

---

#### POST /api/importar/lote
Importa múltiples obras desde una lista de títulos y/o URLs.

**Body (JSON):**
```json
{
  "obras": [
    {"titulo": "El Quijote"},
    {"titulo": "La Regenta"},
    {"url": "https://datos.bne.es/data/XX123456"},
    {"titulo": "Bodas de sangre"}
  ]
}
```

**Ejemplo:**
```bash
curl -X POST http://localhost:5000/api/importar/lote \
  -H "Content-Type: application/json" \
  -d '{
    "obras": [
      {"titulo": "El Quijote"},
      {"titulo": "La Regenta"},
      {"titulo": "Bodas de sangre"}
    ]
  }'
```

**Respuesta:**
```json
{
  "message": "Procesadas 3 obras",
  "estadisticas": {
    "importadas": 2,
    "existentes": 1,
    "errores": 0,
    "total": 3
  },
  "resultados": {
    "importadas": [
      {
        "id": 12,
        "titulo": "El Quijote",
        "origen": "Título: El Quijote"
      },
      {
        "id": 13,
        "titulo": "La Regenta",
        "origen": "Título: La Regenta"
      }
    ],
    "existentes": [
      {
        "id": 14,
        "titulo": "Bodas de sangre",
        "origen": "Título: Bodas de sangre"
      }
    ],
    "errores": []
  }
}
```

**Procesamiento:**
- Procesa obras una por una
- Si existe en BD, la marca como existente (no duplica)
- Si hay error, lo registra pero continúa con las demás
- Retorna estadísticas consolidadas

---

## 🔄 Flujo de Importación

```
┌─────────────────────────────────────────────────────────────┐
│                     3 Métodos Disponibles                    │
└─────────────────────────────────────────────────────────────┘

1. POR URL DIRECTA
   ┌─────────────┐
   │ URL + datos │
   │ bne.es/data │
   └──────┬──────┘
          │
          ▼
   ┌──────────────────┐
   │ GET desde datos  │
   │ bne.es (JSON/RDF)│
   └────────┬─────────┘
            │
            ▼
   ┌──────────────────┐
   │ Procesar         │
   │ metadata         │
   │ (20+ campos)     │
   └────────┬─────────┘
            │
            ▼
   ┌──────────────────┐
   │ ¿Duplicado?      │
   │ (donde enlace=URL)
   └────────┬─────────┘
            │
       Sí ─┼─ No
          │   │
          │   ▼
          │  ┌──────────────────┐
          │  │ INSERT en BD      │
          │  │ (SQLAlchemy)      │
          │  └──────────────────┘
          │
          ▼
   ┌──────────────────┐
   │ RETURN JSON      │
   │ 201/200          │
   └──────────────────┘


2. POR TÍTULO
   ┌─────────────┐
   │ TÍTULO      │
   │ (string)    │
   └──────┬──────┘
          │
          ▼
   ┌──────────────────┐
   │ SEARCH en datos  │
   │ bne.es           │
   └────────┬─────────┘
            │
            ▼
   ┌──────────────────┐
   │ EXTRACT URL      │
   │ de resultados    │
   └────────┬─────────┘
            │
            └─────────────────┐
                              │
                    (igual que Método 1)


3. LOTE (MÚLTIPLES)
   ┌─────────────┐
   │ ARRAY de    │
   │ {url|titulo}│
   └──────┬──────┘
          │
          ▼
   ┌──────────────────┐
   │ FOR CADA OBRA    │
   │ (error isolation)│
   └────────┬─────────┘
            │
            ├─→ Intenta URL/Título
            │   (Método 1 o 2)
            │
            │ ✓ Importada
            │ ✓ Existente
            │ ✗ Error
            │
            ▼
   ┌──────────────────┐
   │ ESTADÍSTICAS     │
   │ consolidadas     │
   │ {importadas,     │
   │  existentes,     │
   │  errores}        │
   └──────────────────┘
```

**Validaciones en Todos los Métodos:**
- ✓ Se valida que URL/Título no sean NULL
- ✓ Se verifica duplicado antes de insertar
- ✓ Se extraen 20+ campos automáticamente
- ✓ Si hay error, se registra y continúa
- ✓ Transacción rollback en duplicados (BD intacta)

**Campos Extraídos Automáticamente:**
1. titulo
2. tipo_publicacion
3. autor_firma
4. nombre_autor
5. anio
6. fecha
7. tema_principal
8. paginas
9. como_citar
10. imprenta
11. lugar_impresion
12. uri_rdf
13. url_digital
14. derechos
15. formato
16. num_periodico
17. identificador
18. enlace (de datos.bne.es)
19. descripcion
20. idioma

---

## Ejemplos con cURL

### Buscar obras
```bash
curl "http://localhost:5000/api/buscar?q=Quijote"
```

### Importar por URL
```bash
curl -X POST http://localhost:5000/api/importar/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://datos.bne.es/data/XX0000000"}'
```

### Importar por TÍTULO
```bash
curl -X POST http://localhost:5000/api/importar/titulo \
  -H "Content-Type: application/json" \
  -d '{"titulo": "El Quijote"}'
```

### Importar LOTE (múltiples)
```bash
curl -X POST http://localhost:5000/api/importar/lote \
  -H "Content-Type: application/json" \
  -d '{
    "obras": [
      {"titulo": "El Quijote"},
      {"titulo": "La Regenta"},
      {"url": "https://datos.bne.es/data/XX123456"}
    ]
  }'
```

### Listar obras
```bash
curl "http://localhost:5000/api/obras?page=1&per_page=5"
```

### Crear obra
```bash
curl -X POST http://localhost:5000/api/obras \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Mi Nueva Obra",
    "tipo_publicacion": "Poesía",
    "nombre_autor": "Poeta Desconocido",
    "anio": 2024,
    "tema_principal": "Modernismo"
  }'
```

### Actualizar obra
```bash
curl -X PUT http://localhost:5000/api/obras/1 \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "El Quijote - Edición Revisada",
    "anio": 1605
  }'
```

### Eliminar obra
```bash
curl -X DELETE http://localhost:5000/api/obras/1
```

### Estadísticas
```bash
curl http://localhost:5000/api/estadisticas/resumen
```

### Búsqueda
```bash
curl "http://localhost:5000/api/buscar?q=García+Lorca"
```

---

## Rate Limiting

Actualmente no implementado. En producción, considerar:
- 100 requests por minuto por IP
- 1000 requests por hora por usuario autenticado

## CORS

Configurado para aceptar requestsdesde:
- http://localhost:3000 (frontend local)
- En producción, restringir a dominio específico

## Errores Comunes

### 404 Not Found
```json
{
  "error": "Obra no encontrada"
}
```

### 400 Bad Request
```json
{
  "error": "Título es requerido"
}
```

### 500 Server Error
```json
{
  "error": "Error interno del servidor"
}
```

---

**Versión:** 1.0.0
**Última actualización:** 14 de abril de 2026
