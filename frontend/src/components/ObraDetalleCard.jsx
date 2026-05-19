import FieldLabel from './FieldLabel';

export default function ObraDetalleCard({ obra, fuente }) {
    return (
        <div className="bg-white rounded-lg border border-stone-200 border-l-4 border-l-amber-500 p-5 hover:shadow-md transition-shadow">
            <div className="mb-3 pb-3 border-b border-stone-100">
                <p className="font-serif font-bold text-stone-800 text-lg leading-snug">{obra.titulo}</p>
                <div className="flex gap-2 mt-2 flex-wrap">
                    <span className="text-xs bg-stone-100 text-stone-600 px-2 py-0.5 rounded-full border border-stone-200">
                        ID: {obra.id}
                    </span>
                    {fuente && (
                        <span className="text-xs bg-amber-50 text-amber-700 px-2 py-0.5 rounded-full border border-amber-200">
                            {fuente}
                        </span>
                    )}
                </div>
            </div>

            <div className="grid grid-cols-2 gap-3 text-sm">
                {obra.nombre_autor     && <div><FieldLabel icon="👤" text="Autor"    /><p className="text-stone-700">{obra.nombre_autor}</p></div>}
                {obra.autor_firma      && <div><FieldLabel icon="✍️" text="Firma"    /><p className="text-stone-700">{obra.autor_firma}</p></div>}
                {obra.anio             && <div><FieldLabel icon="📅" text="Año"      /><p className="text-stone-700">{obra.anio}</p></div>}
                {obra.fecha            && <div><FieldLabel icon="📆" text="Fecha"    /><p className="text-stone-700">{obra.fecha}</p></div>}
                {obra.tipo_publicacion && <div><FieldLabel icon="🏷️" text="Tipo"    /><p className="text-stone-700">{obra.tipo_publicacion}</p></div>}
                {obra.tema_principal   && <div><FieldLabel icon="🎯" text="Tema"     /><p className="text-stone-700">{obra.tema_principal}</p></div>}
                {obra.imprenta         && <div><FieldLabel icon="🖨️" text="Imprenta"/><p className="text-stone-700">{obra.imprenta}</p></div>}
                {obra.lugar_impresion  && <div><FieldLabel icon="📍" text="Lugar"    /><p className="text-stone-700">{obra.lugar_impresion}</p></div>}
                {obra.paginas          && <div><FieldLabel icon="📖" text="Páginas"  /><p className="text-stone-700">{obra.paginas}</p></div>}
                {obra.idioma           && <div><FieldLabel icon="🌐" text="Idioma"   /><p className="text-stone-700">{obra.idioma}</p></div>}
                {obra.formato          && <div><FieldLabel icon="💾" text="Formato"  /><p className="text-stone-700">{obra.formato}</p></div>}
                {obra.derechos         && <div><FieldLabel icon="⚖️" text="Derechos"/><p className="text-stone-700">{obra.derechos}</p></div>}
            </div>

            {obra.como_citar && (
                <div className="mt-4 pt-3 border-t border-stone-100">
                    <FieldLabel icon="📚" text="Cómo citar" />
                    <p className="text-stone-600 text-xs bg-stone-50 p-2 rounded font-mono mt-1 border border-stone-100">
                        {obra.como_citar}
                    </p>
                </div>
            )}

            <div className="mt-3 pt-3 border-t border-stone-100 flex gap-2 flex-wrap">
                {obra.enlace && (
                    <a href={obra.enlace} target="_blank" rel="noopener noreferrer"
                        className="text-xs bg-stone-100 text-stone-600 hover:bg-amber-50 hover:text-amber-700 px-3 py-1.5 rounded-full border border-stone-200 transition-colors">
                        🔗 Ver en BNE
                    </a>
                )}
            </div>
        </div>
    );
}
