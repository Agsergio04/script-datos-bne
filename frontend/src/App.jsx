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
        <div className="min-h-screen bg-stone-50">
            <header className="bg-gradient-to-br from-stone-800 via-stone-700 to-amber-900">
                <div className="max-w-4xl mx-auto px-6 py-6">
                    <div className="flex items-center gap-5">
                        <div className="text-5xl select-none leading-none">📚</div>
                        <div>
                            <h1 className="font-serif text-3xl font-bold text-white tracking-tight">
                                Recogida de Datos BNE
                            </h1>
                            <div className="w-16 h-px bg-amber-400 mt-2 mb-2" />
                            <p className="text-stone-300 text-sm tracking-wide">
                                Biblioteca Nacional de España · Archivo Digital
                            </p>
                        </div>
                    </div>

                    <nav className="flex gap-1 mt-6">
                        {PAGES.map(({ id, label }) => (
                            <button key={id} onClick={() => setPage(id)}
                                className={`px-5 py-2 rounded-t-lg text-sm font-semibold tracking-wide transition-all ${
                                    page === id
                                        ? 'bg-stone-50 text-stone-800'
                                        : 'text-stone-300 hover:text-white hover:bg-white/10'
                                }`}>
                                {label}
                            </button>
                        ))}
                    </nav>
                </div>
            </header>

            <main>
                {page === 'periodicos'
                    ? <PeriodocosPage queryParams={queryParams} />
                    : <AutoresPage />
                }
            </main>

            <footer className="max-w-4xl mx-auto px-6 mt-4 mb-8 pt-6 border-t border-stone-200 text-center">
                <p className="text-stone-400 text-sm">
                    Datos de:{' '}
                    <a href="https://datos.bne.es" target="_blank" rel="noopener noreferrer"
                        className="text-amber-600 hover:text-amber-800 hover:underline">
                        datos.bne.es
                    </a>
                </p>
                <p className="text-stone-300 text-xs mt-1">Licencia CC0 · Creative Commons Public Domain</p>
            </footer>
        </div>
    );
}
