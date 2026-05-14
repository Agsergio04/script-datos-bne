/**
 * Frontend React - Recogida de Datos BNE
 * Acepta parametros: URL o nombre del periódico/obra
 */

import React, { useState, useEffect } from 'react';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function useQueryParams() {
    const [params, setParams] = useState({
        url: null,
        titulo: null,
        periodicode: null,
        fechaDesde: null,
        fechaHasta: null
    });

    useEffect(() => {
        const searchParams = new URLSearchParams(window.location.search);
        setParams({
            url: searchParams.get('url'),
            titulo: searchParams.get('titulo'),
            periodicode: searchParams.get('periodicode'),
            fechaDesde: searchParams.get('fechaDesde'),
            fechaHasta: searchParams.get('fechaHasta')
        });
    }, []);

    return params;
}

function LoadingSpinner() {
    return (
        <div className="flex items-center justify-center gap-3 py-6">
            <div className="w-2.5 h-2.5 bg-amber-600 rounded-full animate-bounce"></div>
            <div className="w-2.5 h-2.5 bg-amber-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
            <div className="w-2.5 h-2.5 bg-amber-600 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
            <span className="text-stone-500 text-sm italic ml-1">Consultando la Biblioteca...</span>
        </div>
    );
}

function FieldLabel({ icon, text }) {
    return (
        <p className="text-stone-400 text-xs font-semibold tracking-widest uppercase mb-0.5">
            {icon} {text}
        </p>
    );
}

function ObraDetalleCard({ obra, fuente }) {
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
                {obra.nombre_autor && (
                    <div>
                        <FieldLabel icon="👤" text="Autor" />
                        <p className="text-stone-700">{obra.nombre_autor}</p>
                    </div>
                )}
                {obra.autor_firma && (
                    <div>
                        <FieldLabel icon="✍️" text="Firma" />
                        <p className="text-stone-700">{obra.autor_firma}</p>
                    </div>
                )}
                {obra.anio && (
                    <div>
                        <FieldLabel icon="📅" text="Año" />
                        <p className="text-stone-700">{obra.anio}</p>
                    </div>
                )}
                {obra.fecha && (
                    <div>
                        <FieldLabel icon="📆" text="Fecha" />
                        <p className="text-stone-700">{obra.fecha}</p>
                    </div>
                )}
                {obra.tipo_publicacion && (
                    <div>
                        <FieldLabel icon="🏷️" text="Tipo" />
                        <p className="text-stone-700">{obra.tipo_publicacion}</p>
                    </div>
                )}
                {obra.tema_principal && (
                    <div>
                        <FieldLabel icon="🎯" text="Tema" />
                        <p className="text-stone-700">{obra.tema_principal}</p>
                    </div>
                )}
                {obra.imprenta && (
                    <div>
                        <FieldLabel icon="🖨️" text="Imprenta" />
                        <p className="text-stone-700">{obra.imprenta}</p>
                    </div>
                )}
                {obra.lugar_impresion && (
                    <div>
                        <FieldLabel icon="📍" text="Lugar" />
                        <p className="text-stone-700">{obra.lugar_impresion}</p>
                    </div>
                )}
                {obra.paginas && (
                    <div>
                        <FieldLabel icon="📖" text="Páginas" />
                        <p className="text-stone-700">{obra.paginas}</p>
                    </div>
                )}
                {obra.idioma && (
                    <div>
                        <FieldLabel icon="🌐" text="Idioma" />
                        <p className="text-stone-700">{obra.idioma}</p>
                    </div>
                )}
                {obra.formato && (
                    <div>
                        <FieldLabel icon="💾" text="Formato" />
                        <p className="text-stone-700">{obra.formato}</p>
                    </div>
                )}
                {obra.derechos && (
                    <div>
                        <FieldLabel icon="⚖️" text="Derechos" />
                        <p className="text-stone-700">{obra.derechos}</p>
                    </div>
                )}
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
                    <a
                        href={obra.enlace}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs bg-stone-100 text-stone-600 hover:bg-amber-50 hover:text-amber-700 px-3 py-1.5 rounded-full border border-stone-200 transition-colors"
                    >
                        🔗 Ver en BNE
                    </a>
                )}
            </div>
        </div>
    );
}

