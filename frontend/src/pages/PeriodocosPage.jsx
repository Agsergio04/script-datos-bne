import { useState, useEffect } from 'react';
import { API_BASE_URL } from '../constants';
import ImportResults from '../components/ImportResults';

const TABS = [
    { id: 'nombre',       icon: '🔎', label: 'Buscar en BD'   },
    { id: 'url',          icon: '🔗', label: 'Por URL'        },
    { id: 'titulo',       icon: '🔍', label: 'Por Título BNE' },
    { id: 'rango-fechas', icon: '📅', label: 'Por Fechas'     },
    { id: 'lote',         icon: '📦', label: 'Lote'           },
];

const inputClass = "w-full px-4 py-3 border border-stone-200 rounded-lg bg-stone-50 text-stone-800 placeholder-stone-400 focus:outline-none focus:ring-2 focus:ring-amber-400 focus:border-amber-400 transition-colors";
const btnPrimary = "w-full bg-stone-700 hover:bg-stone-800 text-white py-3 px-6 rounded-lg font-semibold tracking-wide transition-colors disabled:opacity-50 disabled:cursor-not-allowed";
const btnEmerald = "w-full bg-emerald-700 hover:bg-emerald-800 text-white py-3 px-6 rounded-lg font-semibold tracking-wide transition-colors disabled:opacity-50 disabled:cursor-not-allowed";
const labelClass = "block text-xs font-semibold tracking-widest text-stone-500 uppercase mb-2";

