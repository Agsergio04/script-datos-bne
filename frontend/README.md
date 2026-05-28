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

## 🎨 Estilos (CSS + metodología BEM)

Los estilos están en **CSS plano** organizados con la metodología **BEM**
(Block · Element · Modifier) dentro de la carpeta [`src/styles/`](src/styles).
**No se usa Tailwind**: todas las clases siguen la nomenclatura
`bloque__elemento--modificador`.

### Estructura de `src/styles/`

| Archivo           | Contenido |
|-------------------|-----------|
| `index.css`       | Punto de entrada. Importa el resto en orden con `@import`. |
| `variables.css`   | *Design tokens*: paleta de color, tipografías, radios y sombras como variables CSS (`--color-stone-700`, `--font-serif`, …). |
| `base.css`        | Reset ligero, estilos base del `body` y la animación del spinner. |
| `layout.css`      | Bloques de estructura: `app`, `site-header`, `site-nav`, `site-footer`, `page`. |
| `components.css`  | Bloques reutilizables: `panel`, `stat-card`, `bar-chart`, `obra-card`, `obra-list`, `imagen-preview`, `import-card`, etc. |
| `pages.css`       | Formularios (`form`), botones (`button`), pestañas (`tabs`), paginación y estilos por página. |

### Convención BEM

```css
.obra-card            { /* Bloque: componente independiente */ }
.obra-card__title     { /* Elemento: parte del bloque */ }
.obra-card__tag--source { /* Modificador: variante del elemento */ }
```

```jsx
<div className="obra-card">
  <p className="obra-card__title">…</p>
  <span className="obra-card__tag obra-card__tag--source">BNE</span>
</div>
```

### Cómo añadir estilos

1. Si es un componente nuevo, crea su bloque BEM en `components.css` (o el archivo que corresponda).
2. Reutiliza los *tokens* de `variables.css` (`var(--color-…)`) en lugar de valores fijos.
3. Aplica las clases con `className="bloque__elemento bloque__elemento--modificador"` en el JSX.

- ✅ Sin dependencia de Tailwind (CSS más ligero)
- ✅ Tokens centralizados → fácil cambiar la paleta
- ✅ Animaciones suaves y estados de carga
- ✅ Tipografía serif (Playfair Display) cargada desde Google Fonts en `public/index.html`

## 📱 Ejemplo HTML Manual

Si preferis versión sin build tools:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Importar Obras BNE</title>
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <link rel="stylesheet" href="/styles/index.css">
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
Componente de spinner animado (`.loading-spinner`)

### `ImagenPreview`
Previsualización de imagen con *fallback*. Muestra la portada de una obra o el
retrato de un autor (`imagen_url` extraído de datos.bne.es); si no hay imagen o
falla la carga, muestra un placeholder. Props: `src`, `alt`, `size`
(`sm`/`md`/`lg`), `tipo` (`obra`/`autor`).

### `ImportResults`
Muestra resultados de importación:
- Individuales (url/titulo)
- Lote (estadísticas)

### `ObraDetalleCard`
Ficha detallada de una obra. Incluye un botón **"Editar imagen"** que abre un
input para pegar una URL (p. ej. una portada de la Hemeroteca Digital de la BNE)
y la guarda con `PUT /api/obras/<id>`, refrescando la previsualización al
instante. Accesible (`htmlFor`/`id`, `aria-expanded`, errores con `role="alert"`).

### `ListaObras` · `SectionHeader` · `BarChart` · `EmptyState` · `FieldLabel`
Componentes de presentación reutilizables, cada uno con su bloque BEM en `src/styles/`.

### `App`
Componente principal con lógica completa.

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
**Última actualización:** 28 de mayo de 2026
