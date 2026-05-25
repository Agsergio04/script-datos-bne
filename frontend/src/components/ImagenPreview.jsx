import { useState } from 'react';

/**
 * Previsualización de imagen con fallback.
 * Muestra la imagen relacionada (portada de obra / retrato de autor) extraída
 * de datos.bne.es. Si no hay URL o la imagen falla al cargar, muestra un
 * placeholder con un icono según el tipo.
 *
 * Props:
 *   src   - URL de la imagen (imagen_url)
 *   alt   - texto alternativo
 *   size  - 'sm' | 'md' | 'lg'
 *   tipo  - 'obra' | 'autor'  (define el icono del placeholder)
 */
export default function ImagenPreview({ src, alt = '', size = 'md', tipo = 'obra' }) {
    const [error, setError] = useState(false);
    const placeholderIcon = tipo === 'autor' ? '👤' : '📄';

    if (!src || error) {
        return (
            <div
                className={`imagen-preview imagen-preview--${size} imagen-preview--placeholder`}
                title="Sin imagen disponible"
            >
                {placeholderIcon}
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
