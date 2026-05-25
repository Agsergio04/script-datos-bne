import { useState } from 'react';
import { useQueryParams } from './hooks/useQueryParams';
import AutoresPage from './pages/AutoresPage';
import PeriodocosPage from './pages/PeriodocosPage';

const PAGES = [
    { id: 'periodicos', label: '📰 Periódicos' },
    { id: 'autores',    label: '👤 Autores'    },
];

export default function App() {
    const queryParams = useQueryParams();
    const [page, setPage] = useState('periodicos');

    return (
        <div className="app">
            <header className="site-header">
                <div className="site-header__inner">
                    <div className="site-header__brand">
                        <div className="site-header__logo">📚</div>
                        <div>
                            <h1 className="site-header__title">Recogida de Datos BNE</h1>
                            <div className="site-header__rule" />
                            <p className="site-header__subtitle">
                                Biblioteca Nacional de España · Archivo Digital
                            </p>
                        </div>
                    </div>

                    <nav className="site-nav">
                        {PAGES.map(({ id, label }) => (
                            <button
                                key={id}
                                onClick={() => setPage(id)}
                                className={`site-nav__button ${page === id ? 'site-nav__button--active' : ''}`}
                            >
                                {label}
                            </button>
                        ))}
                    </nav>
                </div>
            </header>

            <main className="app__main">
                {page === 'periodicos'
                    ? <PeriodocosPage queryParams={queryParams} />
                    : <AutoresPage />
                }
            </main>

            <footer className="site-footer">
                <p className="site-footer__text">
                    Datos de:{' '}
                    <a href="https://datos.bne.es" target="_blank" rel="noopener noreferrer" className="site-footer__link">
                        datos.bne.es
                    </a>
                </p>
                <p className="site-footer__license">Licencia CC0 · Creative Commons Public Domain</p>
            </footer>
        </div>
    );
}
