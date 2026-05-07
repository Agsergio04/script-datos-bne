# 🚀 GUÍA: Extraer Datos de BNE - Solución Completa

## 📍 Problema Original
```
Error: net::ERR_CONNECTION_REFUSED
POST http://localhost:5000/api/importar/url
```
**Causa**: El backend no estaba corriendo.

---

## ✅ OPCIÓN 1: Prueba Rápida (SIN Docker, SIN BD)

Perfecto para **pruebas rápidas** sin necesidad de base de datos.

### Paso 1: Instalar dependencias
```bash
cd "c:\Users\sergi\Desktop\Trabajo\Practicas\Inem-His\Recogida de datos de BNE"
pip install -r backend/requirements.txt
```

### Paso 2: Ejecutar el test
```bash
python test_extractor.py
```

### Resultado esperado
```
✅ ÉXITO: Se extrajeron X campos

📋 Datos extraídos:
TITULO: El ingenioso hidalgo Don Quijote de la Mancha
AUTOR: Cervantes Saavedra, Miguel de
AUTOR FIRMA: Miguel de Cervantes Saavedra
EDITORIAL: Ramón Sopena
LUGAR: Barcelona
FECHA: [ca. 1916]
DESCRIPCIÓN: 892 p.
DIMENSIONES: 18 cm
...

💾 Datos guardados en: quijote_datos.json
```

---

## ✅ OPCIÓN 2: Con Backend + Base de datos (Completo)

Para **producción** con almacenamiento en BD.

### Paso 1: Verificar Docker Desktop
```bash
# Debe mostrar la versión
docker --version
docker-compose --version
```

### Paso 2: Iniciar los servicios
```bash
cd "c:\Users\sergi\Desktop\Trabajo\Practicas\Inem-His\Recogida de datos de BNE"

# OPCIÓN A: Todos los servicios (DB + Backend + Frontend)
docker-compose up

# OPCIÓN B: Solo BD y Backend (sin Frontend)
docker-compose up db backend

# OPCIÓN C: Solo Backend (si BD ya corre en otra terminal)
docker-compose up backend
```

### Paso 3: Esperar a que levante
```
✓ db service healthy
✓ backend service running
Escuchando en: http://localhost:5000
```

### Paso 4: Probar el endpoint

**Opción A: Con cURL**
```bash
curl -X POST http://localhost:5000/api/importar/edicion/html \
  -H "Content-Type: application/json" \
  -d '{"url":"https://datos.bne.es/edicion/bimo0000659916.html"}'
```

**Opción B: Con Python**
```python
import requests

url = "http://localhost:5000/api/importar/edicion/html"
data = {"url": "https://datos.bne.es/edicion/bimo0000659916.html"}

response = requests.post(url, json=data)
print(response.json())
```

**Opción C: Desde el Frontend**
```
http://localhost:3000/?url=https://datos.bne.es/edicion/bimo0000659916.html
```

### Resultado esperado (con BD)
```json
{
  "message": "Edición importada exitosamente",
  "data": {
    "id": 1,
    "titulo": "El ingenioso hidalgo Don Quijote de la Mancha",
    "enlace": "https://datos.bne.es/edicion/bimo0000659916.html",
    ...
  },
  "datos_extraidos": {
    "titulo": "El ingenioso hidalgo Don Quijote de la Mancha",
    "autor": "Cervantes Saavedra, Miguel de",
    "editorial": "Ramón Sopena",
    "lugar_publicacion": "Barcelona",
    "fecha_publicacion": "[ca. 1916]",
    ...
  }
}
```

---

## 🔧 NUEVOS ENDPOINTS DISPONIBLES

### 1️⃣ Importar desde Edición HTML
```
POST /api/importar/edicion/html
Content-Type: application/json

{
  "url": "https://datos.bne.es/edicion/bimo0000659916.html"
}
```

