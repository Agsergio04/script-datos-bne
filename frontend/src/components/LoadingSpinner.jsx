export default function LoadingSpinner({ label = 'Consultando la Biblioteca...' }) {
    return (
        <div className="loading-spinner">
            <div className="loading-spinner__dot" />
            <div className="loading-spinner__dot loading-spinner__dot--2" />
            <div className="loading-spinner__dot loading-spinner__dot--3" />
            <span className="loading-spinner__label">{label}</span>
        </div>
    );
}
