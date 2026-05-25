export default function SectionHeader({ color = 'stone', label, count }) {
    return (
        <h4 className={`section-header section-header--${color}`}>
            <span className="section-header__bar" />
            {label} {count !== undefined && `(${count})`}
        </h4>
    );
}
