# ✅ SOLUCIÓN COMPLETA: Extracción de Datos del Quijote de BNE

## 🎯 Problema Original Resuelto

```
ERROR: net::ERR_CONNECTION_REFUSED
POST http://localhost:5000/api/importar/url
```

**Solución**: Agregué un nuevo extractor que:
- ✅ Extrae datos HTML **sin necesidad de API REST de BNE**
- ✅ Funciona **sin base de datos** (opción local)
- ✅ Almacena en BD **cuando se levanta Docker** (opción completa)

---

## 📊 EJEMPLO: URL del Quijote

```
https://datos.bne.es/edicion/bimo0000659916.html
```

### Datos Extraídos Automáticamente
```json
{
  "titulo": "El ingenioso hidalgo Don Quijote de la Mancha; Miguel de Cervantes Saavedra;",
  "lugar_publicacion": "Barcelona",
  "editorial": "Ramón Sopena",
  "fecha_publicacion": "[ca. 1916]",
  "descripcion_fisica": "892 p.",
  "forma_contenido": "Texto (visual)",
  "tipo_medio": "sin mediación",
  "notas": [
    "Bibliografía: p. [19]-25",
    "De p. [30] pasa a p.[33]"
  ],
  "recursos_relacionados": [
    "Biblioteca Digital Hispánica"
  ]
}
```

---

## 🚀 USAR AHORA (3 opciones)

### OPCIÓN 1: Test Rápido (SIN Docker, SIN BD)

```bash
# 1. Instalar dependencias
pip install -r backend/requirements.txt

# 2. Ejecutar test
python test_extractor.py

# 3. Ver resultado en: quijote_datos.json
```

✅ **Ventaja**: Rápido, sin dependencias de DB
❌ **Inconveniente**: No almacena en base de datos

---

### OPCIÓN 2: Con Backend (Docker)

```bash
# 1. Levanta todos los servicios
docker-compose up

# 2. Espera a que esté listo
# Verás: ✓ db service healthy
#        ✓ backend running on :5000

# 3. Llama al endpoint (PowerShell):
$response = Invoke-RestMethod -Uri "http://localhost:5000/api/importar/edicion/html" `
  -Method POST `
  -Body (@{"url"="https://datos.bne.es/edicion/bimo0000659916.html"} | ConvertTo-Json) `
  -ContentType "application/json"
  
ConvertTo-Json $response
```

✅ **Ventaja**: Almacena en BD, sistema completo
❌ **Inconveniente**: Requiere Docker

---

### OPCIÓN 3: Con cURL (Para Postman)

```bash
curl -X POST http://localhost:5000/api/importar/edicion/html \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://datos.bne.es/edicion/bimo0000659916.html"
  }'
```

**Respuesta (201 Created)**:
```json
{
  "message": "Edición importada exitosamente",
  "data": {
    "id": 1,
    "titulo": "El ingenioso hidalgo Don Quijote de la Mancha",
    "enlace": "https://datos.bne.es/edicion/bimo0000659916.html",
    "fecha_creacion": "2026-04-21T08:25:00"
  },
  "datos_extraidos": {
    "titulo": "...",
    "editorial": "Ramón Sopena",
    "lugar_publicacion": "Barcelona",
    ...
  }
}
```

---

## 🔧 NUEVOS ARCHIVOS/CAMBIOS

| Archivo | Cambio | Descripción |
|---------|--------|-------------|
| `requirements.txt` | ✏️ Modificado | +beautifulsoup4, lxml |
| `bne_scraper.py` | ✏️ Modificado | Nuevo método `extraer_datos_edicion_html()` |
| `app.py` | ✏️ Modificado | Nuevo endpoint `POST /api/importar/edicion/html` |
| `test_extractor.py` | 🆕 Nuevo | Script de prueba rápida |
| `diagnostico_html.py` | 🆕 Nuevo | Diagnóstico de estructura HTML |
| `GUIA_EXTRACCION.md` | 🆕 Nuevo | Documentación completa |

---

## 💻 PYTHON API (Uso Programático)

```python
from backend.bne_scraper import BNEScraper