function SectionHeader({ color, label, count }) {
    const colors = {
        stone: 'bg-stone-400 text-stone-700',
        emerald: 'bg-emerald-500 text-emerald-700',
        amber: 'bg-amber-400 text-amber-700',
        red: 'bg-red-400 text-red-700',
    };
    const [bg, text] = colors[color].split(' ');
    return (
        <h4 className={`font-serif font-bold ${text} mb-3 flex items-center gap-2`}>
            <span className={`w-1.5 h-4 ${bg} rounded-full`}></span>
            {label} ({count})
        </h4>
    );
}

function ListaObras({ obras, dotColor, showLink = false }) {
    return (
        <div className="bg-white border border-stone-200 rounded-xl overflow-hidden">
            {obras.map((obra, idx) => (
                <div
                    key={idx}
                    className={`flex items-center gap-3 px-5 py-3 text-sm ${idx < obras.length - 1 ? 'border-b border-stone-100' : ''}`}
                >
                    <span className={`w-1.5 h-1.5 ${dotColor} rounded-full flex-shrink-0`}></span>
                    <span className="text-stone-800 font-medium flex-1">{obra.titulo}</span>
                    <span className="text-stone-400 text-xs">ID: {obra.id}</span>
                    {showLink && obra.enlace && (
                        <a
                            href={obra.enlace}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-xs text-amber-600 hover:text-amber-800 hover:underline"
                        >
                            BNE ↗
                        </a>
                    )}
                </div>
            ))}
        </div>
    );
}

