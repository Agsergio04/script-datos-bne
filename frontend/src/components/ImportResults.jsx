import LoadingSpinner from './LoadingSpinner';
import SectionHeader from './SectionHeader';
import ObraDetalleCard from './ObraDetalleCard';
import ListaObras from './ListaObras';
import FieldLabel from './FieldLabel';
import EmptyState from './EmptyState';

export default function ImportResults({ resultado, loading, error }) {
    if (loading) return (
        <div className="bg-white border border-stone-200 p-6 rounded-xl shadow-sm">
            <LoadingSpinner />
        </div>
    );

    if (error) return (
        <div className="bg-red-50 border border-red-200 p-5 rounded-xl">
            <p className="text-red-700 font-medium">❌ {error}</p>
        </div>
    );

    if (!resultado) return null;

    // Búsqueda por nombre
    if (resultado.nombre_buscado) {
        const {
            nombre_buscado,
            resultados_bd_local = [],
            guardadas = [],
            ya_en_bd = [],
            errores_bne = [],
            total_encontrados,
        } = resultado;
        const resultados_bd = resultados_bd_local.length > 0 ? resultados_bd_local : (resultado.resultados_bd || []);

        return (
            <div className="space-y-5">
                <div className="bg-amber-50 border border-amber-200 p-4 rounded-xl">
                    <p className="text-amber-800 font-medium">
                        🔎 Búsqueda: "<strong>{nombre_buscado}</strong>" —{' '}
                        <strong className="text-amber-700">{total_encontrados}</strong> resultados encontrados
                    </p>
                    {resultado.mensaje && <p className="text-amber-700 text-sm mt-1 italic">{resultado.mensaje}</p>}
                </div>

                {(guardadas.length > 0 || ya_en_bd.length > 0 || errores_bne.length > 0) && (
                    <div className="grid grid-cols-3 gap-3">
                        <div className="bg-white border border-emerald-200 p-4 rounded-xl text-center">
                            <p className="text-emerald-600 font-bold text-3xl font-serif">{guardadas.length}</p>
                            <p className="text-emerald-700 text-xs font-semibold tracking-wide uppercase mt-1">Nuevas guardadas</p>
                        </div>
                        <div className="bg-white border border-amber-200 p-4 rounded-xl text-center">
                            <p className="text-amber-600 font-bold text-3xl font-serif">{ya_en_bd.length}</p>
                            <p className="text-amber-700 text-xs font-semibold tracking-wide uppercase mt-1">Ya en BD</p>
                        </div>
                        <div className="bg-white border border-red-200 p-4 rounded-xl text-center">
                            <p className="text-red-600 font-bold text-3xl font-serif">{errores_bne.length}</p>
                            <p className="text-red-700 text-xs font-semibold tracking-wide uppercase mt-1">Errores</p>
                        </div>
                    </div>
                )}

                {resultados_bd.length > 0 && (
                    <div>
                        <SectionHeader color="stone" label="Base de Datos Local" count={resultados_bd.length} />
                        <div className="space-y-3">
                            {resultados_bd.map((obra, idx) => <ObraDetalleCard key={idx} obra={obra} fuente="📍 BD Local" />)}
                        </div>
                    </div>
                )}

                {guardadas.length > 0 && (
                    <div>
                        <SectionHeader color="emerald" label="Nuevas obras guardadas desde BNE" count={guardadas.length} />
                        <ListaObras obras={guardadas} dotColor="bg-emerald-500" showLink />
                    </div>
                )}

                {ya_en_bd.length > 0 && (
                    <div>
                        <SectionHeader color="amber" label="Ya existían en BD" count={ya_en_bd.length} />
                        <ListaObras obras={ya_en_bd} dotColor="bg-amber-400" />
                    </div>
                )}

                {errores_bne.length > 0 && (
                    <div>
                        <SectionHeader color="red" label="Errores" count={errores_bne.length} />
                        <div className="bg-white border border-red-200 rounded-xl overflow-hidden">
                            {errores_bne.map((err, idx) => (
                                <div key={idx} className={`flex items-start gap-3 px-5 py-3 text-sm ${idx < errores_bne.length - 1 ? 'border-b border-stone-100' : ''}`}>
                                    <span className="w-1.5 h-1.5 bg-red-400 rounded-full flex-shrink-0 mt-1.5" />
                                    <span className="text-red-700">
                                        <span className="font-medium">{err.titulo}</span>: {err.error}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {total_encontrados === 0 && (
                    <EmptyState
                        icon="🔍"
                        title={`Sin resultados para "${nombre_buscado}"`}
                        description="Prueba con otro término o revisa la ortografía"
                    />
                )}
            </div>
        );
    }

    // Importación individual (url o titulo)
    if (resultado.data) {
        const obra = resultado.data;
        const fuente = resultado.fuente;
        const esNueva = resultado.message.includes('importada') && !resultado.message.includes('existe');

        let borderColor, tagBg, tagText, icon;
        if (esNueva) {
            borderColor = 'border-l-emerald-500'; tagBg = 'bg-emerald-50'; tagText = 'text-emerald-700'; icon = '✅';
        } else if (fuente === 'BD local') {
            borderColor = 'border-l-amber-500'; tagBg = 'bg-amber-50'; tagText = 'text-amber-700'; icon = '📚';
        } else {
            borderColor = 'border-l-stone-400'; tagBg = 'bg-stone-50'; tagText = 'text-stone-700'; icon = 'ℹ️';
        }

        return (
            <div className={`bg-white border border-stone-200 border-l-4 ${borderColor} p-6 rounded-xl shadow-sm`}>
                <div className="flex items-start gap-4">
                    <span className="text-2xl flex-shrink-0 mt-0.5">{icon}</span>
                    <div className="flex-1">
                        <p className="font-serif font-bold text-lg text-stone-800 mb-2">{resultado.message}</p>
                        {fuente && (
                            <span className={`inline-block text-xs ${tagBg} ${tagText} px-2.5 py-1 rounded-full border border-stone-200 mb-4`}>
                                📍 {fuente}
                            </span>
                        )}
                        <div className="grid grid-cols-2 gap-3 text-sm pt-3 border-t border-stone-100">
                            <div><FieldLabel icon="📖" text="Título" /><p className="text-stone-700">{obra.titulo}</p></div>
                            <div><FieldLabel icon="✍️" text="Autor"  /><p className="text-stone-700">{obra.nombre_autor || 'N/A'}</p></div>
                            <div><FieldLabel icon="📅" text="Año"    /><p className="text-stone-700">{obra.anio || 'N/A'}</p></div>
                            <div><FieldLabel icon="🏷️" text="Tipo"  /><p className="text-stone-700">{obra.tipo_publicacion || 'N/A'}</p></div>
                            <div><FieldLabel icon="🆔" text="ID"     /><p className="text-stone-700">{obra.id}</p></div>
                            {obra.enlace && (
                                <div>
                                    <FieldLabel icon="🔗" text="Enlace" />
                                    <a href={obra.enlace} target="_blank" rel="noopener noreferrer"
                                        className="text-amber-600 hover:text-amber-800 hover:underline text-sm">
                                        Ver en datos.bne.es ↗
                                    </a>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    // Importación en lote
    if (resultado.estadisticas) {
        const stats = resultado.estadisticas;
        return (
            <div className="space-y-5">
                <div className="bg-white border border-stone-200 p-6 rounded-xl shadow-sm">
                    <h3 className="font-serif font-bold text-stone-800 text-xl mb-5">Estadísticas del lote</h3>
                    <div className="grid grid-cols-2 gap-4">
                        <div className="bg-stone-50 border border-stone-200 p-4 rounded-xl text-center">
                            <p className="text-stone-700 font-bold text-3xl font-serif">{stats.total}</p>
                            <p className="text-stone-500 text-xs tracking-wide uppercase mt-1">Total procesadas</p>
                        </div>
                        <div className="bg-white border border-emerald-200 p-4 rounded-xl text-center">
                            <p className="text-emerald-600 font-bold text-3xl font-serif">{stats.importadas}</p>
                            <p className="text-emerald-600 text-xs tracking-wide uppercase mt-1">Nuevas importadas</p>
                        </div>
                        <div className="bg-white border border-amber-200 p-4 rounded-xl text-center">
                            <p className="text-amber-600 font-bold text-3xl font-serif">{stats.existentes}</p>
                            <p className="text-amber-600 text-xs tracking-wide uppercase mt-1">Ya existentes</p>
                        </div>
                        <div className="bg-white border border-red-200 p-4 rounded-xl text-center">
                            <p className="text-red-600 font-bold text-3xl font-serif">{stats.errores}</p>
                            <p className="text-red-600 text-xs tracking-wide uppercase mt-1">Errores</p>
                        </div>
                    </div>
                </div>

                {resultado.resultados.importadas.length > 0 && (
                    <div>
                        <SectionHeader color="emerald" label="Nuevas Importadas" count={resultado.resultados.importadas.length} />
                        <div className="bg-white border border-stone-200 rounded-xl overflow-hidden">
                            {resultado.resultados.importadas.map((obra, idx) => (
                                <div key={idx} className={`flex items-center gap-3 px-5 py-3 text-sm ${idx < resultado.resultados.importadas.length - 1 ? 'border-b border-stone-100' : ''}`}>
                                    <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full flex-shrink-0" />
                                    <span className="text-stone-800 font-medium flex-1">{obra.titulo}</span>
                                    <span className="text-stone-400 text-xs">ID: {obra.id}</span>
                                    <span className="text-xs text-stone-400">📥 {obra.fuente || 'datos.bne.es'}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {resultado.resultados.existentes.length > 0 && (
                    <div>
                        <SectionHeader color="amber" label="Ya Existentes" count={resultado.resultados.existentes.length} />
                        <div className="bg-white border border-stone-200 rounded-xl overflow-hidden">
                            {resultado.resultados.existentes.map((obra, idx) => (
                                <div key={idx} className={`flex items-center gap-3 px-5 py-3 text-sm ${idx < resultado.resultados.existentes.length - 1 ? 'border-b border-stone-100' : ''}`}>
                                    <span className="w-1.5 h-1.5 bg-amber-400 rounded-full flex-shrink-0" />
                                    <span className="text-stone-700 flex-1">{obra.titulo}</span>
                                    <span className="text-stone-400 text-xs">📍 {obra.fuente || 'BD'}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {resultado.resultados.errores.length > 0 && (
                    <div>
                        <SectionHeader color="red" label="Errores" count={resultado.resultados.errores.length} />
                        <div className="bg-white border border-red-200 rounded-xl overflow-hidden">
                            {resultado.resultados.errores.map((error, idx) => (
                                <div key={idx} className={`flex items-start gap-3 px-5 py-3 text-sm ${idx < resultado.resultados.errores.length - 1 ? 'border-b border-stone-100' : ''}`}>
                                    <span className="w-1.5 h-1.5 bg-red-400 rounded-full flex-shrink-0 mt-1.5" />
                                    <span className="text-red-700">
                                        <span className="font-medium">{error.origen}</span>: {error.error}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        );
    }

    return null;
}
