export default function BarChart({ items, color = 'amber', labelKey = 'label' }) {
    if (!items || items.length === 0) return null;

    const getValue = item => item.total ?? item.count ?? 0;
    const max = Math.max(...items.map(getValue));
    const fillModifier = color === 'blue' ? 'bar-chart__fill--blue' : '';

    return (
        <div className="bar-chart">
            {items.map((item, idx) => {
                const value = getValue(item);
                const pct = max > 0 ? Math.round((value / max) * 100) : 0;
                const label = item.nombre_autor || item.tipo || item[labelKey] || 'Desconocido';
                return (
                    <div key={idx} className="bar-chart__row">
                        <span className="bar-chart__label" title={label}>{label}</span>
                        <div className="bar-chart__track">
                            <div
                                className={`bar-chart__fill ${fillModifier}`}
                                style={{ width: `${pct}%` }}
                            />
                        </div>
                        <span className="bar-chart__value">{value}</span>
                    </div>
                );
            })}
        </div>
    );
}
