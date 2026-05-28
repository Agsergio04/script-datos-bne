import { useState } from 'react';
import { API_BASE_URL } from '../constants';
import FieldLabel from './FieldLabel';
import ImagenPreview from './ImagenPreview';

function Campo({ text, value }) {
    if (!value) return null;
    return (
        <div>
            <FieldLabel text={text} />
            <p className="field-value">{value}</p>
        </div>
    );
}

export default function ObraDetalleCard({ obra, fuente }) {
    const [imagen, setImagen] = useState(obra.imagen_url || '');
    const [editando, setEditando] = useState(false);
    const [valor, setValor] = useState(obra.imagen_url || '');
    const [guardando, setGuardando] = useState(false);
    const [error, setError] = useState(null);

    const guardarImagen = async () => {
        if (!obra.id) return;
        setGuardando(true); setError(null);
        try {
            const res = await fetch(`${API_BASE_URL}/api/obras/${obra.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ imagen_url: valor.trim() || null }),
            });
            if (!res.ok) { const e = await res.json().catch(() => ({})); throw new Error(e.error || `Error ${res.status}`); }
            setImagen(valor.trim());
            setEditando(false);
        } catch (e) { setError(e.message); } finally { setGuardando(false); }
    };

    return (
        <div className="obra-card">
            <div className="obra-card__head">
                <ImagenPreview src={imagen} alt={obra.titulo} size="lg" tipo="obra" />
                <div className="obra-card__heading">
                    <p className="obra-card__title">{obra.titulo}</p>
                    <div className="obra-card__tags">
                        <span className="obra-card__tag">ID: {obra.id}</span>
                        {fuente && <span className="obra-card__tag obra-card__tag--source">{fuente}</span>}
                    </div>
                    {obra.id && (
                        <button
                            type="button"
                            className="obra-card__edit-toggle"
                            aria-expanded={editando}
                            onClick={() => { setValor(imagen || ''); setError(null); setEditando(v => !v); }}
                        >
                            {editando ? 'Cancelar' : 'Editar imagen'}
                        </button>
                    )}
                </div>
            </div>

            {editando && (
                <div className="obra-card__edit">
                    <label className="field-label" htmlFor={`img-${obra.id}`}>URL de la imagen</label>
                    <div className="obra-card__edit-row">
                        <input
                            id={`img-${obra.id}`}
                            type="text"
                            className="form__input"
                            value={valor}
                            onChange={e => setValor(e.target.value)}
                            placeholder="https://… (p. ej. portada de la Hemeroteca)"
                            onKeyPress={e => e.key === 'Enter' && guardarImagen()}
                        />
                        <button type="button" className="button button--primary" onClick={guardarImagen} disabled={guardando}>
                            {guardando ? 'Guardando…' : 'Guardar'}
                        </button>
                    </div>
                    {error && <p className="search-box__error" role="alert"><strong>Error:</strong> {error}</p>}
                </div>
            )}

            <div className="obra-card__grid">
                <Campo text="Autor"    value={obra.nombre_autor} />
                <Campo text="Firma"    value={obra.autor_firma} />
                <Campo text="Año"      value={obra.anio} />
                <Campo text="Fecha"    value={obra.fecha} />
                <Campo text="Tipo"     value={obra.tipo_publicacion} />
                <Campo text="Tema"     value={obra.tema_principal} />
                <Campo text="Imprenta" value={obra.imprenta} />
                <Campo text="Lugar"    value={obra.lugar_impresion} />
                <Campo text="Páginas"  value={obra.paginas} />
                <Campo text="Idioma"   value={obra.idioma} />
                <Campo text="Formato"  value={obra.formato} />
                <Campo text="Derechos" value={obra.derechos} />
            </div>

            {obra.como_citar && (
                <div className="obra-card__cite">
                    <FieldLabel text="Cómo citar" />
                    <p className="obra-card__cite-text">{obra.como_citar}</p>
                </div>
            )}

            {obra.enlace && (
                <div className="obra-card__footer">
                    <a href={obra.enlace} target="_blank" rel="noopener noreferrer" className="obra-card__link">
                        Ver en datos.bne.es
                    </a>
                </div>
            )}
        </div>
    );
}
