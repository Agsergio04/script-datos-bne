import LoadingSpinner from './LoadingSpinner';
import SectionHeader from './SectionHeader';
import ObraDetalleCard from './ObraDetalleCard';
import ListaObras from './ListaObras';
import FieldLabel from './FieldLabel';
import EmptyState from './EmptyState';

export default function ImportResults({ resultado, loading, error }) {
    if (loading) return (
        <div className="panel">
            <LoadingSpinner />
        </div>
    );

    if (error) return (
        <div className="import-card import-card--info" style={{ borderLeftColor: 'var(--color-red-400)' }}>
            <p className="obra-list__error">❌ {error}</p>
        </div>
    );

    if (!resultado) return null;

    // ── Búsqueda por nombre ─────────────────────────────────
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
            <div className="stack">
                <div className="import-banner">
                    <p className="import-banner__text">
                        🔎 Búsqueda: "<strong>{nombre_buscado}</strong>" —{' '}
                        <strong>{total_encontrados}</strong> resultados encontrados
                    </p>
                    {resultado.mensaje && <p className="import-banner__message">{resultado.mensaje}</p>}
                </div>

                {(guardadas.length > 0 || ya_en_bd.length > 0 || errores_bne.length > 0) && (
                    <div className="stats-grid">
                        <div className="stat-card stat-card--emerald">
                            <p className="stat-card__value stat-card__value--emerald stat-card__value--md">{guardadas.length}</p>
                            <p className="stat-card__label stat-card__label--emerald">Nuevas guardadas</p>
                        </div>
                        <div className="stat-card stat-card--amber">
                            <p className="stat-card__value stat-card__value--amber stat-card__value--md">{ya_en_bd.length}</p>
                            <p className="stat-card__label stat-card__label--amber">Ya en BD</p>
                        </div>
                        <div className="stat-card stat-card--red">
                            <p className="stat-card__value stat-card__value--red stat-card__value--md">{errores_bne.length}</p>
                            <p className="stat-card__label stat-card__label--red">Errores</p>
                        </div>
                    </div>
                )}

                {resultados_bd.length > 0 && (
                    <div>
                        <SectionHeader color="stone" label="Base de Datos Local" count={resultados_bd.length} />
                        <div className="stack--sm">
                            {resultados_bd.map((obra, idx) => <ObraDetalleCard key={idx} obra={obra} fuente="📍 BD Local" />)}
                        </div>
                    </div>
                )}

                {guardadas.length > 0 && (
                    <div>
                        <SectionHeader color="emerald" label="Nuevas obras guardadas desde BNE" count={guardadas.length} />
                        <ListaObras obras={guardadas} dotColor="obra-list__dot--emerald" showLink />
                    </div>
                )}

                {ya_en_bd.length > 0 && (
                    <div>
                        <SectionHeader color="amber" label="Ya existían en BD" count={ya_en_bd.length} />
                        <ListaObras obras={ya_en_bd} dotColor="obra-list__dot--amber" />
                    </div>
                )}

                {errores_bne.length > 0 && (
                    <div>
                        <SectionHeader color="red" label="Errores" count={errores_bne.length} />
                        <div className="obra-list">
                            {errores_bne.map((err, idx) => (
                                <div key={idx} className="obra-list__item obra-list__item--top">
                                    <span className="obra-list__dot obra-list__dot--red" />
                                    <span className="obra-list__error">
                                        <span className="obra-list__error-name">{err.titulo}</span>: {err.error}
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

    // ── Importación individual (url o título) ───────────────
    if (resultado.data) {
        const obra = resultado.data;
        const fuente = resultado.fuente;
        const esNueva = resultado.message.includes('importada') && !resultado.message.includes('existe');

        let cardModifier, sourceModifier, icon;
        if (esNueva) {
            cardModifier = 'import-card--new'; sourceModifier = 'import-card__source--new'; icon = '✅';
        } else if (fuente === 'BD local') {
            cardModifier = 'import-card--local'; sourceModifier = 'import-card__source--local'; icon = '📚';
        } else {
            cardModifier = 'import-card--info'; sourceModifier = ''; icon = 'ℹ️';
        }

        return (
            <div className={`import-card ${cardModifier}`}>
                <div className="import-card__body">
                    <span className="import-card__icon">{icon}</span>
                    <div className="import-card__content">
                        <p className="import-card__title">{resultado.message}</p>
                        {fuente && (
                            <span className={`import-card__source ${sourceModifier}`}>📍 {fuente}</span>
                        )}
                        <div className="import-card__grid">
                            <div><FieldLabel icon="📖" text="Título" /><p className="field-value">{obra.titulo}</p></div>
                            <div><FieldLabel icon="✍️" text="Autor"  /><p className="field-value">{obra.nombre_autor || 'N/A'}</p></div>
                            <div><FieldLabel icon="📅" text="Año"    /><p className="field-value">{obra.anio || 'N/A'}</p></div>
                            <div><FieldLabel icon="🏷️" text="Tipo"  /><p className="field-value">{obra.tipo_publicacion || 'N/A'}</p></div>
                            <div><FieldLabel icon="🆔" text="ID"     /><p className="field-value">{obra.id}</p></div>
                            {obra.enlace && (
                                <div>
                                    <FieldLabel icon="🔗" text="Enlace" />
                                    <a href={obra.enlace} target="_blank" rel="noopener noreferrer" className="import-card__link">
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

    // ── Importación en lote ─────────────────────────────────
    if (resultado.estadisticas) {
        const stats = resultado.estadisticas;
        return (
            <div className="stack">
                <div className="panel">
                    <h3 className="panel__title" style={{ marginBottom: '1.25rem' }}>Estadísticas del lote</h3>
                    <div className="stats-grid stats-grid--cols-2">
                        <div className="stat-card stat-card--muted">
                            <p className="stat-card__value stat-card__value--md">{stats.total}</p>
                            <p className="stat-card__label">Total procesadas</p>
                        </div>
                        <div className="stat-card stat-card--emerald">
                            <p className="stat-card__value stat-card__value--emerald stat-card__value--md">{stats.importadas}</p>
                            <p className="stat-card__label stat-card__label--emerald">Nuevas importadas</p>
                        </div>
                        <div className="stat-card stat-card--amber">
                            <p className="stat-card__value stat-card__value--amber stat-card__value--md">{stats.existentes}</p>
                            <p className="stat-card__label stat-card__label--amber">Ya existentes</p>
                        </div>
                        <div className="stat-card stat-card--red">
                            <p className="stat-card__value stat-card__value--red stat-card__value--md">{stats.errores}</p>
                            <p className="stat-card__label stat-card__label--red">Errores</p>
                        </div>
                    </div>
                </div>

                {resultado.resultados.importadas.length > 0 && (
                    <div>
                        <SectionHeader color="emerald" label="Nuevas Importadas" count={resultado.resultados.importadas.length} />
                        <div className="obra-list">
                            {resultado.resultados.importadas.map((obra, idx) => (
                                <div key={idx} className="obra-list__item">
                                    <span className="obra-list__dot obra-list__dot--emerald" />
                                    <span className="obra-list__title obra-list__title--medium">{obra.titulo}</span>
                                    <span className="obra-list__id">ID: {obra.id}</span>
                                    <span className="obra-list__source">📥 {obra.fuente || 'datos.bne.es'}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {resultado.resultados.existentes.length > 0 && (
                    <div>
                        <SectionHeader color="amber" label="Ya Existentes" count={resultado.resultados.existentes.length} />
                        <div className="obra-list">
                            {resultado.resultados.existentes.map((obra, idx) => (
                                <div key={idx} className="obra-list__item">
                                    <span className="obra-list__dot obra-list__dot--amber" />
                                    <span className="obra-list__title">{obra.titulo}</span>
                                    <span className="obra-list__source">📍 {obra.fuente || 'BD'}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {resultado.resultados.errores.length > 0 && (
                    <div>
                        <SectionHeader color="red" label="Errores" count={resultado.resultados.errores.length} />
                        <div className="obra-list">
                            {resultado.resultados.errores.map((error, idx) => (
                                <div key={idx} className="obra-list__item obra-list__item--top">
                                    <span className="obra-list__dot obra-list__dot--red" />
                                    <span className="obra-list__error">
                                        <span className="obra-list__error-name">{error.origen}</span>: {error.error}
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
