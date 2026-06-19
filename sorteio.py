import re
import random
import pandas as pd
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client

SUPABASE_URL = "https://verblizvjotairyleqtw.supabase.co"
SUPABASE_KEY = "sb_publishable__wdMzDQPgL7QFVEdU4T3zg_7VBUIxVy"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

URL_DOCS = "https://docs.google.com/document/d/e/2PACX-1vSi86kbA0bT2Ham0UvmwCJCi8itcHuFXH71Soqko2PpUYtAHJ87YnlF597--rPeOc07RxDjLuIFGXk_/pub"

def extrair_dados_doc():
    resposta = requests.get(URL_DOCS)

    # teste de acesso ao documento, 200 é o código de sucesso
    if resposta.status_code != 200:
        print("Erro ao acessar o documento. Status code:", resposta.status_code)
        return None
    
    soup = BeautifulSoup(resposta.content, 'html.parser')
    
    tabela = soup.find('table')
    if not tabela:
        print("Não foi possível encontrar a tabela no documento.")
        return None

    linhas_tabela = tabela.find_all('tr')

    cabecalho = linhas_tabela[0]
    integrantes = [celula.get_text(strip=True) for celula in cabecalho.find_all('td')]
    
    lista_livros = []

    for linha in linhas_tabela[1:]:  # ignora a linha do cabeçalho
        celulas = linha.find_all('td')

        for index, celula in enumerate(celulas):
            texto_celula = celula.get_text(strip=True)
            # limpa travessões longos e médios, deixando apenas o hífen simples
            texto_celula = texto_celula.replace("—", "-").replace("–", "-")

            # se a linha não tem hífen, é o nome da integrante (cabeçalho)
            if texto_celula and "-" in texto_celula:
                # se tem hífen, será separado em título e autor
                try:
                    titulo, autor = texto_celula.split("-", 1)
                    titulo_limpo = titulo.strip()
                    autor_limpo = autor.strip()
                    integrante_atual = integrantes[index]
                    # variável para verificar se o livro já foi sugerido por outra integrante
                    livro_duplicado = None

                    for livro in lista_livros:
                        if livro['titulo'].lower() == titulo_limpo.lower():
                            livro_duplicado = livro
                            break
                    
                    if livro_duplicado is None:
                            lista_livros.append({
                            'sugerido_por': integrante_atual,
                            'titulo': titulo_limpo,
                            'autor': autor_limpo,
                            'status': 'Não lido',
                            'peso': 1
                        })
                    else:
                        # soma 1 ao peso do livro se ele já estiver em alguma lista
                        livro_duplicado['peso'] += 1
                        # adiciona o nome das integrantes que sugeriram o mesmo livro
                        livro_duplicado['sugerido_por'] += f", {integrante_atual}"

                        if len(autor_limpo) > len(livro_duplicado['autor']):
                            livro_duplicado['autor'] = autor_limpo


                except Exception:
                    print(f"Erro ao processar a linha: {linha}")
                    continue
    df = pd.DataFrame(lista_livros)
    return df

def sortear_livro(df):
    if df.empty:
        print("A lista de livros está vazia. Não é possível realizar o sorteio.")
        return None
    
    lista_indices = df.index.tolist()
    lista_pesos = df['peso'].tolist()

    sorteio = random.choices(lista_indices, weights=lista_pesos, k=1)
    linha_sorteada = df.loc[sorteio[0]]
    
    return linha_sorteada['titulo'], linha_sorteada['id']

def atualizar_status(idlivro, novo_status = "Lido"):
    try:
        supabase.table('livro').update({'status': novo_status}).eq('id', int(idlivro)).execute()
    except Exception as e:
        print(f"Erro ao atualizar status do livro: {e}")

def sincronizar_supabase(df):
    df_pra_supabase = df.drop(columns=['status'], errors='ignore')
    # transforma o df em uma lista de dicionários, e cada dicionário representa um livro
    livros_prontos = df_pra_supabase.to_dict(orient='records')
    # usa a coluna de titulo pra evitar duplicidade, apenas atualizando o existente
    supabase.table('livro').upsert(livros_prontos, on_conflict=['titulo']).execute()


if __name__ == "__main__":
    dados_clube = extrair_dados_doc()
    if dados_clube is not None:
        sincronizar_supabase(dados_clube) 
        resposta = supabase.table('livro').select('*').eq('status', 'Não lido').execute()
        df_atualizado = pd.DataFrame(resposta.data)
        
        livro_sorteado, indice_sorteado = sortear_livro(df_atualizado)
        print(f"O livro sorteado é: {livro_sorteado}")
        atualizar_status(indice_sorteado, "Lido")