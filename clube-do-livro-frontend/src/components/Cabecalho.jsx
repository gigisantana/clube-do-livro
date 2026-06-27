export default function Cabecalho({onSincronizar, onSortear}) {
    return (
        <header className="text-center py-2 space-y-2">
            <h1 className="text-6xl md:text-7xl font-serif text-brand-sage tracking-widest font-light">
                FORMA
            </h1>
            <p className="text-xs uppercase tracking-[0.3em] opacity-80">
                Clube Literário
            </p>
            <div className="pt-4 flex justify-center gap-4">
        <button 
          onClick={onSincronizar}
          className="bg-transparent border border-brand-sage text-brand-dark px-4 py-2 rounded-xl text-sm font-medium hover:bg-brand-sage/10 transition-colors cursor-pointer"
        >
          Sincronizar Google Doc
        </button>
        
        <button 
          onClick={onSortear}
          className="bg-brand-pink text-white px-6 py-2 rounded-xl text-sm font-medium hover:opacity-90 transition-opacity shadow-sm cursor-pointer"
        >
          Sortear Livro do Mês
        </button>
      </div>
        </header>
    );
}