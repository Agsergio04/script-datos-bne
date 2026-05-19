export default function FieldLabel({ icon, text }) {
    return (
        <p className="text-stone-400 text-xs font-semibold tracking-widest uppercase mb-0.5">
            {icon} {text}
        </p>
    );
}
