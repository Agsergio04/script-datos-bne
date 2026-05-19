export default function EmptyState({ icon, title, description }) {
    return (
        <div className="text-center py-12 bg-white border border-stone-200 rounded-xl">
            <div className="text-5xl mb-3">{icon}</div>
            <p className="text-stone-600 font-medium">{title}</p>
            {description && <p className="text-stone-400 text-sm mt-1">{description}</p>}
        </div>
    );
}
