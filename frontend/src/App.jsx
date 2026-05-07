/**
 * Frontend React - Recogida de Datos BNE
 * Acepta parametros: URL o nombre del periódico/obra
 */

import React, { useState, useEffect } from 'react';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Hook para leer parámetros de URL
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

// Componente para mostrar estado de carga
function LoadingSpinner() {
    return (
        <div className="flex items-center justify-center space-x-2">
            <div className="w-3 h-3 bg-blue-600 rounded-full animate-bounce"></div>
            <div className="w-3 h-3 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
            <div className="w-3 h-3 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
        </div>
    );
}

// Componente para mostrar resultados de importación
function ImportResults({ resultado, loading, error }) {
    if (loading) {
        return (
            <div className="bg-white p-6 rounded-lg shadow">
                <LoadingSpinner />
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-50 border border-red-200 p-4 rounded-lg">
                <p className="text-red-700"><strong>❌ Error:</strong> {error}</p>
            </div>
        );
    }

    if (!resultado) return null;

    // Para búsquedas por nombre
    if (resultado.nombre_buscado) {
        const { nombre_buscado, resultados_bd, resultados_bne, total_encontrados } = resultado;
        
        const ObraDetalleCard = ({ obra, fuente }) => (
            <div className="bg-white p-4 rounded border-l-4 border-blue-400 shadow-sm hover:shadow-md transition">
                {/* Encabezado */}
                <div className="mb-3 pb-3 border-b-2 border-gray-200">
                    <p className="font-bold text-lg text-gray-800">{obra.titulo}</p>
                    <div className="flex gap-2 mt-1">
                        <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">ID: {obra.id}</span>
                        {fuente && <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">{fuente}</span>}
                    </div>
                </div>
                
                {/* Información en rejilla */}
                <div className="grid grid-cols-2 gap-3 text-sm">
                    {/* Fila 1: Autores */}
                    {(obra.nombre_autor || obra.autor_firma) && (
                        <>
                            {obra.nombre_autor && (
                                <div>
                                    <p className="text-gray-500 text-xs font-semibold">👤 AUTOR</p>
                                    <p className="text-gray-800">{obra.nombre_autor}</p>
                                </div>
                            )}
                            {obra.autor_firma && (
                                <div>
                                    <p className="text-gray-500 text-xs font-semibold">✍️ FIRMA</p>
                                    <p className="text-gray-800">{obra.autor_firma}</p>
                                </div>
                            )}
                        </>
                    )}
                    
                    {/* Fila 2: Fechas */}
                    {(obra.anio || obra.fecha) && (
                        <>
                            {obra.anio && (
                                <div>
                                    <p className="text-gray-500 text-xs font-semibold">📅 AÑO</p>
                                    <p className="text-gray-800">{obra.anio}</p>
                                </div>
                            )}
                            {obra.fecha && (
                                <div>
                                    <p className="text-gray-500 text-xs font-semibold">📆 FECHA</p>
                                    <p className="text-gray-800">{obra.fecha}</p>
                                </div>
                            )}
                        </>
                    )}
                    
                    {/* Fila 3: Tipo y publicación */}
                    {obra.tipo_publicacion && (
                        <div>
                            <p className="text-gray-500 text-xs font-semibold">🏷️ TIPO</p>
                            <p className="text-gray-800">{obra.tipo_publicacion}</p>
                        </div>
                    )}
                    {obra.tema_principal && (
                        <div>
                            <p className="text-gray-500 text-xs font-semibold">🎯 TEMA</p>
                            <p className="text-gray-800">{obra.tema_principal}</p>
                        </div>
                    )}
                    
                    {/* Fila 4: Imprenta y lugar */}
                    {obra.imprenta && (
                        <div>
                            <p className="text-gray-500 text-xs font-semibold">🖨️ IMPRENTA</p>
                            <p className="text-gray-800">{obra.imprenta}</p>
                        </div>
                    )}
                    {obra.lugar_impresion && (
                        <div>
                            <p className="text-gray-500 text-xs font-semibold">📍 LUGAR</p>
                            <p className="text-gray-800">{obra.lugar_impresion}</p>
                        </div>
                    )}
                    
                    {/* Fila 5: Páginas e idioma */}
                    {obra.paginas && (
                        <div>
                            <p className="text-gray-500 text-xs font-semibold">📖 PÁGINAS</p>
                            <p className="text-gray-800">{obra.paginas}</p>
                        </div>
                    )}
                    {obra.idioma && (
                        <div>
                            <p className="text-gray-500 text-xs font-semibold">🌐 IDIOMA</p>
                            <p className="text-gray-800">{obra.idioma}</p>
                        </div>
                    )}
                    
                    {/* Fila 6: Formato y derechos */}
                    {obra.formato && (
                        <div>
                            <p className="text-gray-500 text-xs font-semibold">💾 FORMATO</p>
                            <p className="text-gray-800">{obra.formato}</p>
                        </div>
                    )}
                    {obra.derechos && (
                        <div>
                            <p className="text-gray-500 text-xs font-semibold">⚖️ DERECHOS</p>
                            <p className="text-gray-800">{obra.derechos}</p>
                        </div>
                    )}
                </div>
                
                {/* Sección de descripción */}
                
                {/* Sección de cómo citar */}
                {obra.como_citar && (
                    <div className="mt-3 pt-3 border-t border-gray-200">
                        <p className="text-gray-500 text-xs font-semibold mb-1">📚 CÓMO CITAR</p>
                        <p className="text-gray-700 text-sm bg-gray-50 p-2 rounded font-mono text-xs">{obra.como_citar}</p>
                    </div>
                )}
                
                {/* Enlaces */}
                <div className="mt-3 pt-3 border-t border-gray-200 flex gap-2 flex-wrap">
                    {obra.enlace && (
                        <a href={obra.enlace} target="_blank" rel="noopener noreferrer" 
                           className="text-xs bg-blue-100 text-blue-700 hover:bg-blue-200 px-3 py-1 rounded transition">
                            🔗 Ver en BNE
                        </a>
                    )}
                </div>
            </div>
        );
        
        return (
            <div className="space-y-4">
                <div className="bg-blue-50 border border-blue-200 p-4 rounded-lg">
                    <p className="text-blue-700 font-semibold">
                        🔎 Búsqueda: "<strong>{nombre_buscado}</strong>" - 
                        Encontrados: <strong className="text-blue-600">{total_encontrados}</strong> resultados
                    </p>
                </div>
                
                {resultados_bd.length > 0 && (
                    <div className="bg-green-50 border border-green-200 p-4 rounded-lg">
                        <h4 className="font-bold text-green-700 mb-4">
                            ✅ Base de Datos Local ({resultados_bd.length})
                        </h4>
                        <div className="space-y-3">
                            {resultados_bd.map((obra, idx) => (
                                <ObraDetalleCard key={idx} obra={obra} fuente="📍 BD Local" />
                            ))}
                        </div>
                    </div>
                )}
                
                {resultados_bne.length > 0 && (
                    <div className="bg-purple-50 border border-purple-200 p-4 rounded-lg">
                        <h4 className="font-bold text-purple-700 mb-4">
                            🌐 Encontrados en datos.bne.es ({resultados_bne.length})
                        </h4>
                        <div className="space-y-3">
                            {resultados_bne.map((obra, idx) => (
                                <ObraDetalleCard key={idx} obra={obra} fuente="datos.bne.es" />
                            ))}
                        </div>
                    </div>
                )}
                
                {total_encontrados === 0 && (
                    <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
                        <p className="text-yellow-700">⚠️ No se encontraron resultados para "<strong>{nombre_buscado}</strong>" en la base de datos local</p>
                        <p className="text-yellow-600 text-sm mt-2">💡 Recomendación: Usa "Por URL" o "Por Lote" para importar directamente desde datos.bne.es</p>
                    </div>
                )}
                
                {resultado.mensaje && (
                    <div className="bg-blue-50 border border-blue-200 p-4 rounded-lg">
                        <p className="text-blue-700 text-sm">ℹ️ {resultado.mensaje}</p>
                    </div>
                )}
            </div>
        );
    }

    // Para importaciones individuales (url o titulo)
    if (resultado.data) {
        const obra = resultado.data;
        const fuente = resultado.fuente; // 'BD local' o 'datos.bne.es'
        const esNueva = resultado.message.includes('importada') && !resultado.message.includes('existe');
        
        // Determinar color y icono según la fuente
        let bgColor, borderColor, titleColor, icon;
        if (esNueva) {
            // Nueva: verde (importada de datos.bne.es)
            bgColor = 'bg-green-50';
            borderColor = 'border-green-400';
            titleColor = 'text-green-700';
            icon = '✅';
        } else if (fuente === 'BD local') {
            // Existe en BD local: naranja
            bgColor = 'bg-amber-50';
            borderColor = 'border-amber-400';
            titleColor = 'text-amber-700';
            icon = '📚';
        } else {
            // Existe pero nueva en esta sesión: azul
            bgColor = 'bg-blue-50';
            borderColor = 'border-blue-400';
            titleColor = 'text-blue-700';
            icon = 'ℹ️';
        }
        
        return (
            <div className={`border-l-4 p-4 rounded ${bgColor} ${borderColor} border-l`}>
                <div className="flex items-start">
                    <div className={`text-2xl mr-4 ${titleColor}`}>
                        {icon}
                    </div>
                    <div className="flex-1">
                        <p className={`font-bold ${titleColor}`}>
                            {resultado.message}
                        </p>
                        {fuente && (
                            <p className={`text-xs ${titleColor} opacity-75 mt-1`}>
                                📍 Encontrada en: <strong>{fuente}</strong>
                            </p>
                        )}
                        <div className="mt-3 text-sm text-gray-700 space-y-1">
                            <p><strong>📖 Título:</strong> {obra.titulo}</p>
                            <p><strong>✍️ Autor:</strong> {obra.nombre_autor || 'N/A'}</p>
                            <p><strong>📅 Año:</strong> {obra.anio || 'N/A'}</p>
                            <p><strong>🏷️ Tipo:</strong> {obra.tipo_publicacion || 'N/A'}</p>
                            <p><strong>🆔 ID:</strong> {obra.id}</p>
                            {obra.enlace && (
                                <p><strong>🔗 Enlace:</strong> 
                                    <a href={obra.enlace} target="_blank" rel="noopener noreferrer" 
                                       className="text-blue-600 hover:underline ml-1">
                                        Ver en datos.bne.es
                                    </a>
                                </p>
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
            <div className="space-y-4">
                <div className="bg-white p-4 rounded-lg shadow">
                    <h3 className="font-bold text-lg mb-4">📊 Estadísticas</h3>
                    <div className="grid grid-cols-2 gap-4">
                        <div className="bg-blue-50 p-3 rounded">
                            <p className="text-blue-600 font-bold text-2xl">{stats.total}</p>
                            <p className="text-blue-700 text-sm">Total procesadas</p>
                        </div>
                        <div className="bg-green-50 p-3 rounded">
                            <p className="text-green-600 font-bold text-2xl">{stats.importadas}</p>
                            <p className="text-green-700 text-sm">Nuevas importadas</p>
                        </div>
                        <div className="bg-amber-50 p-3 rounded">
                            <p className="text-amber-600 font-bold text-2xl">{stats.existentes}</p>
                            <p className="text-amber-700 text-sm">Ya existentes</p>
                        </div>
                        <div className="bg-red-50 p-3 rounded">
                            <p className="text-red-600 font-bold text-2xl">{stats.errores}</p>
                            <p className="text-red-700 text-sm">Errores</p>
                        </div>
                    </div>
                </div>

                {resultado.resultados.importadas.length > 0 && (
                    <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                        <h4 className="font-bold text-green-700 mb-2">✅ Nuevas Importadas ({resultado.resultados.importadas.length})</h4>
                        <ul className="space-y-1">
                            {resultado.resultados.importadas.map((obra, idx) => (
                                <li key={idx} className="text-sm text-green-600">
                                    • {obra.titulo} (ID: {obra.id}) - 📥 {obra.fuente || 'datos.bne.es'}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}

                {resultado.resultados.existentes.length > 0 && (
                    <div className="bg-amber-50 p-4 rounded-lg border border-amber-200">
                        <h4 className="font-bold text-amber-700 mb-2">📚 Ya Existentes ({resultado.resultados.existentes.length})</h4>
                        <ul className="space-y-1">
                            {resultado.resultados.existentes.map((obra, idx) => (
                                <li key={idx} className="text-sm text-amber-600">
                                    • {obra.titulo} (ID: {obra.id}) - 📍 {obra.fuente || 'BD'}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}

                {resultado.resultados.errores.length > 0 && (
                    <div className="bg-red-50 p-4 rounded-lg border border-red-200">
                        <h4 className="font-bold text-red-700 mb-2">❌ Errores ({resultado.resultados.errores.length})</h4>
                        <ul className="space-y-1">
                            {resultado.resultados.errores.map((error, idx) => (
                                <li key={idx} className="text-sm text-red-600">
                                    • {error.origen}: {error.error}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        );
    }

    return null;
}

// Renderizar la aplicación
export default function App() {
    const queryParams = useQueryParams();
    const [activeTab, setActiveTab] = useState('nombre'); // 'url' o 'titulo' o 'nombre' o 'lote' o 'rango-fechas'
    const [url, setUrl] = useState(queryParams.url || '');
    const [titulo, setTitulo] = useState(queryParams.titulo || queryParams.periodicode || '');
    const [nombre, setNombre] = useState(queryParams.nombre || ''); // Nueva búsqueda por nombre
    const [loteItems, setLoteItems] = useState('');
    const [fechaDesde, setFechaDesde] = useState(queryParams.fechaDesde || '');
    const [fechaHasta, setFechaHasta] = useState(queryParams.fechaHasta || '');
    const [resultado, setResultado] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Si viene con parámetros en URL, importar automáticamente
    useEffect(() => {
        if (queryParams.url && !resultado) {
            importarURL();
        } else if ((queryParams.titulo || queryParams.periodicode) && !resultado) {
            importarTitulo();
        } else if (queryParams.fechaDesde && queryParams.fechaHasta && !resultado) {
            setActiveTab('rango-fechas');
            // Se ejecutará con useEffect adicional
        }
    }, [queryParams]);

    // Ejecutar búsqueda por fechas si viene en parámetros
    useEffect(() => {
        if (queryParams.fechaDesde && queryParams.fechaHasta && !resultado && fechaDesde && fechaHasta) {
            buscarPorRangoFechas();
        }
    }, [fechaDesde, fechaHasta, queryParams]);

    const importarURL = async () => {
        if (!url.trim()) {
            setError('Por favor ingresa una URL');
            return;
        }

        setLoading(true);
        setError(null);
        try {
            const response = await fetch(`${API_BASE_URL}/api/importar/url`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: url.trim() })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                const errorMsg = errorData.error || `Error ${response.status}: ${response.statusText}`;
                throw new Error(errorMsg);
            }

            const data = await response.json();
            setResultado(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const importarTitulo = async () => {
        if (!titulo.trim()) {
            setError('Por favor ingresa un título');
            return;
        }

        setLoading(true);
        setError(null);
        try {
            const response = await fetch(`${API_BASE_URL}/api/importar/titulo`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ titulo: titulo.trim() })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                const errorMsg = errorData.error || `Error ${response.status}: ${response.statusText}`;
                throw new Error(errorMsg);
            }

            const data = await response.json();
            setResultado(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const buscarPorNombre = async () => {
        if (!nombre.trim()) {
            setError('Por favor ingresa un nombre o palabra clave');
            return;
        }

        setLoading(true);
        setError(null);
        try {
            const response = await fetch(`${API_BASE_URL}/api/importar/nombre`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nombre: nombre.trim(), limite: 20 })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                const errorMsg = errorData.error || `Error ${response.status}: ${response.statusText}`;
                throw new Error(errorMsg);
            }

            const data = await response.json();
            setResultado(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const importarLote = async () => {
        const lineas = loteItems.trim().split('\n').filter(l => l.trim());
        if (lineas.length === 0) {
            setError('Por favor ingresa al menos un título o URL');
            return;
        }

        const obras = lineas.map(linea => {
            const isUrl = linea.includes('datos.bne.es');
            return isUrl ? { url: linea } : { titulo: linea };
        });

        setLoading(true);
        setError(null);
        try {
            const response = await fetch(`${API_BASE_URL}/api/importar/lote`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ obras })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                const errorMsg = errorData.error || `Error ${response.status}: ${response.statusText}`;
                throw new Error(errorMsg);
            }

            const data = await response.json();
            setResultado(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const buscarPorRangoFechas = async () => {
        if (!fechaDesde || !fechaHasta) {
            setError('Por favor ingresa las fechas de inicio y fin');
            return;
        }

        // Validación adicional de fechas
        const fechaDesdeObj = new Date(fechaDesde);
        const fechaHastaObj = new Date(fechaHasta);
        
        if (fechaDesdeObj > fechaHastaObj) {
            setError('La fecha de inicio no puede ser posterior a la fecha final');
            return;
        }

        if (fechaDesdeObj.getFullYear() < 1500 || fechaDesdeObj.getFullYear() > 2100) {
            setError('Año inválido en fecha de inicio. Use rango 1500-2100');
            return;
        }

        if (fechaHastaObj.getFullYear() < 1500 || fechaHastaObj.getFullYear() > 2100) {
            setError('Año inválido en fecha final. Use rango 1500-2100');
            return;
        }

        setLoading(true);
        setError(null);
        try {
            const response = await fetch(
                `${API_BASE_URL}/api/periodicos/rango-fechas?fecha_desde=${fechaDesde}&fecha_hasta=${fechaHasta}&page=1&per_page=50`,
                {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json' }
                }
            );

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                const errorMsg = errorData.error || `Error ${response.status}: ${response.statusText}`;
                throw new Error(errorMsg);
            }

            const data = await response.json();
            
            // Formatear resultado para mostrar como búsqueda
            const resultadoFormato = {
                nombre_buscado: `Periódicos del ${fechaDesde} al ${fechaHasta}`,
                resultados_bd: data.data || [],
                resultados_bne: [],
                total_encontrados: data.pagination.total
            };
            
            setResultado(resultadoFormato);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
            {/* Header */}
            <div className="bg-white shadow-sm border-b border-gray-200">
                <div className="max-w-4xl mx-auto px-4 py-6">
                    <h1 className="text-3xl font-bold text-gray-800">📚 Recogida de Datos BNE</h1>
                    <p className="text-gray-600 mt-1">Importa obras desde la Biblioteca Nacional de España</p>
                </div>
            </div>

            {/* Contenido principal */}
            <div className="max-w-4xl mx-auto px-4 py-8">
                {/* Tabs */}
                <div className="flex gap-2 mb-6 bg-white p-1 rounded-lg shadow flex-wrap">
                    <button
                        onClick={() => setActiveTab('url')}
                        className={`flex-1 py-2 px-4 rounded font-semibold transition ${activeTab === 'url' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
                    >
                        🔗 Por URL
                    </button>
                    <button
                        onClick={() => setActiveTab('nombre')}
                        className={`flex-1 py-2 px-4 rounded font-semibold transition ${activeTab === 'nombre' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
                    >
                        🔎 Por Nombre
                    </button>
                    <button
                        onClick={() => setActiveTab('titulo')}
                        className={`flex-1 py-2 px-4 rounded font-semibold transition ${activeTab === 'titulo' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
                    >
                        🔍 Por Título
                    </button>
                    <button
                        onClick={() => setActiveTab('rango-fechas')}
                        className={`flex-1 py-2 px-4 rounded font-semibold transition ${activeTab === 'rango-fechas' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
                    >
                        📅 Por Fechas
                    </button>
                    <button
                        onClick={() => setActiveTab('lote')}
                        className={`flex-1 py-2 px-4 rounded font-semibold transition ${activeTab === 'lote' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
                    >
                        📦 Lote
                    </button>
                </div>

                {/* Sección URL */}
                {activeTab === 'url' && (
                    <div className="bg-white p-6 rounded-lg shadow mb-6">
                        <h2 className="text-xl font-bold mb-4">Importar por URL</h2>
                        <p className="text-gray-600 mb-4">Pega la URL de datos.bne.es directamente</p>
                        <div className="space-y-4">
                            <input
                                type="text"
                                value={url}
                                onChange={(e) => setUrl(e.target.value)}
                                placeholder="https://datos.bne.es/data/XX0000000"
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                            <button
                                onClick={importarURL}
                                disabled={loading}
                                className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition font-semibold"
                            >
                                {loading ? 'Importando...' : 'Importar Obra'}
                            </button>
                        </div>
                    </div>
                )}

                {/* Sección Búsqueda por Nombre */}
                {activeTab === 'nombre' && (
                    <div className="bg-white p-6 rounded-lg shadow mb-6">
                        <h2 className="text-xl font-bold mb-4">Buscar por Nombre o Palabra Clave</h2>
                        <p className="text-gray-600 mb-4">Busca en toda la base de datos (BD local + datos.bne.es)</p>
                        <div className="space-y-4">
                            <input
                                type="text"
                                value={nombre}
                                onChange={(e) => setNombre(e.target.value)}
                                placeholder="Ej: Quijote, García, Periódico ABC..."
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                onKeyPress={(e) => e.key === 'Enter' && buscarPorNombre()}
                            />
                            <button
                                onClick={buscarPorNombre}
                                disabled={loading}
                                className="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 disabled:bg-gray-400 transition font-semibold"
                            >
                                {loading ? 'Buscando...' : 'Buscar en Base de Datos'}
                            </button>
                        </div>
                    </div>
                )}

                {/* Sección Título */}
                {activeTab === 'titulo' && (
                    <div className="bg-white p-6 rounded-lg shadow mb-6">
                        <h2 className="text-xl font-bold mb-4">Buscar por Título Exacto</h2>
                        <p className="text-gray-600 mb-4">Escribe el título completo del periódico o la obra</p>
                        <div className="space-y-4">
                            <input
                                type="text"
                                value={titulo}
                                onChange={(e) => setTitulo(e.target.value)}
                                placeholder="Ej: El Quijote, ABC, La Vanguardia..."
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                            <button
                                onClick={importarTitulo}
                                disabled={loading}
                                className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition font-semibold"
                            >
                                {loading ? 'Buscando...' : 'Buscar e Importar'}
                            </button>
                        </div>
                    </div>
                )}

                {/* Sección Rango de Fechas */}
                {activeTab === 'rango-fechas' && (
                    <div className="bg-white p-6 rounded-lg shadow mb-6">
                        <h2 className="text-xl font-bold mb-4">Buscar Periódicos por Rango de Fechas</h2>
                        <p className="text-gray-600 mb-4">Encuentra todos los periódicos dentro de un intervalo de fecha específico</p>
                        <div className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-1">📅 Fecha Desde</label>
                                    <input
                                        type="date"
                                        value={fechaDesde}
                                        onChange={(e) => setFechaDesde(e.target.value)}
                                        min="1500-01-01"
                                        max="2100-12-31"
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-1">📅 Fecha Hasta</label>
                                    <input
                                        type="date"
                                        value={fechaHasta}
                                        onChange={(e) => setFechaHasta(e.target.value)}
                                        min="1500-01-01"
                                        max="2100-12-31"
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    />
                                </div>
                            </div>
                            <div className="bg-blue-50 border border-blue-200 p-3 rounded text-sm text-blue-700">
                                ℹ️ Filtro automático por periódicos BIMO (prefijo https://datos.bne.es/resource/bimo...)
                            </div>
                            <button
                                onClick={buscarPorRangoFechas}
                                disabled={loading}
                                className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition font-semibold"
                            >
                                {loading ? 'Buscando...' : 'Buscar Periódicos'}
                            </button>
                        </div>
                    </div>
                )}

                {/* Sección Lote */}
                {activeTab === 'lote' && (
                    <div className="bg-white p-6 rounded-lg shadow mb-6">
                        <h2 className="text-xl font-bold mb-4">Importación en Lote</h2>
                        <p className="text-gray-600 mb-4">un url por linea</p>
                        <div className="space-y-4">
                            <textarea
                                value={loteItems}
                                onChange={(e) => setLoteItems(e.target.value)}
                                placeholder="https://datos.bne.es/edicion/bimo0000659916.html&#10;https://datos.bne.es/data/XX0000000&#10;https://datos.bne.es/edicion/a6065627.html"
                                rows={6}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
                            />
                            <button
                                onClick={importarLote}
                                disabled={loading}
                                className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition font-semibold"
                            >
                                {loading ? 'Procesando...' : 'Importar Lote'}
                            </button>
                        </div>
                    </div>
                )}

                {/* Resultados */}
                {(resultado || loading || error) && (
                    <div className="mb-6">
                        <h2 className="text-xl font-bold mb-4">Resultados</h2>
                        <ImportResults resultado={resultado} loading={loading} error={error} />
                    </div>
                )}

                {/* Footer */}
                <div className="bg-white p-4 rounded-lg text-center text-sm text-gray-600 mt-8">
                    <p>📖 Datos de: <a href="https://datos.bne.es" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">datos.bne.es</a></p>
                    <p className="mt-2">Licencia: CC0 - Creative Commons Public Domain</p>
                </div>
            </div>
        </div>
    );
}
