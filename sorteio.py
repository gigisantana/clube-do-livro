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

                    if index < len(integrantes):
                        integrante_atual = integrantes[index]
                        lista_livros.append({
                            'Sugerido por': integrante_atual,
                            'Título': titulo.strip(),
                            'Autor': autor.strip(),
                            'Status': 'Não lido'
                        })
                except Exception:
                    print(f"Erro ao processar a linha: {linha}")
                    continue
    df = pd.DataFrame(lista_livros)
    return df

if __name__ == "__main__":
    dados_clube = extrair_dados_doc()
    if dados_clube is not None: 
        dados_clube.to_csv("lista_livros.csv", index=False, encoding='utf-8-sig')