function ImportResults({ resultado, loading, error }) {
    if (loading) {
        return (
            <div className="bg-white border border-stone-200 p-6 rounded-xl shadow-sm">
                <LoadingSpinner />
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-50 border border-red-200 p-5 rounded-xl">
                <p className="text-red-700 font-medium">❌ {error}</p>
            </div>
        );
    }

    if (!resultado) return null;

    // Para búsquedas por nombre
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
                    {resultado.mensaje && (
                        <p className="text-amber-700 text-sm mt-1 italic">{resultado.mensaje}</p>
                    )}
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
                            {resultados_bd.map((obra, idx) => (
                                <ObraDetalleCard key={idx} obra={obra} fuente="📍 BD Local" />
                            ))}
                        </div>
                    </div>
                )}

                {guardadas.length > 0 && (
                    <div>
                        <SectionHeader color="emerald" label="Nuevas obras guardadas desde BNE" count={guardadas.length} />
                        <ListaObras obras={guardadas} dotColor="bg-emerald-500" showLink={true} />
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
                                <div
                                    key={idx}
                                    className={`flex items-start gap-3 px-5 py-3 text-sm ${idx < errores_bne.length - 1 ? 'border-b border-stone-100' : ''}`}
                                >
                                    <span className="w-1.5 h-1.5 bg-red-400 rounded-full flex-shrink-0 mt-1.5"></span>
                                    <span className="text-red-700">
                                        <span className="font-medium">{err.titulo}</span>: {err.error}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {total_encontrados === 0 && (
                    <div className="bg-amber-50 border border-amber-200 p-5 rounded-xl text-center">
                        <p className="text-amber-700 italic">
                            No se encontraron resultados para "<strong>{nombre_buscado}</strong>"
                        </p>
                    </div>
                )}
            </div>
        );
    }

    // Para importaciones individuales (url o titulo)
    if (resultado.data) {
        const obra = resultado.data;
        const fuente = resultado.fuente;
        const esNueva = resultado.message.includes('importada') && !resultado.message.includes('existe');

        let borderColor, tagBg, tagText, icon;
        if (esNueva) {
            borderColor = 'border-l-emerald-500';
            tagBg = 'bg-emerald-50';
            tagText = 'text-emerald-700';
            icon = '✅';
        } else if (fuente === 'BD local') {
            borderColor = 'border-l-amber-500';
            tagBg = 'bg-amber-50';
            tagText = 'text-amber-700';
            icon = '📚';
        } else {
            borderColor = 'border-l-stone-400';
            tagBg = 'bg-stone-50';
            tagText = 'text-stone-700';
            icon = 'ℹ️';
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
                            <div>
                                <FieldLabel icon="📖" text="Título" />
                                <p className="text-stone-700">{obra.titulo}</p>
                            </div>
                            <div>
                                <FieldLabel icon="✍️" text="Autor" />
                                <p className="text-stone-700">{obra.nombre_autor || 'N/A'}</p>
                            </div>
                            <div>
                                <FieldLabel icon="📅" text="Año" />
                                <p className="text-stone-700">{obra.anio || 'N/A'}</p>
                            </div>
                            <div>
                                <FieldLabel icon="🏷️" text="Tipo" />
                                <p className="text-stone-700">{obra.tipo_publicacion || 'N/A'}</p>
                            </div>
                            <div>
                                <FieldLabel icon="🆔" text="ID" />
                                <p className="text-stone-700">{obra.id}</p>
                            </div>
                            {obra.enlace && (
                                <div>
                                    <FieldLabel icon="🔗" text="Enlace" />
                                    <a
                                        href={obra.enlace}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="text-amber-600 hover:text-amber-800 hover:underline text-sm"
                                    >
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

    // Para importaciones en lote
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
                                <div
                                    key={idx}
                                    className={`flex items-center gap-3 px-5 py-3 text-sm ${idx < resultado.resultados.importadas.length - 1 ? 'border-b border-stone-100' : ''}`}
                                >
                                    <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full flex-shrink-0"></span>
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
                                <div
                                    key={idx}
                                    className={`flex items-center gap-3 px-5 py-3 text-sm ${idx < resultado.resultados.existentes.length - 1 ? 'border-b border-stone-100' : ''}`}
                                >
                                    <span className="w-1.5 h-1.5 bg-amber-400 rounded-full flex-shrink-0"></span>
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
                                <div
                                    key={idx}
                                    className={`flex items-start gap-3 px-5 py-3 text-sm ${idx < resultado.resultados.errores.length - 1 ? 'border-b border-stone-100' : ''}`}
                                >
                                    <span className="w-1.5 h-1.5 bg-red-400 rounded-full flex-shrink-0 mt-1.5"></span>
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

const TABS = [
    { id: 'nombre',       icon: '🔎', label: 'Buscar en BD'  },
    { id: 'url',          icon: '🔗', label: 'Por URL'       },
    { id: 'titulo',       icon: '🔍', label: 'Por Título BNE' },
    { id: 'rango-fechas', icon: '📅', label: 'Por Fechas'    },
    { id: 'lote',         icon: '📦', label: 'Lote'          },
];

export default function App() {
    const queryParams = useQueryParams();
    const [activeTab, setActiveTab] = useState('nombre');
    const [url, setUrl] = useState(queryParams.url || '');
    const [titulo, setTitulo] = useState(queryParams.titulo || queryParams.periodicode || '');
    const [nombre, setNombre] = useState(queryParams.nombre || '');
    const [loteItems, setLoteItems] = useState('');
    const [fechaDesde, setFechaDesde] = useState(queryParams.fechaDesde || '');
    const [fechaHasta, setFechaHasta] = useState(queryParams.fechaHasta || '');
    const [resultado, setResultado] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (queryParams.url && !resultado) {
            importarURL();
        } else if ((queryParams.titulo || queryParams.periodicode) && !resultado) {
            importarTitulo();
        } else if (queryParams.fechaDesde && queryParams.fechaHasta && !resultado) {
            setActiveTab('rango-fechas');
        }
    }, [queryParams]);

    useEffect(() => {
        if (queryParams.fechaDesde && queryParams.fechaHasta && !resultado && fechaDesde && fechaHasta) {
            buscarPorRangoFechas();
        }
    }, [fechaDesde, fechaHasta, queryParams]);

    const importarURL = async () => {
        if (!url.trim()) { setError('Por favor ingresa una URL'); return; }
        setLoading(true); setError(null);
        try {
            const response = await fetch(`${API_BASE_URL}/api/importar/url`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: url.trim() })
            });
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `Error ${response.status}: ${response.statusText}`);
            }
            setResultado(await response.json());
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const importarTitulo = async () => {
        if (!titulo.trim()) { setError('Por favor ingresa un título'); return; }
        setLoading(true); setError(null);
        try {
            const response = await fetch(`${API_BASE_URL}/api/importar/titulo`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ titulo: titulo.trim() })
            });
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `Error ${response.status}: ${response.statusText}`);
            }
            setResultado(await response.json());
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const buscarPorNombre = async () => {
        if (!nombre.trim()) { setError('Por favor ingresa un nombre o palabra clave'); return; }
        setLoading(true); setError(null);
        try {
            const response = await fetch(`${API_BASE_URL}/api/importar/nombre`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nombre: nombre.trim(), limite: 20 })
            });
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `Error ${response.status}: ${response.statusText}`);
            }
            setResultado(await response.json());
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const importarLote = async () => {
        const lineas = loteItems.trim().split('\n').filter(l => l.trim());
        if (lineas.length === 0) { setError('Por favor ingresa al menos un título o URL'); return; }
        const obras = lineas.map(linea => {
            const isUrl = linea.includes('datos.bne.es');
            return isUrl ? { url: linea } : { titulo: linea };
        });
        setLoading(true); setError(null);
        try {
            const response = await fetch(`${API_BASE_URL}/api/importar/lote`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ obras })
            });
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `Error ${response.status}: ${response.statusText}`);
            }
            setResultado(await response.json());
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const buscarPorRangoFechas = async () => {
        if (!fechaDesde || !fechaHasta) { setError('Por favor ingresa las fechas de inicio y fin'); return; }
        const fechaDesdeObj = new Date(fechaDesde);
        const fechaHastaObj = new Date(fechaHasta);
        if (fechaDesdeObj > fechaHastaObj) { setError('La fecha de inicio no puede ser posterior a la fecha final'); return; }
        if (fechaDesdeObj.getFullYear() < 1500 || fechaDesdeObj.getFullYear() > 2100) { setError('Año inválido en fecha de inicio. Use rango 1500-2100'); return; }
        if (fechaHastaObj.getFullYear() < 1500 || fechaHastaObj.getFullYear() > 2100) { setError('Año inválido en fecha final. Use rango 1500-2100'); return; }

        setLoading(true); setError(null);
        try {
            const response = await fetch(
                `${API_BASE_URL}/api/periodicos/rango-fechas?fecha_desde=${fechaDesde}&fecha_hasta=${fechaHasta}&page=1&per_page=50`,
                { method: 'GET', headers: { 'Content-Type': 'application/json' } }
            );
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `Error ${response.status}: ${response.statusText}`);
            }
            const data = await response.json();
            setResultado({
                nombre_buscado: `Periódicos del ${fechaDesde} al ${fechaHasta}`,
                resultados_bd: data.data || [],
                resultados_bne: [],
                total_encontrados: data.pagination.total
            });
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const inputClass = "w-full px-4 py-3 border border-stone-200 rounded-lg bg-stone-50 text-stone-800 placeholder-stone-400 focus:outline-none focus:ring-2 focus:ring-amber-400 focus:border-amber-400 transition-colors";
    const btnPrimary = "w-full bg-stone-700 hover:bg-stone-800 text-white py-3 px-6 rounded-lg font-semibold tracking-wide transition-colors disabled:opacity-50 disabled:cursor-not-allowed";
    const btnEmerald = "w-full bg-emerald-700 hover:bg-emerald-800 text-white py-3 px-6 rounded-lg font-semibold tracking-wide transition-colors disabled:opacity-50 disabled:cursor-not-allowed";
    const labelClass = "block text-xs font-semibold tracking-widest text-stone-500 uppercase mb-2";

    return (
        <div className="min-h-screen bg-stone-50">
            {/* Header */}
            <header className="bg-gradient-to-br from-stone-800 via-stone-700 to-amber-900">
                <div className="max-w-4xl mx-auto px-6 py-8">
                    <div className="flex items-start gap-5">
                        <div className="text-5xl select-none leading-none mt-1">📚</div>
                        <div>
                            <h1 className="font-serif text-3xl font-bold text-white tracking-tight">
                                Recogida de Datos BNE
                            </h1>
                            <div className="w-16 h-px bg-amber-400 mt-2 mb-2"></div>
                            <p className="text-stone-300 text-sm tracking-wide">
                                Biblioteca Nacional de España · Archivo Digital
                            </p>
                        </div>
                    </div>
                </div>
            </header>

            <main className="max-w-4xl mx-auto px-6 py-8">
                {/* Tabs */}
                <div className="border-b border-stone-200 mb-8">
                    <nav className="flex overflow-x-auto -mb-px">
                        {TABS.map(tab => (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                className={`px-5 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-all ${
                                    activeTab === tab.id
                                        ? 'border-amber-600 text-amber-700 bg-amber-50/40'
                                        : 'border-transparent text-stone-500 hover:text-stone-700 hover:border-stone-300'
                                }`}
                            >
                                <span className="mr-1.5">{tab.icon}</span>{tab.label}
                            </button>
                        ))}
                    </nav>
                </div>

                {/* Formulario */}
                <div className="bg-white rounded-xl border border-stone-200 shadow-sm p-8 mb-8">

                    {/* Tab: URL */}
                    {activeTab === 'url' && (
                        <>
                            <h2 className="font-serif text-xl font-bold text-stone-800 mb-1">Importar por URL</h2>
                            <p className="text-stone-500 text-sm mb-6">Pega la URL de datos.bne.es directamente</p>
                            <div className="space-y-4">
                                <div>
                                    <label className={labelClass}>Dirección URL</label>
                                    <input
                                        type="text"
                                        value={url}
                                        onChange={(e) => setUrl(e.target.value)}
                                        placeholder="https://datos.bne.es/data/XX0000000"
                                        className={inputClass}
                                    />
                                </div>
                                <button onClick={importarURL} disabled={loading} className={btnPrimary}>
                                    {loading ? 'Importando...' : '↓ Importar Obra'}
                                </button>
                            </div>
                        </>
                    )}

                    {/* Tab: Buscar en BD */}
                    {activeTab === 'nombre' && (
                        <>
                            <h2 className="font-serif text-xl font-bold text-stone-800 mb-1">Buscar en BNE y Guardar</h2>
                            <p className="text-stone-500 text-sm mb-1">
                                Busca en <strong className="text-stone-600">datos.bne.es</strong> y en tu base de datos local.
                            </p>
                            <p className="text-stone-400 text-xs mb-6 italic">
                                Las obras de BNE no registradas en tu BD se guardan automáticamente.
                            </p>
                            <div className="space-y-4">
                                <div>
                                    <label className={labelClass}>Nombre o palabra clave</label>
                                    <input
                                        type="text"
                                        value={nombre}
                                        onChange={(e) => setNombre(e.target.value)}
                                        placeholder="Ej: Quijote, Periódico ABC, La Vanguardia..."
                                        className={inputClass.replace('focus:ring-amber-400 focus:border-amber-400', 'focus:ring-emerald-400 focus:border-emerald-400')}
                                        onKeyPress={(e) => e.key === 'Enter' && buscarPorNombre()}
                                    />
                                </div>
                                <button onClick={buscarPorNombre} disabled={loading} className={btnEmerald}>
                                    {loading ? 'Buscando y guardando...' : '🔎 Buscar en BNE y Guardar en BD'}
                                </button>
                            </div>
                        </>
                    )}

                    {/* Tab: Por Título */}
                    {activeTab === 'titulo' && (
                        <>
                            <h2 className="font-serif text-xl font-bold text-stone-800 mb-1">Importar por Título</h2>
                            <p className="text-stone-500 text-sm mb-1">
                                Importa todas las obras cuyo <strong className="text-stone-600">título contenga</strong> la frase indicada.
                            </p>
                            <p className="text-stone-400 text-xs mb-6 italic">
                                Para buscar varios títulos a la vez, sepáralos con comas.
                            </p>
                            <div className="space-y-4">
                                <div>
                                    <label className={labelClass}>Título o frase</label>
                                    <input
                                        type="text"
                                        value={titulo}
                                        onChange={(e) => setTitulo(e.target.value)}
                                        placeholder="Ej: La Vanguardia, periódico de damas, El Quijote..."
                                        className={inputClass}
                                        onKeyPress={(e) => e.key === 'Enter' && importarTitulo()}
                                    />
                                </div>
                                <button onClick={importarTitulo} disabled={loading} className={btnPrimary}>
                                    {loading ? 'Importando...' : '↓ Importar Obras'}
                                </button>
                            </div>
                        </>
                    )}

                    {/* Tab: Por Fechas */}
                    {activeTab === 'rango-fechas' && (
                        <>
                            <h2 className="font-serif text-xl font-bold text-stone-800 mb-1">Buscar por Rango de Fechas</h2>
                            <p className="text-stone-500 text-sm mb-6">
                                Encuentra todos los periódicos dentro de un intervalo específico
                            </p>
                            <div className="space-y-4">
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className={labelClass}>📅 Fecha desde</label>
                                        <input
                                            type="date"
                                            value={fechaDesde}
                                            onChange={(e) => setFechaDesde(e.target.value)}
                                            min="1500-01-01"
                                            max="2100-12-31"
                                            className={inputClass}
                                        />
                                    </div>
                                    <div>
                                        <label className={labelClass}>📅 Fecha hasta</label>
                                        <input
                                            type="date"
                                            value={fechaHasta}
                                            onChange={(e) => setFechaHasta(e.target.value)}
                                            min="1500-01-01"
                                            max="2100-12-31"
                                            className={inputClass}
                                        />
                                    </div>
                                </div>
                                <div className="bg-amber-50 border border-amber-100 p-3 rounded-lg text-xs text-amber-700">
                                    ℹ️ Filtro automático por periódicos BIMO (prefijo https://datos.bne.es/resource/bimo...)
                                </div>
                                <button onClick={buscarPorRangoFechas} disabled={loading} className={btnPrimary}>
                                    {loading ? 'Buscando...' : '🔍 Buscar Periódicos'}
                                </button>
                            </div>
                        </>
                    )}

                    {/* Tab: Lote */}
                    {activeTab === 'lote' && (
                        <>
                            <h2 className="font-serif text-xl font-bold text-stone-800 mb-1">Importación en Lote</h2>
                            <p className="text-stone-500 text-sm mb-6">Una URL o título por línea</p>
                            <div className="space-y-4">
                                <div>
                                    <label className={labelClass}>URLs o títulos</label>
                                    <textarea
                                        value={loteItems}
                                        onChange={(e) => setLoteItems(e.target.value)}
                                        placeholder={"https://datos.bne.es/edicion/bimo0000659916.html\nhttps://datos.bne.es/data/XX0000000\nhttps://datos.bne.es/edicion/a6065627.html"}
                                        rows={6}
                                        className={`${inputClass} font-mono text-xs resize-none`}
                                    />
                                </div>
                                <button onClick={importarLote} disabled={loading} className={btnPrimary}>
                                    {loading ? 'Procesando...' : '↓ Importar Lote'}
                                </button>
                            </div>
                        </>
                    )}
                </div>

                {/* Resultados */}
                {(resultado || loading || error) && (
                    <div className="mb-8">
                        <h2 className="font-serif text-xl font-bold text-stone-800 mb-4 flex items-center gap-3">
                            <span className="w-1 h-6 bg-amber-500 rounded-full"></span>
                            Resultados
                        </h2>
                        <ImportResults resultado={resultado} loading={loading} error={error} />
                    </div>
                )}

                {/* Footer */}
                <footer className="mt-12 pt-6 border-t border-stone-200 text-center">
                    <p className="text-stone-400 text-sm">
                        Datos de:{' '}
                        <a
                            href="https://datos.bne.es"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-amber-600 hover:text-amber-800 hover:underline"
                        >
                            datos.bne.es
                        </a>
                    </p>
                    <p className="text-stone-300 text-xs mt-1">Licencia CC0 · Creative Commons Public Domain</p>
                </footer>
            </main>
        </div>
    );
}
