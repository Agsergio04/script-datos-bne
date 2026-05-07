# 🎨 Frontend - Recogida de Datos BNE

Frontend React para importar obras desde **datos.bne.es** de forma interactiva.

## 🎯 Características

✅ **3 Modos de Importación:**
- 🔗 Por URL directa
- 🔍 Por Título/Periódico
- 📦 En lote (múltiples obras)

✅ **Parámetros URL:**
- Acepta `?url=...` para importar directo
- Acepta `?titulo=...` para buscar automáticamente
- Acepta `?periodicode=...` (alias de titulo)

✅ **Respuestas Visual:**
- Indicadores de éxito/error
- Estadísticas de importación en lote
- Lista detallada de obras importadas

## 🚀 Inicio Rápido

### Con Docker
```bash
docker-compose up frontend
```

Frontend disponible en: **http://localhost:3000**

### Local
```bash
cd frontend
npm install
npm start
```

## 📝 Parámetros de URL

### 1. Importar por URL directa

```
http://localhost:3000/?url=https://datos.bne.es/data/XX0000000
```

El frontend:
1. Detecta el parámetro `url`
2. Completa el formulario automáticamente
3. Presiona enviar automáticamente
4. Muestra el resultado

### 2. Buscar por Título o Periódico

```
http://localhost:3000/?titulo=El%20Quijote
http://localhost:3000/?periodicode=ABC
http://localhost:3000/?titulo=La%20Regenta
```

El frontend:
1. Detecta el parámetro `titulo` o `periodicode`
2. Busca en datos.bne.es
3. Importa automáticamente
4. Muestra resultado

### 3. Combinación de parámetros

```
http://localhost:3000/?url=https://datos.bne.es/data/XX0000000
http://localhost:3000/?titulo=El%20Quijote
```

## 💻 Usos Prácticos

### Caso 1: Compartir un enlace de importación

Quieres que alguien importe rápido una obra específica:

```
https://tudominio.com?titulo=El%20Quijote
```

Al hacer clic, se importa automáticamente.

### Caso 2: URL desde datos.bne.es

Ya tienes la URL exacta:

```
https://tudominio.com?url=https://datos.bne.es/data/XX0000000
```

Se importa directamente.

### Caso 3: Widget embebido

En otra app, crear link que abre el importador:

```html
<a href="http://localhost:3000/?titulo=ABC" target="_blank">
  Importar periódico ABC
</a>
```

## 📊 Interfaz

### Pestañas

1. **🔗 Por URL**
   - Input para URL de datos.bne.es
   - Botón "Importar Obra"
   - Muestra resultado

2. **🔍 Por Título**
   - Input para título o periódico
   - Botón "Buscar e Importar"
   - Sistema busca y importa automáticamente

3. **📦 Lote**
   - Textarea para múltiples títulos/URLs
   - Uno por línea
   - Botón "Importar Lote"
   - Estadísticas consolidadas

### Resultados

**Importación individual (URL/Título):**
- ✅ Obra nuevamente importada (verde)
- ℹ️ Obra ya existe (azul)
- ❌ Error (rojo)

**Importación lote:**
- 📊 Gráfica con estadísticas
- ✅ Lista de importadas
- ℹ️ Lista de existentes
- ❌ Lista de errores

## ⚙️ Configuración

### Variables de Entorno

Crear `.env` en la raíz del frontend:

```env
REACT_APP_API_URL=http://localhost:5000
NODE_ENV=development
REACT_APP_TITULO=Recogida de Datos BNE
```

### Para Producción

```env
REACT_APP_API_URL=https://api.tudominio.com
NODE_ENV=production
```

## 📦 Builder y Build

### Desarrollo
```bash
npm run dev
```

Inicia servidor de desarrollo en puerto 3000

### Producción
```bash
npm run build
```

Genera carpeta `build/` lista para desplegar

## 🔗 Integración con Backend

El frontend se conecta a:

- `POST /api/importar/url` - Importar por URL
- `POST /api/importar/titulo` - Importar por Título
- `POST /api/importar/lote` - Importar Lote

Asegúrate que el backend está corriendo en el puerto configurado (default: 5000)

## 🎨 Estilos

Utiliza **Tailwind CSS** para estilos responsive.

- ✅ Mobile responsive
- ✅ Dark mode compatible
- ✅ Animaciones suaves
- ✅ Estados de carga

## 📱 Ejemplo HTML Manual

Si preferis versión sin build tools:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Importar Obras BNE</title>
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    <div id="app"></div>
    <script src="/App.jsx"></script>
</body>
</html>
```

## 🧪 Testing

```bash
npm test
```

## 📚 Documentación de Componentes

### `useQueryParams()`
Hook que lee parámetros de URL:
- `url` - URL de datos.bne.es
- `titulo` - Título o periódico
- `periodicode` - Alias de titulo

### `LoadingSpinner`
Componente de spinner animado

### `ImportResults`
Muestra resultados de importación:
- Individuales (url/titulo)
- Lote (estadísticas)

### `App`
Componente principal con lógica completa

## 🔍 URLs de Ejemplo

```
# Por URL
http://localhost:3000/?url=https://datos.bne.es/data/XX0000000

# Por Título
http://localhost:3000/?titulo=El%20Quijote

# Por Periódico
http://localhost:3000/?titulo=ABC

# Caracteres especiales (URL encoded)
http://localhost:3000/?titulo=La%20Arquer%C3%ADa
```

## 🐛 Troubleshooting

### "No se conecta a la API"
- Verificar que backend está en puerto 5000
- Revisar `.env` > REACT_APP_API_URL
- Ver logs del backend

### "CORS error"
- Backend debe tener CORS habilitado
- Check flask_cors en app.py

### "Parámetros no se detienen"
- Revisar format: `?titulo=...` o `?url=...`
- Usar URL encoding para caracteres especiales
- Revisar console.log en DevTools

## 📄 Licencia

CC0 - Creative Commons Public Domain

---

**Estado:** ✅ En desarrollo  
**Última actualización:** 14 de abril de 2026