# Crear scraper
scraper = BNEScraper(verify_ssl=False)

# Extraer datos de la edición
url = "https://datos.bne.es/edicion/bimo0000659916.html"
datos = scraper.extraer_datos_edicion_html(url)

# Usar los datos
print(f"Título: {datos['titulo']}")
print(f"Editorial: {datos['editorial']}")
print(f"Lugar: {datos['lugar_publicacion']}")

# Guardar a JSON
import json
with open('datos_quijote.json', 'w', encoding='utf-8') as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)
```

---

## 🌐 INTEGRACIÓN CON FRONTEND

### Modificar App.jsx para usar nuevo endpoint

```jsx
// En App.jsx, cambiar POST a /api/importar/url por:

const [errorMsg, setErrorMsg] = useState('');

async function importarEdicionHTML(url) {
  try {
    const response = await fetch('http://localhost:5000/api/importar/edicion/html', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: url })
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('✅ Edición importada:', data);
      // Mostrar datos extraídos
      setErrorMsg(null);
      alert(`Importado: ${data.data.titulo}`);
    } else {
      const error = await response.json();
      setErrorMsg(error.error || 'Error al importar');
    }
  } catch (err) {
    setErrorMsg(`Error: ${err.message}`);
  }
}

// En el formulario:
<button onClick={() => importarEdicionHTML(formUrl)}>
  Importar Edición
</button>
```

---

## ✨ CARACTERÍSTICAS DEL EXTRACTOR

### ✅ Lo que extrae:
- Título
- Autor(es)
- Editorial/Imprenta
- Lugar de publicación
- Fecha de publicación
- Descripción física
- Dimensiones
- Forma del contenido
- Tipo de medio
- Idioma
- Notas
- Recursos relacionados
- ISBN/ISSN

### 🔄 Métodos de búsqueda (en orden):
1. **Tablas HTML** (Principal - Datos estructurados)
2. **Listas de definición (DL)**
3. **Divs con clases específicas**
4. **H1/H2/H3 headers**
5. **Meta tags**

### 🛡️ Manejo de errores:
- ✅ Certificados SSL (Windows) - Soportado con `verify_ssl=False`
- ✅ Timeouts - 30 segundos (configurable)
- ✅ Codificación UTF-8
- ✅ Caracteres especiales

---

## 📈 PRÓXIMOS PASOS RECOMENDADOS

1. **Prueba rápida** (sin Docker):
   ```bash
   python test_extractor.py
   ```

2. **Con BD** (Docker):
   ```bash
   docker-compose up backend
   curl -X POST http://localhost:5000/api/importar/edicion/html ...
   ```

3. **Frontend integrado**:
   - Modify `frontend/src/App.jsx`
   - Use nuevo endpoint `/api/importar/edicion/html`
   - Mostrar datos extraídos

4. **Producción**:
   - Activar verificación SSL (usa certificados válidos)
   - Agregar autenticación JWT
   - Logging centralizado
   - Rate limiting

---

## 🐛 TROUBLESHOOTING

### ¿No extrae datos?
1. Verifica que la URL es válida en navegador
2. Ejecuta `python diagnostico_html.py` para ver estructura HTML
3. Ajusta selectores según la estructura

### ¿Error SSL?
```python
scraper = BNEScraper(verify_ssl=False)  # ← Esto resuelve
```

### ¿No genera BD?
```bash
# Asegúrate que Docker está corriendo
docker-compose up db backend
```

---

## 📞 SOPORTE

**Archivos de referencia**:
- Guía completa: `GUIA_EXTRACCION.md`
- Datos ejemplo: `quijote_datos.json`
- Estructura HTML: `page_structure.html`
- Logs: `bne_scraper.log`

**URLs de prueba**:
- Quijote: https://datos.bne.es/edicion/bimo0000659916.html
- Portal: https://datos.bne.es

---

**¡Listo para usar! Elige tu opción y comienza.** 🎉
