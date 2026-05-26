import { useState, useEffect } from 'react';
import { API_BASE_URL, PER_PAGE } from '../constants';
import LoadingSpinner from '../components/LoadingSpinner';
import EmptyState from '../components/EmptyState';
import SectionHeader from '../components/SectionHeader';
import BarChart from '../components/BarChart';
import ImportResults from '../components/ImportResults';
import ImagenPreview from '../components/ImagenPreview';

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

    // Mapa nombre_completo (en minúsculas) → imagen_url, para mostrar el
    // retrato del autor en la cabecera de cada grupo de obras.
    const [autoresImg, setAutoresImg] = useState({});

    useEffect(() => {
        const cargarStats = async () => {
            try {
                const res = await fetch(`${API_BASE_URL}/api/estadisticas/resumen`);
                if (res.ok) setStats(await res.json());
            } catch { /* stats son opcionales */ } finally {
                setStatsLoading(false);
            }
        };
        const cargarAutoresImg = async () => {
            try {
                const res = await fetch(`${API_BASE_URL}/api/autores?per_page=500`);
                if (res.ok) {
                    const data = await res.json();
                    const mapa = {};
                    (data.data || []).forEach(a => {
                        if (a.imagen_url) mapa[(a.nombre_completo || '').toLowerCase()] = a.imagen_url;
                    });
                    setAutoresImg(mapa);
                }
            } catch { /* retratos son opcionales */ }
        };
        cargarStats();
        cargarAutoresImg();
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

    return (
        <div className="page">

            {/* Estadísticas */}
            <section className="autores-page__section">
                <div className="stats-grid">
                    {statsLoading ? (
                        <div className="stat-card stat-card--span">
                            <LoadingSpinner label="Cargando estadísticas..." />
                        </div>
                    ) : stats ? (
                        <>
                            <div className="stat-card">
                                <p className="stat-card__value">{stats.resumen?.total_obras ?? '—'}</p>
                                <p className="stat-card__label">Total obras</p>
                            </div>
                            <div className="stat-card stat-card--blue">
                                <p className="stat-card__value stat-card__value--blue">
                                    {stats.resumen?.autores_principales?.length ?? '—'}
                                </p>
                                <p className="stat-card__label">Autores registrados</p>
                            </div>
                            <div className="stat-card stat-card--amber">
                                <p className="stat-card__value stat-card__value--amber">
                                    {stats.resumen?.obras_por_tipo?.length ?? '—'}
                                </p>
                                <p className="stat-card__label">Tipos de obra</p>
                            </div>
                        </>
                    ) : (
                        <div className="stat-card stat-card--span">
                            <p className="stat-card__message">
                                Estadísticas no disponibles — asegúrate de que el backend está en marcha
                            </p>
                        </div>
                    )}
                </div>
            </section>

            {/* Gráficas */}
            {stats && (stats.resumen?.autores_principales?.length > 0 || stats.resumen?.obras_por_tipo?.length > 0) && (
                <section className="autores-page__section">
                    <div className="charts-grid">
                        {stats.resumen?.autores_principales?.length > 0 && (
                            <div className="panel">
                                <SectionHeader color="blue" label="Autores principales" />
                                <BarChart items={stats.resumen.autores_principales.slice(0, 7)} color="blue" />
                            </div>
                        )}
                        {stats.resumen?.obras_por_tipo?.length > 0 && (
                            <div className="panel">
                                <SectionHeader color="amber" label="Obras por tipo" />
                                <BarChart items={stats.resumen.obras_por_tipo} color="amber" labelKey="tipo" />
                            </div>
                        )}
                    </div>
                </section>
            )}

            {/* Buscador */}
            <section className="autores-page__section">
                <div className="panel">
                    <h2 className="panel__title">Buscar Autor en BNE</h2>
                    <p className="panel__subtitle">
                        Busca en <strong>datos.bne.es</strong> y en tu base de datos local.
                        Las obras encontradas se guardan automáticamente.
                    </p>
                    <div className="search-box__row">
                        <input
                            type="text"
                            value={query}
                            onChange={e => setQuery(e.target.value)}
                            onKeyPress={e => e.key === 'Enter' && buscarAutor()}
                            placeholder="Ej: Cervantes, Quevedo, Lope de Vega..."
                            aria-label="Buscar autor en datos.bne.es"
                            className="form__input form__input--blue"
                        />
                        <button onClick={buscarAutor} disabled={loading} className="button button--blue">
                            {loading ? 'Buscando...' : 'Buscar'}
                        </button>
                    </div>
                    {error && <p className="search-box__error" role="alert"><strong>Error:</strong> {error}</p>}
                </div>
            </section>

            {/* Resultados de la búsqueda */}
            {(resultado || loading) && (
                <section className="autores-page__section">
                    <h2 className="results-heading">
                        <span className="results-heading__bar results-heading__bar--blue" />
                        Resultados de la búsqueda
                    </h2>
                    <ImportResults resultado={resultado} loading={loading} error={null} />
                </section>
            )}

            {/* Obras en la base de datos */}
            <section className="autores-page__section">
                <div className="list-header">
                    <h2 className="results-heading">
                        <span className="results-heading__bar" />
                        Obras en la Base de Datos
                    </h2>
                    {totalPaginas > 1 && (
                        <span className="results-heading__meta">Página {paginaActual} / {totalPaginas}</span>
                    )}
                </div>

                {listLoading ? (
                    <LoadingSpinner label="Cargando obras..." />
                ) : obrasLista.length === 0 ? (
                    <EmptyState
                        title="No hay obras registradas"
                        description="Usa el buscador de arriba para importar obras desde la BNE"
                    />
                ) : (
                    <>
                        <div>
                            {Object.entries(obrasPorAutor).map(([autor, obras]) => (
                                <div key={autor} className="obras-group">
                                    <div className="obras-group__header">
                                        <ImagenPreview src={autoresImg[autor.toLowerCase()]} alt={autor} size="sm" tipo="autor" />
                                        <span className="obras-group__author">{autor}</span>
                                        <span className="obras-group__count">
                                            {obras.length} obra{obras.length !== 1 ? 's' : ''}
                                        </span>
                                    </div>
                                    {obras.map((obra, idx) => (
                                        <div key={idx} className="obras-group__item">
                                            <ImagenPreview src={obra.imagen_url} alt={obra.titulo} size="sm" tipo="obra" />
                                            <span className="obra-list__title">{obra.titulo}</span>
                                            {obra.anio && <span className="obra-list__year">{obra.anio}</span>}
                                            <span className="obra-list__type">{obra.tipo_publicacion || 'obra'}</span>
                                            {obra.enlace && (
                                                <a href={obra.enlace} target="_blank" rel="noopener noreferrer" className="obra-list__link">
                                                    Ver en BNE
                                                </a>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            ))}
                        </div>

                        {totalPaginas > 1 && (
                            <div className="pagination">
                                <button
                                    onClick={() => cargarObras(paginaActual - 1)}
                                    disabled={paginaActual === 1}
                                    className="pagination__button"
                                >
                                    ← Anterior
                                </button>
                                <span className="pagination__status">{paginaActual} / {totalPaginas}</span>
                                <button
                                    onClick={() => cargarObras(paginaActual + 1)}
                                    disabled={paginaActual === totalPaginas}
                                    className="pagination__button"
                                >
                                    Siguiente →
                                </button>
                            </div>
                        )}
                    </>
                )}
            </section>
        </div>
    );
}
