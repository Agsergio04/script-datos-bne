export default function EmptyState({ icon, title, description }) {
    return (
        <div className="empty-state">
            <div className="empty-state__icon">{icon}</div>
            <p className="empty-state__title">{title}</p>
            {description && <p className="empty-state__description">{description}</p>}
        </div>
    );
}
