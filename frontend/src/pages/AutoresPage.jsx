import { useState, useEffect } from 'react';
import { API_BASE_URL, PER_PAGE } from '../constants';
import LoadingSpinner from '../components/LoadingSpinner';
import EmptyState from '../components/EmptyState';
import SectionHeader from '../components/SectionHeader';
import BarChart from '../components/BarChart';
import ImportResults from '../components/ImportResults';

export default function AutoresPage() {
    const [query, setQuery] = useState('');
    const [resultado, setResultado] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const [stats, setStats] = useState(null);
    const [statsLoading, setStatsLoading] = useState(true);

    const [obrasLista, setObrasLista] = useState([]);
    const [paginaActual, setPaginaActual] = useState(1);
    const [totalPaginas, setTotalPaginas] = useState(1);
    const [listLoading, setListLoading] = useState(true);

    useEffect(() => {
        const cargarStats = async () => {
            try {
                const res = await fetch(`${API_BASE_URL}/api/estadisticas/resumen`);
                if (res.ok) setStats(await res.json());
            } catch { /* stats son opcionales */ } finally {
                setStatsLoading(false);
            }
        };
        cargarStats();
        cargarObras(1);
    }, []);

    const cargarObras = async (pagina) => {
        setListLoading(true);
        try {
            const res = await fetch(`${API_BASE_URL}/api/obras?page=${pagina}&per_page=${PER_PAGE}`);
            if (res.ok) {
                const data = await res.json();
                setObrasLista(data.data || []);
                setTotalPaginas(Math.ceil((data.pagination?.total || 0) / PER_PAGE));
                setPaginaActual(pagina);
            }
        } catch { /* fail silently */ } finally {
            setListLoading(false);
        }
    };

    const buscarAutor = async () => {
        if (!query.trim()) { setError('Por favor ingresa el nombre del autor'); return; }
        setLoading(true); setError(null); setResultado(null);
        try {
            const res = await fetch(`${API_BASE_URL}/api/importar/nombre`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nombre: query.trim(), limite: 20 }),
            });
            if (!res.ok) {
                const e = await res.json().catch(() => ({}));
                throw new Error(e.error || `Error ${res.status}`);
            }
            setResultado(await res.json());
            cargarObras(1);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const obrasPorAutor = obrasLista.reduce((acc, obra) => {
        const autor = obra.nombre_autor || 'Autor desconocido';
        if (!acc[autor]) acc[autor] = [];
        acc[autor].push(obra);
        return acc;
    }, {});

    const inputClass = "w-full px-4 py-3 border border-stone-200 rounded-lg bg-stone-50 text-stone-800 placeholder-stone-400 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-blue-400 transition-colors";

    return (
        <div className="max-w-4xl mx-auto px-6 py-8 space-y-8">

            {/* Stats cards */}
            <div className="grid grid-cols-3 gap-4">
                {statsLoading ? (
                    <div className="col-span-3">
                        <LoadingSpinner label="Cargando estadísticas..." />
                    </div>
                ) : stats ? (
                    <>
                        <div className="bg-white border border-stone-200 rounded-xl p-5 text-center shadow-sm">
                            <p className="font-serif font-bold text-stone-800 text-4xl">
                                {stats.resumen?.total_obras ?? '—'}
                            </p>
                            <p className="text-stone-400 text-xs tracking-widest uppercase mt-1">Total obras</p>
                        </div>
                        <div className="bg-white border border-blue-100 rounded-xl p-5 text-center shadow-sm">
                            <p className="font-serif font-bold text-blue-700 text-4xl">
                                {stats.resumen?.autores_principales?.length ?? '—'}
                            </p>
                            <p className="text-stone-400 text-xs tracking-widest uppercase mt-1">Autores registrados</p>
                        </div>
                        <div className="bg-white border border-amber-100 rounded-xl p-5 text-center shadow-sm">
                            <p className="font-serif font-bold text-amber-700 text-4xl">
                                {stats.resumen?.obras_por_tipo?.length ?? '—'}
                            </p>
                            <p className="text-stone-400 text-xs tracking-widest uppercase mt-1">Tipos de obra</p>
                        </div>
                    </>
                ) : (
                    <div className="col-span-3 text-center text-stone-400 text-sm py-4 bg-white border border-stone-200 rounded-xl">
                        Estadísticas no disponibles — asegúrate de que el backend está en marcha
                    </div>
                )}
            </div>

            {/* Charts */}
            {stats && (stats.resumen?.autores_principales?.length > 0 || stats.resumen?.obras_por_tipo?.length > 0) && (
                <div className="grid grid-cols-2 gap-6">
                    {stats.resumen?.autores_principales?.length > 0 && (
                        <div className="bg-white border border-stone-200 rounded-xl p-5 shadow-sm">
                            <SectionHeader color="blue" label="Autores principales" />
                            <BarChart
                                items={stats.resumen.autores_principales.slice(0, 7)}
                                colorClass="bg-blue-500"
                            />
                        </div>
                    )}
                    {stats.resumen?.obras_por_tipo?.length > 0 && (
                        <div className="bg-white border border-stone-200 rounded-xl p-5 shadow-sm">
                            <SectionHeader color="amber" label="Obras por tipo" />
                            <BarChart
                                items={stats.resumen.obras_por_tipo}
                                colorClass="bg-amber-500"
                                labelKey="tipo"
                            />
                        </div>
                    )}
                </div>
            )}

            {/* Search */}
            <div className="bg-white border border-stone-200 rounded-xl p-8 shadow-sm">
                <h2 className="font-serif text-xl font-bold text-stone-800 mb-1">Buscar Autor en BNE</h2>
                <p className="text-stone-500 text-sm mb-6">
                    Busca en <strong className="text-stone-600">datos.bne.es</strong> y en tu base de datos local.
                    Las obras encontradas se guardan automáticamente.
                </p>
                <div className="flex gap-3">
                    <input
                        type="text"
                        value={query}
                        onChange={e => setQuery(e.target.value)}
                        onKeyPress={e => e.key === 'Enter' && buscarAutor()}
                        placeholder="Ej: Cervantes, Quevedo, Lope de Vega..."
                        className={inputClass}
                    />
                    <button
                        onClick={buscarAutor}
                        disabled={loading}
                        className="bg-blue-700 hover:bg-blue-800 text-white px-6 py-3 rounded-lg font-semibold tracking-wide transition-colors disabled:opacity-50 whitespace-nowrap"
                    >
                        {loading ? 'Buscando...' : '🔎 Buscar'}
                    </button>
                </div>
                {error && <p className="text-red-600 text-sm mt-3">❌ {error}</p>}
            </div>

            {/* Search results */}
            {(resultado || loading) && (
                <div>
                    <h2 className="font-serif text-xl font-bold text-stone-800 mb-4 flex items-center gap-3">
                        <span className="w-1 h-6 bg-blue-500 rounded-full" />
                        Resultados de la búsqueda
                    </h2>
                    <ImportResults resultado={resultado} loading={loading} error={null} />
                </div>
            )}

            {/* Obras grouped by author */}
            <div>
                <div className="flex items-center justify-between mb-4">
                    <h2 className="font-serif text-xl font-bold text-stone-800 flex items-center gap-3">
                        <span className="w-1 h-6 bg-stone-400 rounded-full" />
                        Obras en la Base de Datos
                    </h2>
                    {totalPaginas > 1 && (
                        <span className="text-stone-400 text-sm">Página {paginaActual} / {totalPaginas}</span>
                    )}
                </div>

                {listLoading ? (
                    <LoadingSpinner label="Cargando obras..." />
                ) : obrasLista.length === 0 ? (
                    <EmptyState
                        icon="📭"
                        title="No hay obras registradas"
                        description="Usa el buscador de arriba para importar obras desde la BNE"
                    />
                ) : (
                    <>
                        <div className="space-y-4">
                            {Object.entries(obrasPorAutor).map(([autor, obras]) => (
                                <div key={autor} className="bg-white border border-stone-200 rounded-xl overflow-hidden shadow-sm">
                                    <div className="bg-stone-50 border-b border-stone-100 px-5 py-3 flex items-center gap-3">
                                        <span className="text-stone-400">👤</span>
                                        <span className="font-semibold text-stone-700">{autor}</span>
                                        <span className="ml-auto text-xs bg-stone-200 text-stone-600 px-2 py-0.5 rounded-full">
                                            {obras.length} obra{obras.length !== 1 ? 's' : ''}
                                        </span>
                                    </div>
                                    {obras.map((obra, idx) => (
                                        <div key={idx} className={`flex items-center gap-3 px-5 py-3 text-sm ${idx < obras.length - 1 ? 'border-b border-stone-100' : ''}`}>
                                            <span className="w-1.5 h-1.5 bg-blue-400 rounded-full flex-shrink-0" />
                                            <span className="text-stone-800 flex-1">{obra.titulo}</span>
                                            {obra.anio && <span className="text-stone-400 text-xs">{obra.anio}</span>}
                                            <span className="text-xs bg-stone-100 text-stone-500 px-2 py-0.5 rounded-full">
                                                {obra.tipo_publicacion || 'obra'}
                                            </span>
                                            {obra.enlace && (
                                                <a href={obra.enlace} target="_blank" rel="noopener noreferrer"
                                                    className="text-xs text-amber-600 hover:underline">BNE ↗</a>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            ))}
                        </div>

                        {totalPaginas > 1 && (
                            <div className="flex justify-center gap-2 mt-6">
                                <button
                                    onClick={() => cargarObras(paginaActual - 1)}
                                    disabled={paginaActual === 1}
                                    className="px-4 py-2 rounded-lg border border-stone-200 text-stone-600 hover:bg-stone-50 disabled:opacity-40 text-sm transition-colors"
                                >
                                    ← Anterior
                                </button>
                                <span className="px-4 py-2 text-stone-500 text-sm">{paginaActual} / {totalPaginas}</span>
                                <button
                                    onClick={() => cargarObras(paginaActual + 1)}
                                    disabled={paginaActual === totalPaginas}
                                    className="px-4 py-2 rounded-lg border border-stone-200 text-stone-600 hover:bg-stone-50 disabled:opacity-40 text-sm transition-colors"
                                >
                                    Siguiente →
                                </button>
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
}
