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
        <div className="page">
            {/* Pestañas */}
            <div className="tabs">
                <nav className="tabs__list">
                    {TABS.map(tab => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`tabs__tab ${activeTab === tab.id ? 'tabs__tab--active' : ''}`}
                        >
                            <span className="tabs__icon">{tab.icon}</span>{tab.label}
                        </button>
                    ))}
                </nav>
            </div>

            {/* Formulario */}
            <div className="panel periodicos-page__section">
                {activeTab === 'url' && (
                    <>
                        <h2 className="panel__title">Importar por URL</h2>
                        <p className="panel__subtitle">Pega la URL de datos.bne.es directamente</p>
                        <div className="form">
                            <div className="form__group">
                                <label className="form__label">Dirección URL</label>
                                <input type="text" value={url} onChange={e => setUrl(e.target.value)}
                                    placeholder="https://datos.bne.es/data/XX0000000" className="form__input" />
                            </div>
                            <div className="form__group">
                                <button onClick={importarURL} disabled={loading} className="button button--primary button--block">
                                    {loading ? 'Importando...' : '↓ Importar Obra'}
                                </button>
                            </div>
                        </div>
                    </>
                )}

                {activeTab === 'nombre' && (
                    <>
                        <h2 className="panel__title">Buscar en BNE y Guardar</h2>
                        <p className="panel__subtitle panel__subtitle--tight">
                            Busca en <strong>datos.bne.es</strong> y en tu base de datos local.
                        </p>
                        <p className="panel__note">
                            Las obras de BNE no registradas en tu BD se guardan automáticamente.
                        </p>
                        <div className="form">
                            <div className="form__group">
                                <label className="form__label">Nombre o palabra clave</label>
                                <input type="text" value={nombre} onChange={e => setNombre(e.target.value)}
                                    placeholder="Ej: Quijote, Periódico ABC, La Vanguardia..."
                                    className="form__input form__input--emerald"
                                    onKeyPress={e => e.key === 'Enter' && buscarPorNombre()} />
                            </div>
                            <div className="form__group">
                                <button onClick={buscarPorNombre} disabled={loading} className="button button--emerald button--block">
                                    {loading ? 'Buscando y guardando...' : '🔎 Buscar en BNE y Guardar en BD'}
                                </button>
                            </div>
                        </div>
                    </>
                )}

                {activeTab === 'titulo' && (
                    <>
                        <h2 className="panel__title">Importar por Título</h2>
                        <p className="panel__subtitle panel__subtitle--tight">
                            Importa todas las obras cuyo <strong>título contenga</strong> la frase indicada.
                        </p>
                        <p className="panel__note">Para buscar varios títulos a la vez, sepáralos con comas.</p>
                        <div className="form">
                            <div className="form__group">
                                <label className="form__label">Título o frase</label>
                                <input type="text" value={titulo} onChange={e => setTitulo(e.target.value)}
                                    placeholder="Ej: La Vanguardia, periódico de damas, El Quijote..."
                                    className="form__input" onKeyPress={e => e.key === 'Enter' && importarTitulo()} />
                            </div>
                            <div className="form__group">
                                <button onClick={importarTitulo} disabled={loading} className="button button--primary button--block">
                                    {loading ? 'Importando...' : '↓ Importar Obras'}
                                </button>
                            </div>
                        </div>
                    </>
                )}

                {activeTab === 'rango-fechas' && (
                    <>
                        <h2 className="panel__title">Buscar por Rango de Fechas</h2>
                        <p className="panel__subtitle">Encuentra todos los periódicos dentro de un intervalo específico</p>
                        <div className="form">
                            <div className="form__grid">
                                <div className="form__group">
                                    <label className="form__label">📅 Fecha desde</label>
                                    <input type="date" value={fechaDesde} onChange={e => setFechaDesde(e.target.value)}
                                        min="1500-01-01" max="2100-12-31" className="form__input" />
                                </div>
                                <div className="form__group">
                                    <label className="form__label">📅 Fecha hasta</label>
                                    <input type="date" value={fechaHasta} onChange={e => setFechaHasta(e.target.value)}
                                        min="1500-01-01" max="2100-12-31" className="form__input" />
                                </div>
                            </div>
                            <div className="form__group">
                                <div className="form__hint">
                                    ℹ️ Filtro automático por periódicos BIMO (prefijo https://datos.bne.es/resource/bimo...)
                                </div>
                            </div>
                            <div className="form__group">
                                <button onClick={buscarPorRangoFechas} disabled={loading} className="button button--primary button--block">
                                    {loading ? 'Buscando...' : '🔍 Buscar Periódicos'}
                                </button>
                            </div>
                        </div>
                    </>
                )}

                {activeTab === 'lote' && (
                    <>
                        <h2 className="panel__title">Importación en Lote</h2>
                        <p className="panel__subtitle">Una URL o título por línea</p>
                        <div className="form">
                            <div className="form__group">
                                <label className="form__label">URLs o títulos</label>
                                <textarea value={loteItems} onChange={e => setLoteItems(e.target.value)}
                                    placeholder={"https://datos.bne.es/edicion/bimo0000659916.html\nhttps://datos.bne.es/data/XX0000000\nhttps://datos.bne.es/edicion/a6065627.html"}
                                    rows={6} className="form__textarea" />
                            </div>
                            <div className="form__group">
                                <button onClick={importarLote} disabled={loading} className="button button--primary button--block">
                                    {loading ? 'Procesando...' : '↓ Importar Lote'}
                                </button>
                            </div>
                        </div>
                    </>
                )}
            </div>

            {/* Resultados */}
            {(resultado || loading || error) && (
                <div className="periodicos-page__section">
                    <h2 className="results-heading">
                        <span className="results-heading__bar results-heading__bar--amber" />
                        Resultados
                    </h2>
                    <ImportResults resultado={resultado} loading={loading} error={error} />
                </div>
            )}
        </div>
    );
}
