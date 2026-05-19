export default function BarChart({ items, colorClass = 'bg-amber-500', labelKey = 'label' }) {
    if (!items || items.length === 0) return null;

    const getValue = item => item.total ?? item.count ?? 0;
    const max = Math.max(...items.map(getValue));

    return (
        <div className="space-y-2.5">
            {items.map((item, idx) => {
                const value = getValue(item);
                const pct = max > 0 ? Math.round((value / max) * 100) : 0;
                const label = item.nombre_autor || item.tipo || item[labelKey] || 'Desconocido';
                return (
                    <div key={idx} className="flex items-center gap-3">
                        <span className="text-stone-600 text-xs w-28 truncate flex-shrink-0" title={label}>
                            {label}
                        </span>
                        <div className="flex-1 bg-stone-100 rounded-full h-2.5 overflow-hidden">
                            <div
                                className={`h-full ${colorClass} rounded-full transition-all duration-700`}
                                style={{ width: `${pct}%` }}
                            />
                        </div>
                        <span className="text-stone-500 text-xs w-6 text-right flex-shrink-0">{value}</span>
                    </div>
                );
            })}
        </div>
    );
}
