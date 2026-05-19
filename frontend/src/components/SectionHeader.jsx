const palette = {
    stone:   'bg-stone-400 text-stone-700',
    emerald: 'bg-emerald-500 text-emerald-700',
    amber:   'bg-amber-400 text-amber-700',
    red:     'bg-red-400 text-red-700',
    blue:    'bg-blue-400 text-blue-700',
};

export default function SectionHeader({ color, label, count }) {
    const [bg, text] = palette[color].split(' ');
    return (
        <h4 className={`font-serif font-bold ${text} mb-3 flex items-center gap-2`}>
            <span className={`w-1.5 h-4 ${bg} rounded-full`} />
            {label} {count !== undefined && `(${count})`}
        </h4>
    );
}
