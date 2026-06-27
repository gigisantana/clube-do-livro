
export default function TabelaLivros({ livros }) {
  return (
    <section className="bg-white rounded-2xl p-6 border border-black/5 shadow-sm space-y-4">
      <div className="flex justify-between items-center border-b border-brand-cream pb-4">
        <h3 className="font-serif text-xl font-medium">Sugestões para Sorteio</h3>
        <span className="text-xs bg-brand-sage/20 text-brand-dark px-2.5 py-1 rounded-md font-medium">
          {livros.length} livros na esteira
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="text-xs uppercase tracking-wider opacity-60 border-b border-brand-cream">
              <th className="pb-3 font-medium">Título / Autor</th>
              <th className="pb-3 font-medium">Sugerido Por</th>
              <th className="pb-3 font-medium text-center">Peso</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-brand-cream/50 text-sm">
            {livros.map((livro) => (
              <tr key={livro.id} className="hover:bg-brand-cream/30 transition-colors">
                <td className="py-4 pr-4">
                  <div className="font-medium text-base text-brand-dark">{livro.titulo}</div>
                  <div className="text-xs text-brand-sage mt-0.5">{livro.autor}</div>
                </td>
                <td className="py-4 opacity-80">{livro.sugerido_por}</td>
                <td className="py-4 text-center font-mono">
                  <span className="bg-brand-cream px-2 py-1 rounded text-xs font-bold">
                    {livro.peso}x
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}