export default function Cabecalho({onSincronizar, onSortear}) {
    return (
        <header className="text-center py-2 space-y-2">
            <h1 className="text-6xl md:text-7xl font-serif text-brand-sage tracking-widest font-light">
                FORMA
            </h1>
            <p className="text-xs uppercase tracking-[0.3em] opacity-80">
                Clube Literário
            </p>
        </header>
    );
}