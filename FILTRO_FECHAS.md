# Filtro de Periódicos por Rango de Fechas 📅

Nueva funcionalidad para buscar automáticamente periódicos BIMO dentro de un rango de fechas específico.

## 🔍 ¿Qué es?

El **filtro por rango de fechas** permite extraer todos los periódicos cuya fecha de publicación se encuentre **entre dos fechas** de forma automática y rápida.

Perfecto para periódicos con prefijo: `https://datos.bne.es/resource/bimo...`

## 📌 Características

✅ Filtro **automático** por rango de fechas  
✅ Busca **periódicos + prensa** en BNE  
✅ Soporte via **parámetros URL**  
✅ **Paginación** integrada (20 resultados por defecto)  
✅ Ordenados por **fecha descendente**  

---

## 🚀 Cómo Usar

### 1️⃣ Interfaz Web (Frontend)

**Tab: "📅 Por Fechas"**

1. Haz clic en el tab **"📅 Por Fechas"** en la interfaz
2. Selecciona **"Fecha Desde"** (fecha de inicio)
3. Selecciona **"Fecha Hasta"** (fecha final)
4. Haz clic en **"Buscar Periódicos"**

```
┌─────────────────────────────────────┐
│ 📅 Buscar Periódicos por Fechas     │
├─────────────────────────────────────┤
│ Fecha Desde: [2020-01-01]           │
│ Fecha Hasta: [2024-12-31]           │
│                                     │
│ [Buscar Periódicos]                 │
└─────────────────────────────────────┘
```

### 2️⃣ Vía Parámetros URL

Accede directamente con parámetros en la URL:

```
http://localhost:3000/?fechaDesde=2020-01-01&fechaHasta=2024-12-31
```

**Parámetros:**
- `fechaDesde`: Fecha inicial (formato: YYYY-MM-DD)
- `fechaHasta`: Fecha final (formato: YYYY-MM-DD)

Se buscará **automáticamente** al cargar la página.

### 3️⃣ API REST (Backend)

**Endpoint:**
```
GET /api/periodicos/rango-fechas
```

**Ejemplo:**
```bash
curl -X GET "http://localhost:5000/api/periodicos/rango-fechas?fecha_desde=2020-01-01&fecha_hasta=2024-12-31&page=1&per_page=50"
```

**Parámetros:**
- `fecha_desde`: YYYY-MM-DD (obligatorio)
- `fecha_hasta`: YYYY-MM-DD (obligatorio)
- `page`: número de página (opcional, default: 1)
- `per_page`: resultados por página (opcional, default: 20)

**Respuesta:**
```json
{
  "data": [
    {
      "id_obra": 1,
      "titulo": "ABC",
      "tipo_publicacion": "Periódico",
      "fecha": "2020-01-15",
      "anio": 2020,
      "nombre_autor": "Redacción",
      "tema_principal": "General",
      ...
    }
  ],
  "rango_fechas": {
    "desde": "2020-01-01",
    "hasta": "2024-12-31"
  },
  "pagination": {
    "page": 1,
    "per_page": 50,
    "total": 245,
    "pages": 5
  }
}
```

---

## 📝 Ejemplos Prácticos

### 📌 Periódicos de 2021

**URL:**
```
http://localhost:3000/?fechaDesde=2021-01-01&fechaHasta=2021-12-31
```

**cURL:**
```bash
curl -X GET "http://localhost:5000/api/periodicos/rango-fechas?fecha_desde=2021-01-01&fecha_hasta=2021-12-31"
```

### 📌 Periódicos de 2020-2022 (3 años)

**URL:**
```
http://localhost:3000/?fechaDesde=2020-01-01&fechaHasta=2022-12-31
```

### 📌 Periódicos de un mes específico

**URL:**
```
http://localhost:3000/?fechaDesde=2023-03-01&fechaHasta=2023-03-31
```

### 📌 Periódicos recientes (últimos 5 años)

**URL:**
```
http://localhost:3000/?fechaDesde=2021-01-01&fechaHasta=2026-12-31
```

---

## 🔧 Cambios en el Código

### Backend (`app.py`)

