import FieldLabel from './FieldLabel';
import ImagenPreview from './ImagenPreview';

function Campo({ icon, text, value }) {
    if (!value) return null;
    return (
        <div>
            <FieldLabel icon={icon} text={text} />
            <p className="field-value">{value}</p>
        </div>
    );
}

export default function ObraDetalleCard({ obra, fuente }) {
    return (
        <div className="obra-card">
            <div className="obra-card__head">
                <ImagenPreview src={obra.imagen_url} alt={obra.titulo} size="lg" tipo="obra" />
                <div className="obra-card__heading">
                    <p className="obra-card__title">{obra.titulo}</p>
                    <div className="obra-card__tags">
                        <span className="obra-card__tag">ID: {obra.id}</span>
                        {fuente && <span className="obra-card__tag obra-card__tag--source">{fuente}</span>}
                    </div>
                </div>
            </div>

            <div className="obra-card__grid">
                <Campo icon="👤" text="Autor"    value={obra.nombre_autor} />
                <Campo icon="✍️" text="Firma"    value={obra.autor_firma} />
                <Campo icon="📅" text="Año"      value={obra.anio} />
                <Campo icon="📆" text="Fecha"    value={obra.fecha} />
                <Campo icon="🏷️" text="Tipo"    value={obra.tipo_publicacion} />
                <Campo icon="🎯" text="Tema"     value={obra.tema_principal} />
                <Campo icon="🖨️" text="Imprenta" value={obra.imprenta} />
                <Campo icon="📍" text="Lugar"    value={obra.lugar_impresion} />
                <Campo icon="📖" text="Páginas"  value={obra.paginas} />
                <Campo icon="🌐" text="Idioma"   value={obra.idioma} />
                <Campo icon="💾" text="Formato"  value={obra.formato} />
                <Campo icon="⚖️" text="Derechos" value={obra.derechos} />
            </div>

            {obra.como_citar && (
                <div className="obra-card__cite">
                    <FieldLabel icon="📚" text="Cómo citar" />
                    <p className="obra-card__cite-text">{obra.como_citar}</p>
                </div>
            )}

            {obra.enlace && (
                <div className="obra-card__footer">
                    <a href={obra.enlace} target="_blank" rel="noopener noreferrer" className="obra-card__link">
                        🔗 Ver en BNE
                    </a>
                </div>
            )}
        </div>
    );
}
