# 🎯 Configuración de Búsqueda en Kaggle

## Requisitos

El endpoint `/api/buscar-datasets/kaggle` requiere credenciales válidas de Kaggle.

## 📋 Pasos de Configuración

### 1️⃣ Crear Cuenta en Kaggle
- Ve a https://www.kaggle.com/register
- Completa el formulario y verifica tu email

### 2️⃣ Generar API Token
1. Inicia sesión en Kaggle
2. Ve a **Settings** (esquina superior derecha)
3. Haz clic en **Account**
4. En la sección **API**, haz clic en **Create New API Token**
5. Se descargará automáticamente un archivo `kaggle.json`

### 3️⃣ Guardar el Archivo en la Ubicación Correcta

**En Windows:**
```
C:\Users\{tu_usuario}\.kaggle\kaggle.json
```

**En Linux/Mac:**
```
~/.kaggle/kaggle.json
```

**Ejemplo de contenido kaggle.json:**
```json
{
  "username": "tu_usuario",
  "key": "abc123def456ghi789jkl012..."
}
```

### 4️⃣ Permisos del Archivo (Linux/Mac)
```bash
chmod 600 ~/.kaggle/kaggle.json
```

---

## 🚀 Uso del Endpoint

### Endpoint: `POST /api/buscar-datasets/kaggle`

### Ejemplo 1: Búsqueda Básica
```bash
curl -X POST http://localhost:5000/api/buscar-datasets/kaggle \
  -H "Content-Type: application/json" \
  -d '{
    "query": "periódicos historia españa"
  }'
```

### Ejemplo 2: Búsqueda Avanzada
```bash
curl -X POST http://localhost:5000/api/buscar-datasets/kaggle \
  -H "Content-Type: application/json" \
  -d '{
    "query": "periódicos prensa newspaper",
    "num_resultados": 20,
    "sort_by": "downloads",
    "license": "cc"
  }'
```

### Parámetros
| Parámetro | Tipo | Descripción | Default |
|-----------|------|-------------|---------|
| `query` | string | Término de búsqueda (mín. 3 caracteres) | REQUERIDO |
| `num_resultados` | int | Cantidad de datasets a devolver (1-100) | 10 |
| `sort_by` | string | Ordenar por: `votes`, `newest`, `downloads` | `votes` |
| `license` | string | Filtro de licencia (cc, gpl, cc0, odb, all) | `all` |

### Respuesta Exitosa (200 OK)
```json
{
  "query": "periódicos historia",
  "fuente": "kaggle",
  "cantidad": 5,
  "parametros": {
    "sort_by": "votes",
    "license": "all",
    "solicitados": 10
  },
  "resultados": [
    {
      "indice": 1,
      "titulo": "usuario/dataset-periodicos-espanoles",
      "descripcion": "Spanish Historical Newspapers Dataset",
      "url": "https://www.kaggle.com/datasets/usuario/dataset-periodicos-espanoles",
      "descargas": 1245,
      "votos": 89,
      "likes": 12,
      "actualizado": "2024-01-15",
      "creador": "usuario",
      "tamaño": "2.5 GB",
      "topicTags": ["spain", "history", "newspapers"]
    },
    ...
  ],
  "mensaje": "✅ Búsqueda completada: 5 datasets encontrados en Kaggle"
}
```

### Errores Posibles

**❌ Error 400: Query inválida**
```json
{
  "error": "Query debe tener al menos 3 caracteres"
}
```

**❌ Error 401: Credenciales no configuradas**
```json
{
  "error": "Credenciales de Kaggle no configuradas",
  "instrucciones": [
    "1. Crear cuenta en https://www.kaggle.com",
    "2. Ir a Settings → Account → API → Create New API Token",
    "3. Descargar kaggle.json",
    "4. Guardar en ~/.kaggle/kaggle.json",
    "5. En Windows: C:\\Users\\{usuario}\\.kaggle\\kaggle.json"
  ]
}
```

**❌ Error 501: Librería no instalada**
```json
{
  "error": "Librería kaggle no instalada",
  "instrucciones": "Ejecuta: pip install kaggle"
}
```

---

## 🔌 Ejemplo desde Python

```python
import requests
import json

def buscar_datasets_kaggle(query, num_resultados=10):
    """Busca datasets en Kaggle desde Python"""
    
    url = "http://localhost:5000/api/buscar-datasets/kaggle"
    
    payload = {
        "query": query,
        "num_resultados": num_resultados,
        "sort_by": "votes"
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"\n📊 Resultados para: '{query}'")
        print(f"Encontrados: {data['cantidad']} datasets\n")
        
        for dataset in data['resultados']:
            print(f"✓ {dataset['titulo']}")
            print(f"  📝 {dataset['descripcion']}")
            print(f"  🔗 {dataset['url']}")
            print(f"  ⬇️  {dataset['descargas']} descargas | 👍 {dataset['votos']} votos")
            print(f"  👤 Por: {dataset['creador']}")
            print()
    else:
        print(f"Error {response.status_code}: {response.json()}")

# Usar
buscar_datasets_kaggle("periódicos historia españa", 10)
```

---

## 🐳 Para Docker

Si usas Docker, asegúrate de:

1. **Montar el directorio .kaggle:**
```yaml
services:
  backend:
    volumes:
      - ~/.kaggle:/root/.kaggle:ro
```

2. **O copiar kaggle.json en el Dockerfile:**
```dockerfile
COPY kaggle.json /root/.kaggle/kaggle.json
RUN chmod 600 /root/.kaggle/kaggle.json
```

---

## ✅ Verificar Instalación

```bash
# Desde el contenedor
docker-compose exec backend python -c "from kaggle.api.kaggle_api_extended import KaggleApi; print('✓ Kaggle OK')"

# O desde Python local
python -c "from kaggle.api.kaggle_api_extended import KaggleApi; print('✓ Kaggle OK')"
```

---

## 📚 Referencias

- [Documentación oficial de Kaggle API](https://github.com/Kaggle/kaggle-api)
- [Datasets populares de Kaggle](https://www.kaggle.com/datasets)
- [API Reference](https://www.kaggle.com/docs/api)
