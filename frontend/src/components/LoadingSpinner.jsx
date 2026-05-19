export default function LoadingSpinner({ label = 'Consultando la Biblioteca...' }) {
    return (
        <div className="flex items-center justify-center gap-3 py-6">
            <div className="w-2.5 h-2.5 bg-amber-600 rounded-full animate-bounce" />
            <div className="w-2.5 h-2.5 bg-amber-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
            <div className="w-2.5 h-2.5 bg-amber-600 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
            <span className="text-stone-500 text-sm italic ml-1">{label}</span>
        </div>
    );
}
