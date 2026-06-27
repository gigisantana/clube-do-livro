import { useEffect, useState } from "react";
import {supabase} from "./supabase.js";
import TabelaLivros from "./components/TabelaLivros"; // 1. IMPORTA O SEU COMPONENTE
import Cabecalho from "./components/Cabecalho";

export default function App() {
  const [livros, setLivros] = useState([]);
  const [livroSorteado, setLivroSorteado] = useState(null);
  
  const buscarLivrosDoBanco = async () => {
  // 1. ADICIONE ESSE LOG AQUI:
  console.log("🚀 1. A função buscarLivrosDoBanco foi disparada!");

    try {      
      const { data, error } = await supabase.from("livro").select("*");
      
      if (error) {
        console.error("❌ 2. O Supabase retornou um erro:", error.message);
        return;
      }

      console.log("🎉 3. O Supabase respondeu com sucesso! Dados:", data);
      setLivros(data || []);

    } catch (erro) {
      console.error("💥 4. Erro crítico no bloco catch:", erro.message);
    }
  };

  useEffect(() => {
  // 3. ADICIONE ESSE LOG AQUI:
    console.log("🎬 3. O useEffect rodou assim que a página nasceu!");
    buscarLivrosDoBanco();
  }, []);
  
  const lidarComSincronizacao = () => {
    buscarLivrosDoBanco();
  };

  return (
    <div className="min-h-screen bg-brand-cream text-brand-dark">
        
        {/* ================= SEÇÃO 1: CABEÇALHO ================= */}
        <Cabecalho 
        onSincronizar={lidarComSincronizacao}  />

      <main className="max-w-4xl mx-auto px-4 py-12 md:px-8 space-y-12">
        {/* ================= SEÇÃO 2: CARD DE DESTAQUE ================= */}
        {livroSorteado && (
          <section className="bg-white rounded-2xl p-6 md:p-8 border border-brand-pink/30 shadow-sm max-w-xl mx-auto text-center space-y-3">
            <span className="inline-block bg-brand-pink/10 text-brand-pink text-xs font-semibold uppercase tracking-wider px-3 py-1 rounded-full">
              🎉 Livro Sorteado do Mês!
            </span>
            <h2 className="text-3xl font-serif text-brand-dark font-medium">
              {livroSorteado.titulo}
            </h2>
            <p className="text-brand-sage font-medium">{livroSorteado.autor}</p>
            <p className="text-xs opacity-60">Sugerido por: {livroSorteado.sugerido_por}</p>
          </section>
        )}

        {/* ================= SEÇÃO 3: COMPONENTE ENCAPSULADO ================= */}
        {/* Passamos o nosso estado `livros` para dentro da propriedade `livros` da tabela */}
        {/* No Laravel seria algo como: <x-tabela-livros :livros="$livros" /> */}
        <TabelaLivros livros={livros} />

      </main>
    </div>
  );
}