export default function ListaObras({ obras, dotColor, showLink = false }) {
    return (
        <div className="bg-white border border-stone-200 rounded-xl overflow-hidden">
            {obras.map((obra, idx) => (
                <div
                    key={idx}
                    className={`flex items-center gap-3 px-5 py-3 text-sm ${idx < obras.length - 1 ? 'border-b border-stone-100' : ''}`}
                >
                    <span className={`w-1.5 h-1.5 ${dotColor} rounded-full flex-shrink-0`} />
                    <span className="text-stone-800 font-medium flex-1">{obra.titulo}</span>
                    <span className="text-stone-400 text-xs">ID: {obra.id}</span>
                    {showLink && obra.enlace && (
                        <a href={obra.enlace} target="_blank" rel="noopener noreferrer"
                            className="text-xs text-amber-600 hover:text-amber-800 hover:underline">
                            BNE ↗
                        </a>
                    )}
                </div>
            ))}
        </div>
    );
}
