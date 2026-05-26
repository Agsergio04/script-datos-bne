import { useState, useEffect } from 'react';
import { API_BASE_URL } from '../constants';
import ImportResults from '../components/ImportResults';
import ObraDetalleCard from '../components/ObraDetalleCard';
import LoadingSpinner from '../components/LoadingSpinner';
import EmptyState from '../components/EmptyState';

const TABS = [
    { id: 'nombre',       label: 'Catálogo BD'    },
    { id: 'url',          label: 'Por URL'        },
    { id: 'titulo',       label: 'Por Título BNE' },
    { id: 'rango-fechas', label: 'Por Fechas'     },
    { id: 'lote',         label: 'Lote'           },
];

export default function PeriodocosPage({ queryParams }) {
    const [activeTab, setActiveTab] = useState('nombre');
    const [url, setUrl] = useState(queryParams.url || '');
    const [titulo, setTitulo] = useState(queryParams.titulo || queryParams.periodicode || '');
    const [loteItems, setLoteItems] = useState('');
    const [fechaDesde, setFechaDesde] = useState(queryParams.fechaDesde || '');
    const [fechaHasta, setFechaHasta] = useState(queryParams.fechaHasta || '');
    const [resultado, setResultado] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Catálogo local + filtro dinámico (pestaña "Catálogo BD")
    const [catalogo, setCatalogo] = useState([]);
    const [catalogoLoading, setCatalogoLoading] = useState(true);
    const [filtroCatalogo, setFiltroCatalogo] = useState('');

    const cargarCatalogo = async () => {
        setCatalogoLoading(true);
        try {
            const res = await fetch(`${API_BASE_URL}/api/obras?per_page=1000`);
            if (res.ok) {
                const d = await res.json();
                setCatalogo(d.data || []);
            }
        } catch { /* el catálogo es opcional si el backend no responde */ } finally {
            setCatalogoLoading(false);
        }
    };

    // Carga el catálogo al montar y lo refresca tras cada importación
    useEffect(() => { cargarCatalogo(); }, [resultado]);

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

    // Filtro dinámico del catálogo (cliente, instantáneo)
    const filtro = filtroCatalogo.trim().toLowerCase();
    const catalogoFiltrado = filtro
        ? catalogo.filter(o =>
            [o.titulo, o.nombre_autor, o.autor_firma, o.tema_principal, o.tipo_publicacion, o.anio]
                .some(campo => String(campo ?? '').toLowerCase().includes(filtro)))
        : catalogo;

    return (
        <div className="page">
            {/* Pestañas */}
            <div className="tabs">
                <nav className="tabs__list" aria-label="Modos de consulta e importación">
                    {TABS.map(tab => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            aria-current={activeTab === tab.id ? 'true' : undefined}
                            className={`tabs__tab ${activeTab === tab.id ? 'tabs__tab--active' : ''}`}
                        >
                            {tab.label}
                        </button>
                    ))}
                </nav>
            </div>

            {/* Formulario */}
            <div className="panel periodicos-page__section">
                {activeTab === 'nombre' && (
                    <>
                        <h2 className="panel__title">Catálogo en la Base de Datos</h2>
                        <p className="panel__subtitle">
                            Todas las obras guardadas en tu BD. Escribe para <strong>filtrar al instante</strong> por
                            título, autor, tema, tipo o año.
                        </p>
                        <div className="form">
                            <div className="form__group">
                                <label className="form__label" htmlFor="filtro-catalogo">Filtrar catálogo</label>
                                <input id="filtro-catalogo" type="text" value={filtroCatalogo} onChange={e => setFiltroCatalogo(e.target.value)}
                                    placeholder="Ej: Quijote, Cervantes, novela, 1920..."
                                    aria-label="Filtrar el catálogo de la base de datos"
                                    className="form__input form__input--emerald" />
                            </div>
                        </div>
                    </>
                )}

                {activeTab === 'url' && (
                    <>
                        <h2 className="panel__title">Importar por URL</h2>
                        <p className="panel__subtitle">Pega la URL de datos.bne.es directamente</p>
                        <div className="form">
                            <div className="form__group">
                                <label className="form__label" htmlFor="import-url">Dirección URL</label>
                                <input id="import-url" type="text" value={url} onChange={e => setUrl(e.target.value)}
                                    placeholder="https://datos.bne.es/data/XX0000000" className="form__input" />
                            </div>
                            <div className="form__group">
                                <button onClick={importarURL} disabled={loading} className="button button--primary button--block">
                                    {loading ? 'Importando...' : 'Importar obra'}
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
                                <label className="form__label" htmlFor="import-titulo">Título o frase</label>
                                <input id="import-titulo" type="text" value={titulo} onChange={e => setTitulo(e.target.value)}
                                    placeholder="Ej: La Vanguardia, periódico de damas, El Quijote..."
                                    className="form__input" onKeyPress={e => e.key === 'Enter' && importarTitulo()} />
                            </div>
                            <div className="form__group">
                                <button onClick={importarTitulo} disabled={loading} className="button button--primary button--block">
                                    {loading ? 'Importando...' : 'Importar obras'}
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
                                    <label className="form__label" htmlFor="fecha-desde">Fecha desde</label>
                                    <input id="fecha-desde" type="date" value={fechaDesde} onChange={e => setFechaDesde(e.target.value)}
                                        min="1500-01-01" max="2100-12-31" className="form__input" />
                                </div>
                                <div className="form__group">
                                    <label className="form__label" htmlFor="fecha-hasta">Fecha hasta</label>
                                    <input id="fecha-hasta" type="date" value={fechaHasta} onChange={e => setFechaHasta(e.target.value)}
                                        min="1500-01-01" max="2100-12-31" className="form__input" />
                                </div>
                            </div>
                            <div className="form__group">
                                <div className="form__hint">
                                    Filtro automático por periódicos BIMO (prefijo https://datos.bne.es/resource/bimo...)
                                </div>
                            </div>
                            <div className="form__group">
                                <button onClick={buscarPorRangoFechas} disabled={loading} className="button button--primary button--block">
                                    {loading ? 'Buscando...' : 'Buscar periódicos'}
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
                                <label className="form__label" htmlFor="lote-items">URLs o títulos</label>
                                <textarea id="lote-items" value={loteItems} onChange={e => setLoteItems(e.target.value)}
                                    placeholder={"https://datos.bne.es/edicion/bimo0000659916.html\nhttps://datos.bne.es/data/XX0000000\nhttps://datos.bne.es/edicion/a6065627.html"}
                                    rows={6} className="form__textarea" />
                            </div>
                            <div className="form__group">
                                <button onClick={importarLote} disabled={loading} className="button button--primary button--block">
                                    {loading ? 'Procesando...' : 'Importar lote'}
                                </button>
                            </div>
                        </div>
                    </>
                )}
            </div>

            {/* Catálogo filtrado (pestaña "Catálogo BD") */}
            {activeTab === 'nombre' && (
                <div className="periodicos-page__section">
                    <div className="list-header">
                        <h2 className="results-heading">
                            <span className="results-heading__bar results-heading__bar--amber" />
                            Catálogo
                        </h2>
                        <span className="results-heading__meta">
                            {catalogoFiltrado.length} obra{catalogoFiltrado.length !== 1 ? 's' : ''}
                            {filtro && ` de ${catalogo.length}`}
                        </span>
                    </div>

                    {catalogoLoading ? (
                        <LoadingSpinner label="Cargando catálogo..." />
                    ) : catalogoFiltrado.length === 0 ? (
                        <EmptyState
                            title={catalogo.length === 0 ? 'No hay obras en la base de datos' : 'Sin coincidencias'}
                            description={catalogo.length === 0
                                ? 'Importa obras desde las pestañas Por URL, Por Título BNE o Lote'
                                : 'Prueba con otro término de filtro'}
                        />
                    ) : (
                        <div className="stack--sm">
                            {catalogoFiltrado.map(obra => (
                                <ObraDetalleCard key={obra.id} obra={obra} fuente="BD Local" />
                            ))}
                        </div>
                    )}
                </div>
            )}

            {/* Resultados de importación (resto de pestañas) */}
            {activeTab !== 'nombre' && (resultado || loading || error) && (
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