export default function PeriodocosPage({ queryParams }) {
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
        if (queryParams.url && !resultado) importarURL();
        else if ((queryParams.titulo || queryParams.periodicode) && !resultado) importarTitulo();
        else if (queryParams.fechaDesde && queryParams.fechaHasta && !resultado) setActiveTab('rango-fechas');
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
            const res = await fetch(`${API_BASE_URL}/api/importar/url`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: url.trim() }),
            });
            if (!res.ok) { const e = await res.json().catch(() => ({})); throw new Error(e.error || `Error ${res.status}`); }
            setResultado(await res.json());
        } catch (err) { setError(err.message); } finally { setLoading(false); }
    };

    const importarTitulo = async () => {
        if (!titulo.trim()) { setError('Por favor ingresa un título'); return; }
        setLoading(true); setError(null);
        try {
            const res = await fetch(`${API_BASE_URL}/api/importar/titulo`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ titulo: titulo.trim() }),
            });
            if (!res.ok) { const e = await res.json().catch(() => ({})); throw new Error(e.error || `Error ${res.status}`); }
            setResultado(await res.json());
        } catch (err) { setError(err.message); } finally { setLoading(false); }
    };

    const buscarPorNombre = async () => {
        if (!nombre.trim()) { setError('Por favor ingresa un nombre o palabra clave'); return; }
        setLoading(true); setError(null);
        try {
            const res = await fetch(`${API_BASE_URL}/api/importar/nombre`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nombre: nombre.trim(), limite: 20 }),
            });
            if (!res.ok) { const e = await res.json().catch(() => ({})); throw new Error(e.error || `Error ${res.status}`); }
            setResultado(await res.json());
        } catch (err) { setError(err.message); } finally { setLoading(false); }
    };

    const importarLote = async () => {
        const lineas = loteItems.trim().split('\n').filter(l => l.trim());
        if (lineas.length === 0) { setError('Por favor ingresa al menos un título o URL'); return; }
        const obras = lineas.map(l => l.includes('datos.bne.es') ? { url: l } : { titulo: l });
        setLoading(true); setError(null);
        try {
            const res = await fetch(`${API_BASE_URL}/api/importar/lote`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ obras }),
            });
            if (!res.ok) { const e = await res.json().catch(() => ({})); throw new Error(e.error || `Error ${res.status}`); }
            setResultado(await res.json());
        } catch (err) { setError(err.message); } finally { setLoading(false); }
    };

    const buscarPorRangoFechas = async () => {
        if (!fechaDesde || !fechaHasta) { setError('Por favor ingresa las fechas de inicio y fin'); return; }
        const dDesde = new Date(fechaDesde), dHasta = new Date(fechaHasta);
        if (dDesde > dHasta) { setError('La fecha de inicio no puede ser posterior a la fecha final'); return; }
        if (dDesde.getFullYear() < 1500 || dDesde.getFullYear() > 2100) { setError('Año inválido en fecha de inicio. Use rango 1500-2100'); return; }
        if (dHasta.getFullYear() < 1500 || dHasta.getFullYear() > 2100) { setError('Año inválido en fecha final. Use rango 1500-2100'); return; }
        setLoading(true); setError(null);
        try {
            const res = await fetch(
                `${API_BASE_URL}/api/periodicos/rango-fechas?fecha_desde=${fechaDesde}&fecha_hasta=${fechaHasta}&page=1&per_page=50`
            );
            if (!res.ok) { const e = await res.json().catch(() => ({})); throw new Error(e.error || `Error ${res.status}`); }
            const data = await res.json();
            setResultado({
                nombre_buscado: `Periódicos del ${fechaDesde} al ${fechaHasta}`,
                resultados_bd: data.data || [],
                resultados_bne: [],
                total_encontrados: data.pagination.total,
            });
        } catch (err) { setError(err.message); } finally { setLoading(false); }
    };

    return (
        <div className="max-w-4xl mx-auto px-6 py-8">
            {/* Tabs */}
            <div className="border-b border-stone-200 mb-8">
                <nav className="flex overflow-x-auto -mb-px">
                    {TABS.map(tab => (
                        <button key={tab.id} onClick={() => setActiveTab(tab.id)}
                            className={`px-5 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-all ${
                                activeTab === tab.id
                                    ? 'border-amber-600 text-amber-700 bg-amber-50/40'
                                    : 'border-transparent text-stone-500 hover:text-stone-700 hover:border-stone-300'
                            }`}>
                            <span className="mr-1.5">{tab.icon}</span>{tab.label}
                        </button>
                    ))}
                </nav>
            </div>

            {/* Form */}
            <div className="bg-white rounded-xl border border-stone-200 shadow-sm p-8 mb-8">
                {activeTab === 'url' && (
                    <>
                        <h2 className="font-serif text-xl font-bold text-stone-800 mb-1">Importar por URL</h2>
                        <p className="text-stone-500 text-sm mb-6">Pega la URL de datos.bne.es directamente</p>
                        <div className="space-y-4">
                            <div>
                                <label className={labelClass}>Dirección URL</label>
                                <input type="text" value={url} onChange={e => setUrl(e.target.value)}
                                    placeholder="https://datos.bne.es/data/XX0000000" className={inputClass} />
                            </div>
                            <button onClick={importarURL} disabled={loading} className={btnPrimary}>
                                {loading ? 'Importando...' : '↓ Importar Obra'}
                            </button>
                        </div>
                    </>
                )}

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
                                <input type="text" value={nombre} onChange={e => setNombre(e.target.value)}
                                    placeholder="Ej: Quijote, Periódico ABC, La Vanguardia..."
                                    className={inputClass.replace('focus:ring-amber-400 focus:border-amber-400', 'focus:ring-emerald-400 focus:border-emerald-400')}
                                    onKeyPress={e => e.key === 'Enter' && buscarPorNombre()} />
                            </div>
                            <button onClick={buscarPorNombre} disabled={loading} className={btnEmerald}>
                                {loading ? 'Buscando y guardando...' : '🔎 Buscar en BNE y Guardar en BD'}
                            </button>
                        </div>
                    </>
                )}

                {activeTab === 'titulo' && (
                    <>
                        <h2 className="font-serif text-xl font-bold text-stone-800 mb-1">Importar por Título</h2>
                        <p className="text-stone-500 text-sm mb-1">
                            Importa todas las obras cuyo <strong className="text-stone-600">título contenga</strong> la frase indicada.
                        </p>
                        <p className="text-stone-400 text-xs mb-6 italic">Para buscar varios títulos a la vez, sepáralos con comas.</p>
                        <div className="space-y-4">
                            <div>
                                <label className={labelClass}>Título o frase</label>
                                <input type="text" value={titulo} onChange={e => setTitulo(e.target.value)}
                                    placeholder="Ej: La Vanguardia, periódico de damas, El Quijote..."
                                    className={inputClass} onKeyPress={e => e.key === 'Enter' && importarTitulo()} />
                            </div>
                            <button onClick={importarTitulo} disabled={loading} className={btnPrimary}>
                                {loading ? 'Importando...' : '↓ Importar Obras'}
                            </button>
                        </div>
                    </>
                )}

                {activeTab === 'rango-fechas' && (
                    <>
                        <h2 className="font-serif text-xl font-bold text-stone-800 mb-1">Buscar por Rango de Fechas</h2>
                        <p className="text-stone-500 text-sm mb-6">Encuentra todos los periódicos dentro de un intervalo específico</p>
                        <div className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className={labelClass}>📅 Fecha desde</label>
                                    <input type="date" value={fechaDesde} onChange={e => setFechaDesde(e.target.value)}
                                        min="1500-01-01" max="2100-12-31" className={inputClass} />
                                </div>
                                <div>
                                    <label className={labelClass}>📅 Fecha hasta</label>
                                    <input type="date" value={fechaHasta} onChange={e => setFechaHasta(e.target.value)}
                                        min="1500-01-01" max="2100-12-31" className={inputClass} />
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

                {activeTab === 'lote' && (
                    <>
                        <h2 className="font-serif text-xl font-bold text-stone-800 mb-1">Importación en Lote</h2>
                        <p className="text-stone-500 text-sm mb-6">Una URL o título por línea</p>
                        <div className="space-y-4">
                            <div>
                                <label className={labelClass}>URLs o títulos</label>
                                <textarea value={loteItems} onChange={e => setLoteItems(e.target.value)}
                                    placeholder={"https://datos.bne.es/edicion/bimo0000659916.html\nhttps://datos.bne.es/data/XX0000000\nhttps://datos.bne.es/edicion/a6065627.html"}
                                    rows={6} className={`${inputClass} font-mono text-xs resize-none`} />
                            </div>
                            <button onClick={importarLote} disabled={loading} className={btnPrimary}>
                                {loading ? 'Procesando...' : '↓ Importar Lote'}
                            </button>
                        </div>
                    </>
                )}
            </div>

            {/* Results */}
            {(resultado || loading || error) && (
                <div className="mb-8">
                    <h2 className="font-serif text-xl font-bold text-stone-800 mb-4 flex items-center gap-3">
                        <span className="w-1 h-6 bg-amber-500 rounded-full" />
                        Resultados
                    </h2>
                    <ImportResults resultado={resultado} loading={loading} error={error} />
                </div>
            )}
        </div>
    );
}