**1. Actualización del endpoint GET `/api/obras`**
- Ahora acepta parámetros `fecha_desde` y `fecha_hasta`
- Filtra automáticamente por rango de fechas

**2. Nuevo endpoint: `GET /api/periodicos/rango-fechas`**
- Endpoint dedicado para búsquedas por rango de fechas
- Busca automáticamente periódicos y publicaciones
- Soporte para paginación

### Frontend (`App.jsx`)

**1. Hook `useQueryParams()` actualizado**
- Ahora captura `fechaDesde` y `fechaHasta` de la URL

**2. Nuevo estado: `fechaDesde` y `fechaHasta`**
- Almacena las fechas seleccionadas

**3. Nueva función: `buscarPorRangoFechas()`**
- Realiza la llamada al backend
- Formatea los resultados

**4. Nuevo tab: "📅 Por Fechas"**
- Interfaz visual con dos date pickers
- Botón para iniciar la búsqueda

**5. Auto-ejecución con parámetros URL**
- Si accedes con `?fechaDesde=...&fechaHasta=...`, se ejecuta automáticamente

---

## 🎯 Casos de Uso

| Caso | Parámetros | Descripción |
|------|-----------|-------------|
| **Un año completo** | `2023-01-01` a `2023-12-31` | Todos los periódicos de 2023 |
| **Mes específico** | `2023-05-01` a `2023-05-31` | Periódicos de mayo 2023 |
| **Semana** | `2023-05-01` a `2023-05-07` | Periódicos de una semana |
| **Un día** | `2023-05-15` a `2023-05-15` | Periódicos de un día exacto |
| **Rango de años** | `2020-01-01` a `2025-12-31` | Periódicos de 5 años |
| **Período histórico** | `1900-01-01` a `1950-12-31` | Periódicos históricos |

---

## 📊 Parámetros de Paginación

Cuando hay muchos resultados (>20), se paginan automáticamente:

```bash
# Página 1 (default)
curl -X GET "http://localhost:5000/api/periodicos/rango-fechas?fecha_desde=2020-01-01&fecha_hasta=2024-12-31&page=1&per_page=50"

# Página 2
curl -X GET "http://localhost:5000/api/periodicos/rango-fechas?fecha_desde=2020-01-01&fecha_hasta=2024-12-31&page=2&per_page=50"

# 100 resultados por página
curl -X GET "http://localhost:5000/api/periodicos/rango-fechas?fecha_desde=2020-01-01&fecha_hasta=2024-12-31&per_page=100"
```

---

## ✅ Requisitos

- ✅ Backend ejecutándose (`python app.py` o `docker-compose up backend`)
- ✅ Base de datos PostgreSQL con datos cargados
- ✅ Frontend en ejecución
- ✅ Tabla `obra` con campos `fecha`, `tipo_publicacion`

---

## 🐛 Troubleshooting

### ❌ "Los parámetros fecha_desde y fecha_hasta son obligatorios"
- Asegúrate de ingresar AMBAS fechas
- Formato: YYYY-MM-DD

### ❌ "Formato de fecha inválido"
- Usa el formato **YYYY-MM-DD** (ej: 2023-05-15)
- No incluyas horas o minutos

### ❌ Sin resultados
- Verifica que haya datos en la BD
- Comprueba que el rango de fechas es correcto
- Revisa que haya periódicos en ese rango

---

## 📚 Endpoint Completo

```
GET /api/periodicos/rango-fechas?fecha_desde=YYYY-MM-DD&fecha_hasta=YYYY-MM-DD&page=1&per_page=20
```

**Busca:**
- Tipo de publicación contiene: "periódico" O "prensa"
- Fecha >= fecha_desde
- Fecha <= fecha_hasta

**Ordena:** Por fecha (descendente) y título (ascendente)

**Pagina:** Resultados en bloques

---

## 🔗 Enlaces Útiles

- [Documentación API General](./docs/API.md)
- [Tutorial de Importación](./TUTORIAL_IMPORTACION.md)
- [Parámetros URL](./PARAMETROS_URL.md)

---

**Versión:** 1.3.0  
**Última actualización:** 23 de abril de 2026
