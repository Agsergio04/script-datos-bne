# 📚 Tutorial - Importación de Obras desde datos.bne.es

> Guía práctica para importar obras de la Biblioteca Nacional de España directamente en la base de datos

## Tabla de Contenidos

1. [Requisitos](#requisitos)
2. [Importar por URL](#importar-por-url)
3. [Importar por Título](#importar-por-título)
4. [Importar Lote Masivo](#importar-lote-masivo)
5. [Ejemplos Prácticos](#ejemplos-prácticos)
6. [Troubleshooting](#troubleshooting)

---

## Requisitos

✅ **Backend ejecutándose:**
```bash
docker-compose up -d
```

✅ **Verificar que API está funcionando:**
```bash
curl http://localhost:5000/health
# Respuesta esperada: {"status": "healthy", ...}
```

✅ **Python 3.11+ con requests** (ya incluido en `requirements.txt`)

---

## 1️⃣ Importar por URL

### Cuándo usar:
- ✅ Ya tienes la URL exacta de datos.bne.es
- ✅ Conoces el código de la obra (ej: XX123456)
- ✅ Importar obra específica de forma rápida

### Cómo encontrar la URL:

1. Ve a **https://datos.bne.es**
2. Busca la obra
3. Copia la URL del resultado, debe ser algo como:
   ```
   https://datos.bne.es/data/XX0000000
   ```

### Comando cURL:

```bash
curl -X POST http://localhost:5000/api/importar/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://datos.bne.es/data/XX0000000"}'
```

### Python:

```python
import requests

url_api = "http://localhost:5000/api/importar/url"
obra_url = "https://datos.bne.es/data/XX0000000"

response = requests.post(url_api, json={"url": obra_url})
resultado = response.json()

print(f"Status: {response.status_code}")
print(f"Mensaje: {resultado['message']}")
print(f"Datos: {resultado['data']}")
```

### Respuestas:

#### ✅ Éxito (201 Created):
```json
{
  "message": "Obra importada exitosamente",
  "data": {
    "id": 12,
    "titulo": "El Quijote",
    "nombre_autor": "Miguel de Cervantes",
    "anio": 1605,
    "tipo_publicacion": "Novela",
    "enlace": "https://datos.bne.es/data/XX0000000",
    "fecha_creacion": "2024-04-14T10:30:00Z"
  }
}
```

#### ⚠️ Ya existe (200 OK):
```json
{
  "message": "Obra ya existe en la base de datos",
  "data": {
    "id": 12,
    "titulo": "El Quijote",
    ...
  }
}
```

#### ❌ Error (400 Bad Request):
```json
{
  "message": "URL inválida o sin información disponible",
  "error": "Failed to fetch metadata from URL"
}
```

---

## 2️⃣ Importar por Título

### Cuándo usar:
- ✅ No tienes la URL exacta
- ✅ Solo sabes el título o parte de él
- ✅ Sistema buscará automáticamente

### Comando cURL:

```bash
curl -X POST http://localhost:5000/api/importar/titulo \
  -H "Content-Type: application/json" \
  -d '{"titulo": "El Quijote"}'
```

### Python:

```python
import requests

url_api = "http://localhost:5000/api/importar/titulo"

response = requests.post(url_api, json={"titulo": "El Quijote"})
resultado = response.json()

print(f"Status: {response.status_code}")
if response.status_code == 201:
    print(f"✅ Importada: {resultado['data']['titulo']}")
elif response.status_code == 200:
    print(f"⚠️ Ya existe: {resultado['data']['titulo']}")
else:
    print(f"❌ Error: {resultado['message']}")
```

### Lo que sucede internamente:

```
1. Recibe: "El Quijote"
2. Busca en datos.bne.es
3. Encuentra URL: https://datos.bne.es/data/XX0000000
4. Extrae todos los metadatos
5. Verifica si ya existe
6. Inserta en BD si no existe
7. Retorna datos
```

### Ejemplos de títulos para probar:

```bash
# Clásicos españoles
"El Quijote"
"La Regenta"
"Bodas de sangre"
"Cien años de soledad"
"Como agua para chocolate"

# Por autor
"Lorca"
"García Márquez"
"Cervantes"
```

---

## 3️⃣ Importar Lote Masivo

### Cuándo usar:
- ✅ Importar múltiples obras de una vez
- ✅ Mezclar títulos y URLs
- ✅ Migración de datos
- ✅ Actualizaciones periódicas

### Comando cURL:

```bash
curl -X POST http://localhost:5000/api/importar/lote \
  -H "Content-Type: application/json" \
  -d '{
    "obras": [
      {"titulo": "El Quijote"},
      {"titulo": "La Regenta"},
      {"url": "https://datos.bne.es/data/XX123456"},
      {"titulo": "Bodas de sangre"},
      {"titulo": "La casa de los espíritus"}
    ]
  }'
```

### Python:

```python
import requests
import json

url_api = "http://localhost:5000/api/importar/lote"

obras = [
    {"titulo": "El Quijote"},
    {"titulo": "La Regenta"},
    {"url": "https://datos.bne.es/data/XX123456"},
    {"titulo": "Bodas de sangre"},
]

response = requests.post(url_api, json={"obras": obras})
resultado = response.json()

# Mostrar estadísticas
stats = resultado['estadisticas']
print(f"Total procesadas: {stats['total']}")
print(f"✅ Importadas: {stats['importadas']}")
print(f"⚠️ Existentes: {stats['existentes']}")
print(f"❌ Errores: {stats['errores']}")

# Mostrar detalles
if resultado['resultados']['importadas']:
    print("\n📥 IMPORTADAS:")
    for obra in resultado['resultados']['importadas']:
        print(f"  - {obra['titulo']} (ID: {obra['id']})")

if resultado['resultados']['existentes']:
    print("\n⚠️ YA EXISTENTES:")
    for obra in resultado['resultados']['existentes']:
        print(f"  - {obra['titulo']} (ID: {obra['id']})")

if resultado['resultados']['errores']:
    print("\n❌ ERRORES:")
    for error in resultado['resultados']['errores']:
        print(f"  - {error['titulo']}: {error['mensaje']}")
```

### Respuesta completa:

```json
{
  "message": "Procesadas 5 obras",
  "estadisticas": {
    "importadas": 3,
    "existentes": 1,
    "errores": 1,
    "total": 5
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
      },
      {
        "id": 14,
        "titulo": "Bodas de sangre",
        "origen": "Título: Bodas de sangre"
      }
    ],
    "existentes": [
      {
        "id": 15,
        "titulo": "La casa de los espíritus",
        "origen": "Título: La casa de los espíritus"
      }
    ],
    "errores": [
      {
        "titulo": "Los miserables",
        "origen": "Título: Los miserables",
        "mensaje": "No encontrado en datos.bne.es"
      }
    ]
  }
}
```

### Ventajas del lote:

✅ **Error Isolation:** Un error no detiene el proceso  
✅ **Estadísticas:** Resumen automático  
✅ **Detalles:** Sabe qué se importó, qué quedó, qué falló  
✅ **Eficiente:** Una sola llamada para múltiples obras  

---

## 📋 Ejemplos Prácticos

### Ejemplo 1: Literatura Clásica Española

```bash
curl -X POST http://localhost:5000/api/importar/lote \
  -H "Content-Type: application/json" \
  -d '{
    "obras": [
      {"titulo": "El Quijote"},
      {"titulo": "La Regenta"},
      {"titulo": "Bodas de sangre"},
      {"titulo": "La casa de Bernarda Alba"},
      {"titulo": "Luces de bohemia"}
    ]
  }'
```

### Ejemplo 2: Mezclar Títulos y URLs

```bash
curl -X POST http://localhost:5000/api/importar/lote \
  -H "Content-Type: application/json" \
  -d '{
    "obras": [
      {"titulo": "El Quijote"},
      {"url": "https://datos.bne.es/data/XX0035968"},
      {"titulo": "La Regenta"},
      {"url": "https://datos.bne.es/data/XX0048283"}
    ]
  }'
```

### Ejemplo 3: Periódicos Históricos

```bash
curl -X POST http://localhost:5000/api/importar/lote \
  -H "Content-Type: application/json" \
  -d '{
    "obras": [
      {"titulo": "ABC"},
      {"titulo": "La Vanguardia"},
      {"titulo": "El País"},
      {"titulo": "El Mundo"}
    ]
  }'
```

### Ejemplo 4: Con Python - Script Reutilizable

```python
#!/usr/bin/env python3
# import_obras.py

import requests
import json
import sys

API_URL = "http://localhost:5000/api/importar/lote"

def importar_obras(lista_titulos):
    """Importa lista de obras por títulos"""
    obras = [{"titulo": titulo} for titulo in lista_titulos]
    
    try:
        response = requests.post(API_URL, json={"obras": obras})
        resultado = response.json()
        
        # Mostrar resultados
        stats = resultado['estadisticas']
        print(f"\n📊 RESUMEN:")
        print(f"  Total: {stats['total']}")
        print(f"  ✅ Importadas: {stats['importadas']}")
        print(f"  ⚠️  Existentes: {stats['existentes']}")
        print(f"  ❌ Errores: {stats['errores']}")
        
        return resultado
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return None

if __name__ == "__main__":
    titulos = [
        "El Quijote",
        "La Regenta",
        "Bodas de sangre",
        "La casa de los espíritus",
        "Cien años de soledad"
    ]
    
    importar_obras(titulos)
```

**Usar:**
```bash
python import_obras.py
```

---

## 🆘 Troubleshooting

### ❌ Error: "Connection refused"

**Problema:** API no está ejecutándose

**Solución:**
```bash
# Verificar que docker estaá ejecutándose
docker-compose ps

# Si no está, iniciar
docker-compose up -d

# Verificar logs
docker-compose logs backend
```

---

### ❌ Error: "URL inválida"

**Problema:** URL no es de datos.bne.es o está mal escrita

**Solución:**
```bash
# ✅ Correcto
"https://datos.bne.es/data/XX0000000"

# ❌ Incorrecto
"https://www.bne.es/..."           # URL antigua
"https://datos.bne.es/XX0000000"   # Sin /data/
"datos.bne.es/data/XX0000000"      # Sin protocolo https://
```

---

### ⚠️ Error: "No encontrado en datos.bne.es"

**Problema:** El título no existe en datos.bne.es

**Solución:**
1. Verificar título (mayúsculas/minúsculas, acentos)
2. Probar en https://datos.bne.es directamente
3. Usar URL directa si la conoces

---

### ❌ Error: 500 - Internal Server Error

**Problema:** Error en el servidor

**Solución:**
```bash
# Ver logs del backend
docker-compose logs backend -f

# Si hay error de BD
docker-compose logs db -f

# Reiniciar servicios
docker-compose restart backend
```

---

### ⏱️ Error: "Request timeout"

**Problema:** datos.bne.es tardó mucho en responder

**Solución:**
- Esperar e reintentar
- Verificar conexión a internet
- Usar URL directa en lugar de título (más rápido)

---

## 📊 Campos Importados Automáticamente

Cuando importas una obra, se extraen automáticamente estos campos:

```
✅ titulo                 - Nombre de la obra
✅ tipo_publicacion       - Novela, Poesía, Periódico, etc.
✅ nombre_autor          - Nombre completo del autor
✅ author_firma          - Firma del autor
✅ anio                 - Año de publicación
✅ fecha                - Fecha completa de publicación
✅ descripcion          - Resumen/descripción
✅ tema_principal       - Tema o categoría
✅ paginas              - Número de páginas
✅ idioma               - Idioma del texto
✅ imprenta             - Editorial/Imprenta
✅ lugar_impresion      - Lugar de publicación
✅ como_citar           - Forma recomendada de citar
✅ uri_rdf              - URI del recurso RDF
✅ url_digital          - URL del texto digital (si disponible)
✅ derechos             - Información de derechos/licencia
✅ formato              - Formato del documento
✅ num_periodico        - Número (si es periódico)
✅ identificador        - Identificador único BNE
✅ enlace               - URL de datos.bne.es
```

---

## 🔄 Flujo Visual

```
USUARIO
   │
   ├─→ [Tengo URL exacta]
   │        │
   │        └─→ POST /api/importar/url
   │             ├─→ Valida URL
   │             ├─→ GET JSON/RDF de datos.bne.es
   │             ├─→ Extrae metadata (20+ campos)
   │             ├─→ ¿Duplicado? SÍ → 200 OK
   │             ├─→ ¿Duplicado? NO → INSERT → 201 Created
   │             └─→ Return JSON
   │
   ├─→ [Solo tengo título]
   │        │
   │        └─→ POST /api/importar/titulo
   │             ├─→ Valida título
   │             ├─→ SEARCH en datos.bne.es
   │             ├─→ Extrae URL del resultado
   │             ├─→ (Continúa como importar/url)
   │             └─→ Return JSON
   │
   └─→ [Tengo múltiples]
            │
            └─→ POST /api/importar/lote
                 ├─→ FOR CADA OBRA
                 │    ├─→ Intenta importar
                 │    ├─→ Captura errores (no detiene)
                 │    └─→ Registra resultado
                 ├─→ Calcula estadísticas
                 └─→ Return JSON con resumen
```

---

## 💡 Tips y Trucos

### Tip 1: Buscar URLs en datos.bne.es

```bash
# Acceder a API de búsqueda directly
curl "https://datos.bne.es/buscar?q=Quijote" | jq
```

### Tip 2: Verificar obra antes de importar

```bash
# Ver qué información extraería
curl "https://datos.bne.es/data/XX0000000.json" | jq
```

### Tip 3: Importar desde archivo

```bash
# Si tienes lista en JSON
curl -X POST http://localhost:5000/api/importar/lote \
  -H "Content-Type: application/json" \
  -d @obras.json
```

Donde `obras.json` contiene:
```json
{
  "obras": [
    {"titulo": "El Quijote"},
    {"titulo": "La Regenta"}
  ]
}
```

### Tip 4: Ver obras importadas

```bash
# Listar todas las obras
curl "http://localhost:5000/api/obras"

# Buscar por término
curl "http://localhost:5000/api/buscar?q=Quijote"
```

---

## 🎯 Resumen Rápido

| Situación | Endpoint | Comando |
|-----------|----------|---------|
| Tengo URL exacta | `/api/importar/url` | `curl -X POST ... -d '{"url": "..."}' ` |
| Solo título | `/api/importar/titulo` | `curl -X POST ... -d '{"titulo": "..."}' ` |
| Múltiples obras | `/api/importar/lote` | `curl -X POST ... -d '{"obras": [...]}' ` |

---

**¡Listo!** 🎉 Ya sabes cómo importar obras. ¿Preguntas? Consulta [troubleshooting](#troubleshooting)
