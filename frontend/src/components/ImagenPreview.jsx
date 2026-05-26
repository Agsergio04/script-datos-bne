import { useState } from 'react';

/**
 * Previsualización de imagen con fallback accesible.
 * Muestra la imagen relacionada (portada de obra / retrato de autor) extraída
 * de datos.bne.es. Si no hay URL o la imagen falla al cargar, muestra un
 * placeholder con la inicial y una etiqueta accesible (role="img").
 *
 * Props:
 *   src   - URL de la imagen (imagen_url)
 *   alt   - texto alternativo
 *   size  - 'sm' | 'md' | 'lg'
 *   tipo  - 'obra' | 'autor'  (contexto para la etiqueta accesible)
 */
export default function ImagenPreview({ src, alt = '', size = 'md', tipo = 'obra' }) {
    const [error, setError] = useState(false);

    if (!src || error) {
        const inicial = (alt || '').trim().charAt(0).toUpperCase() || '·';
        const etiqueta = alt ? `Sin imagen de ${tipo}: ${alt}` : `Sin imagen de ${tipo}`;
        return (
            <div
                className={`imagen-preview imagen-preview--${size} imagen-preview--placeholder`}
                role="img"
                aria-label={etiqueta}
            >
                <span aria-hidden="true">{inicial}</span>
            </div>
        );
    }

    return (
        <img
            src={src}
            alt={alt}
            loading="lazy"
            onError={() => setError(true)}
            className={`imagen-preview imagen-preview--${size}`}
        />
    );
}
