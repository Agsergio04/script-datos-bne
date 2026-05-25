export default function ListaObras({ obras, dotColor = '', showLink = false }) {
    return (
        <div className="obra-list">
            {obras.map((obra, idx) => (
                <div key={idx} className="obra-list__item">
                    <span className={`obra-list__dot ${dotColor}`} />
                    <span className="obra-list__title obra-list__title--medium">{obra.titulo}</span>
                    <span className="obra-list__id">ID: {obra.id}</span>
                    {showLink && obra.enlace && (
                        <a href={obra.enlace} target="_blank" rel="noopener noreferrer" className="obra-list__link">
                            BNE ↗
                        </a>
                    )}
                </div>
            ))}
        </div>
    );
}
