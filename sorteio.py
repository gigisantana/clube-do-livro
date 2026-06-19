import re
import random
import pandas as pd
import requests
from bs4 import BeautifulSoup

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
                        if livro['Título'] == titulo_limpo:
                            livro_duplicado = livro
                            break
                    
                    if livro_duplicado is None:
                            lista_livros.append({
                                'Sugerido por': integrante_atual,
                                'Título': titulo_limpo,
                                'Autor': autor_limpo,
                                'Status': 'Não lido',
                                'Peso': 1
                            })
                    else:
                        # soma 1 ao peso do livro se ele já estiver em alguma lista
                        livro_duplicado['Peso'] += 1
                        # adiciona o nome das integrantes que sugeriram o mesmo livro
                        livro_duplicado['Sugerido por'] += f", {integrante_atual}"
                            
                except Exception:
                    print(f"Erro ao processar a linha: {linha}")
                    continue
    df = pd.DataFrame(lista_livros)
    return df

def sortear_livro(df):
    if df.empty:
        print("A lista de livros está vazia. Não é possível realizar o sorteio.")
        return None
    
    livros_nao_lidos = df[df['Status'] == 'Não lido']
    if livros_nao_lidos.empty:
        print("Não há livros não lidos para sortear.")
        return None
    
    lista_indices = livros_nao_lidos.index.tolist()
    lista_pesos = livros_nao_lidos['Peso'].tolist()

    sorteio = random.choices(lista_indices, weights=lista_pesos, k=1)
    linha_sorteada = livros_nao_lidos.loc[sorteio[0]]
    titulo = linha_sorteada['Título']
    autor = linha_sorteada['Autor']
    sugerido_por = linha_sorteada['Sugerido por']
    return (f"{titulo} - {autor} (sugerido por {sugerido_por})", sorteio[0])

def atualizar_status(df, indice, novo_status):
    if indice in df.index:
        df.at[indice, 'Status'] = novo_status
        print(f"Status do livro na linha {indice} atualizado para '{novo_status}'.")
    else:
        print(f"Livro não encontrado na lista.")

if __name__ == "__main__":
    dados_clube = extrair_dados_doc()
    if dados_clube is not None: 
        dados_clube.to_csv("lista_livros.csv", index=False, encoding='utf-8-sig')
        
        livro_sorteado, indice_sorteado = sortear_livro(dados_clube)
        print(f"O livro sorteado é: {livro_sorteado}")
        atualizar_status(dados_clube, indice_sorteado, "Lido")