**Respuesta exitosa (201)**:
- Extrae datos del HTML automáticamente
- Guarda en BD sin dependencias de API
- Retorna datos extraídos + ID guardado

### 2️⃣ Importar desde URL (existente)
```
POST /api/importar/url
Content-Type: application/json

{
  "url": "https://datos.bne.es/data/XX123456"
}
```

### 3️⃣ Buscar por Título (existente)
```
POST /api/importar/titulo
Content-Type: application/json

{
  "titulo": "El Quijote"
}
```

### 4️⃣ Importar Lote (existente)
```
POST /api/importar/lote
Content-Type: application/json

{
  "obras": [
    {"url": "https://datos.bne.es/edicion/bimo0000659916.html"},
    {"titulo": "La Regenta"},
    {"url": "https://datos.bne.es/data/XX123456"}
  ]
}
```

---

## 📊 DATOS EXTRAÍDOS DEL QUIJOTE

De la URL proporcionada: https://datos.bne.es/edicion/bimo0000659916.html

| Campo | Valor |
|-------|-------|
| **Título** | El ingenioso hidalgo Don Quijote de la Mancha |
| **Autor Firma** | Miguel de Cervantes Saavedra |
| **Editorial** | Ramón Sopena |
| **Lugar** | Barcelona |
| **Fecha** | [ca. 1916] |
| **Descripción Física** | 892 p. |
| **Dimensiones** | 18 cm |
| **Forma del Contenido** | Texto (visual) |
| **Tipo de Medio** | sin mediación |
| **Características** | Ilustrado |

---

## 🛠️ SOLUCIÓN DE PROBLEMAS

### Error: `ERR_CONNECTION_REFUSED`
```
❌ POST http://localhost:5000/api/importar/url net::ERR_CONNECTION_REFUSED
```
**Solución**: El backend no está corriendo
```bash
docker-compose up backend
# O si usas test_extractor.py, asegúrate de pip install -r requirements.txt
```

### Error: `Cannot find module 'bs4'`
```
❌ ModuleNotFoundError: No module named 'bs4'
```
**Solución**: 
```bash
pip install beautifulsoup4 lxml
# O reinstalar todo
pip install -r backend/requirements.txt
```

### Error: `URL no es de edición`
```
❌ "error": "URL debe ser de una edición de datos.bne.es (contener /edicion/)"
```
**Solución**: Usa URLs con `/edicion/` o `/data/` en su estructura
```
✓ https://datos.bne.es/edicion/bimo0000659916.html
✓ https://datos.bne.es/data/XX123456
```

### Error: `No se pudo extraer el título`
```
❌ "error": "No se pudo extraer el título de la edición"
```
**Posibles causas**:
1. Estructura HTML diferente en la página
2. Bloqueo por User-Agent
3. Página con AJAX dinámico

**Solución**: 
- Verificar URL en navegador
- Comprobar estructura HTML (F12 > Inspector)
- Ajustar selectores en `bne_scraper.py`

---

## 📝 ARCHIVOS MODIFICADOS/CREADOS

- ✅ `backend/requirements.txt` - Agregado BeautifulSoup4 y lxml
- ✅ `backend/bne_scraper.py` - Nuevo método `extraer_datos_edicion_html()`
- ✅ `backend/app.py` - Nuevo endpoint `POST /api/importar/edicion/html`
- ✅ `test_extractor.py` - Script de prueba (NUEVO)

---

## 💡 PRÓXIMOS PASOS

1. **Prueba rápida**: Ejecuta `python test_extractor.py`
2. **Con BD**: Levanta `docker-compose up backend`
3. **Llamadas HTTP**: Usa cURL o tu cliente favorito
4. **Integración**: Modifica Frontend para usar el nuevo endpoint

---

## 📚 REFERENCIAS

- URL Quijote: https://datos.bne.es/edicion/bimo0000659916.html
- Portal BNE: https://datos.bne.es
- Documentación Flask: https://flask.palletsprojects.com
- BeautifulSoup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
