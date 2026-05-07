# 🌐 Guía de Parámetros URL - Frontend BNE

> Cómo pasar URL del proyecto o nombre del periódico directamente al frontend

## 📋 Tabla de Contenidos

1. [Parámetros Disponibles](#parámetros-disponibles)
2. [Ejemplos Básicos](#ejemplos-básicos)
3. [Casos de Uso](#casos-de-uso)
4. [Codificación URL](#codificación-url)
5. [Integración](#integración)

---

## 🔑 Parámetros Disponibles

### Parámetro `url`

**Descripción:** URL directa de la obra en datos.bne.es

**Formato:**
```
?url=https://datos.bne.es/data/XX0000000
```

**Comportamiento:**
1. Frontend detecta el parámetro
2. Completa el campo "Por URL" automáticamente
3. Envía la solicitud de importación
4. Muestra resultado

**Ejemplo:**
```
http://localhost:3000/?url=https://datos.bne.es/data/XX123456
```

---

### Parámetro `titulo`

**Descripción:** Título de la obra o periódico para buscar

**Formato:**
```
?titulo=El%20Quijote
```

**Comportamiento:**
1. Frontend detecta el parámetro
2. Completa el campo "Por Título" automáticamente
3. Envía la búsqueda e importación
4. Muestra resultado

**Ejemplo:**
```
http://localhost:3000/?titulo=El%20Quijote
http://localhost:3000/?titulo=ABC
http://localhost:3000/?titulo=La%20Regenta
```

---

### Parámetro `periodicode` (Alias)

**Descripción:** Alias de `titulo`, útil para nombres de periódicos

**Formato:**
```
?periodicode=ABC
```

**Comportamiento:** Idéntico a `titulo`

**Ejemplo:**
```
http://localhost:3000/?periodicode=ABC
http://localhost:3000/?periodicode=La%20Vanguardia
```

---

## 📝 Ejemplos Básicos

### 1. URL Directa - Quijote

```
http://localhost:3000/?url=https://datos.bne.es/data/XX0000000
```

El frontend importará automáticamente.

### 2. Por Título - El Quijote

```
http://localhost:3000/?titulo=El%20Quijote
```

Busca y importa automáticamente.

### 3. Por Periódico - ABC

```
http://localhost:3000/?titulo=ABC
```

o

```
http://localhost:3000/?periodicode=ABC
```

Busca el periódico ABC e importa.

### 4. Teatro - Bodas de Sangre

```
http://localhost:3000/?titulo=Bodas%20de%20sangre
```

### 5. Literatura - La Regenta

```
http://localhost:3000/?titulo=La%20Regenta
```

---

## 💼 Casos de Uso

### Caso 1: Widget para Importar Obra Específica

Crear un botón que abre el frontend con eine obra pre-seleccionada:

```html
<!-- En tu aplicación -->
<a href="http://localhost:3000/?titulo=El%20Quijote" 
   class="btn btn-primary" 
   target="_blank">
  📚 Importar El Quijote
</a>
```

Cuando el usuario hacer clic, se abre el frontend y se importa automáticamente.

---

### Caso 2: Enlace desde datos.bne.es

Si descubres una obra interesante en datos.bne.es y quieres importarla:

```
Copia la URL: https://datos.bne.es/data/XX123456
Crea el enlace: http://localhost:3000/?url=https://datos.bne.es/data/XX123456
Compartir con otros
```

---

### Caso 3: Búsqueda de Periódicos

Para importar periódicos históricos de forma rápida:

```html
<button onclick="window.open('http://localhost:3000/?titulo=ABC', '_blank')">
  ABC
</button>

<button onclick="window.open('http://localhost:3000/?titulo=La%20Vanguardia', '_blank')">
  La Vanguardia
</button>

<button onclick="window.open('http://localhost:3000/?titulo=El%20Pa%C3%ADs', '_blank')">
  El País
</button>
```

---

### Caso 4: Tabla de Obras Importables

```html
<table>
  <tr>
    <th>Obra</th>
    <th>Acción</th>
  </tr>
  <tr>
    <td>El Quijote</td>
    <td>
      <a href="http://localhost:3000/?titulo=El%20Quijote">
        Importar
      </a>
    </td>
  </tr>
  <tr>
    <td>La Regenta</td>
    <td>
      <a href="http://localhost:3000/?titulo=La%20Regenta">
        Importar
      </a>
    </td>
  </tr>
</table>
```

---

### Caso 5: API Automático - JavaScript

```javascript
// Función para importar una obra
function importarObra(titulo) {
    const url = new URL('http://localhost:3000/');
    url.searchParams.set('titulo', titulo);
    window.open(url.toString(), '_blank');
}

// Usos
importarObra('El Quijote');
importarObra('ABC');
importarObra('La Vanguardia');
```

---

### Caso 6: Iframe Embebido

```html
<!-- Embeber el frontend en otra página -->
<iframe 
    src="http://localhost:3000/?titulo=El%20Quijote" 
    style="width: 100%; height: 600px; border: none;">
</iframe>
```

---

## 🔤 Codificación URL

### Caracteres Especiales

Algunos caracteres necesitan ser codificados en URLs:

| Carácter | Código | Ejemplo |
|----------|--------|---------|
| Espacio | `%20` | `El%20Quijote` |
| Á | `%C3%81` | `La%20Arquer%C3%ADa` |
| É | `%C3%89` | `Poes%C3%ADa` |
| Í | `%C3%8D` | - |
| Ó | `%C3%93` | - |
| Ú | `%C3%9A` | - |
| ñ | `%C3%B1` | `Se%C3%B1a` |
| & | `%26` | - |
| ? | `%3F` | - |
| = | `%3D` | - |

### Herramientas

**Online:**
- https://www.urlencoder.org/
- https://www.url-encode-decode.com/

**JavaScript:**
```javascript
const titulo = "La Arquerïa";
const encoded = encodeURIComponent(titulo);
const url = `http://localhost:3000/?titulo=${encoded}`;
console.log(url);
// http://localhost:3000/?titulo=La%20Arquer%C3%ADa
```

**Python:**
```python
from urllib.parse import urlencode

params = {'titulo': 'La Arquerïa'}
url = f"http://localhost:3000/?{urlencode(params)}"
print(url)
# http://localhost:3000/?titulo=La+Arquer%C3%ADa
```

---

## 🔗 Integración

### 1. Con HTML Puro

```html
<!-- Botón simple -->
<a href="http://localhost:3000/?titulo=El%20Quijote">
  Importar El Quijote
</a>

<!-- O formulario -->
<form action="http://localhost:3000/" method="get" target="_blank">
    <input type="hidden" name="titulo" value="El Quijote">
    <button type="submit">Importar</button>
</form>
```

### 2. Con JavaScript

```javascript
// Función reutilizable
function abrirImportador(tipo, valor) {
    const url = new URL('http://localhost:3000/');
    url.searchParams.set(tipo, valor);
    window.open(url.toString(), '_blank');
}

// Uso
document.getElementById('importar-btn').addEventListener('click', () => {
    abrirImportador('titulo', 'El Quijote');
});
```

### 3. Con React

```jsx
import { useNavigate } from 'react-router-dom';

export function ImportarObr() {
    const navigate = useNavigate();
    
    const handleImportarObra = (titulo) => {
        const baseUrl = 'http://localhost:3000';
        const params = new URLSearchParams({ titulo });
        window.open(`${baseUrl}?${params}`, '_blank');
    };

    return (
        <button onClick={() => handleImportarObra('El Quijote')}>
            Importar
        </button>
    );
}
```

### 4. Con Vue

```vue
<template>
    <button @click="importarObra('El Quijote')">
        Importar
    </button>
</template>

<script setup>
function importarObra(titulo) {
    const url = new URL('http://localhost:3000/');
    url.searchParams.set('titulo', titulo);
    window.open(url.href, '_blank');
}
</script>
```

### 5. Con Angular

```typescript
export class ImportarComponent {
    importarObra(titulo: string) {
        const url = new URL('http://localhost:3000/');
        url.searchParams.set('titulo', titulo);
        window.open(url.toString(), '_blank');
    }
}
```

---

## 📊 Flujo de Importación con Parámetros

```
┌─────────────────────────────────────┐
│ Usuario hace clic en enlace         │
│ http://localhost:3000/?titulo=Quij. │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Frontend carga con parámetros       │
│ useQueryParams() lee URL            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ useEffect detecta parametros        │
│ Completa formulario automáticamente │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Llama a endpoint API                │
│ POST /api/importar/titulo           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Backend busca en datos.bne.es       │
│ Extrae metadatos                    │
│ Inserta en BD                       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Frontend muestra resultado           │
│ ✅ Importada                        │
│ o ℹ️ Ya existe                      │
└─────────────────────────────────────┘
```

---

## 🔍 Debugging

### Ver Parámetros en Console

```javascript
// En la consola del navegador
console.log(window.location.search);
// Output: ?titulo=El%20Quijote

// Decodificar
const params = new URLSearchParams(window.location.search);
console.log(params.get('titulo'));
// Output: El Quijote
```

### Verificar URL correcta

```
✅ Correcto:
http://localhost:3000/?titulo=El%20Quijote
http://localhost:3000/?url=https://datos.bne.es/data/XX123456

❌ Incorrecto:
http://localhost:3000/?titulo=El Quijote      (sin codificación)
http://localhost:3000?titulo=El%20Quijote     (sin /)
http://localhost:3000/?titulo ==El Quijote    (caracteres especiales)
```

---

## 📱 URLs Completas para Copiar/Pegar

```
# Quijote
http://localhost:3000/?titulo=El%20Quijote

# ABC
http://localhost:3000/?titulo=ABC

# La Vanguardia
http://localhost:3000/?titulo=La%20Vanguardia

# Bodas de Sangre
http://localhost:3000/?titulo=Bodas%20de%20sangre

# Periódico con URL exacta
http://localhost:3000/?url=https://datos.bne.es/data/XX0000000
```

---

**¡Listo!** 🎉 Ya sabes cómo pasar parámetros al frontend.
