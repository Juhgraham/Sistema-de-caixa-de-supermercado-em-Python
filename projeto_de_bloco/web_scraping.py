import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

URL = "https://pedrovncs.github.io/lindosprecos/produtos.html"

def realizar_web_scraping() -> pd.DataFrame | None:
    print(f"Iniciando web scraping da URL: {URL}")
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    
    produtos_html = soup.select("#produtos-lista .product-card")

    dados_produtos = []

    for produto_html in produtos_html:
        try:
            nome_tag = produto_html.find('h5', class_='card-title')
            preco_tag = produto_html.find('p', class_='card-price')
            qtd_tag   = produto_html.find('p', attrs={'data-qtd': True})

            if not (nome_tag and preco_tag and qtd_tag):
                continue

            nome = nome_tag.get_text(strip=True)
            preco_text = preco_tag.get('data-preco') or preco_tag.get_text(strip=True)
            preco_limpo = (
                preco_text
                .replace('R$', '')
                .replace('\xa0', '')
                .replace(',', '.')
                .strip()
            )
            preco = float(re.search(r'[\d\.]+', preco_limpo).group())

            
            qtd = int(qtd_tag['data-qtd'])

            dados_produtos.append({
                'nome': nome,
                'quantidade': qtd,
                'preco': preco,
            })

        except Exception as e:
            # print(f"Erro ao processar um produto: {e}")
            continue

    if not dados_produtos:
        print("Nenhum produto encontrado na página.")
        return None

    print(f"{len(dados_produtos)} produtos extraídos com sucesso.")
    return pd.DataFrame(dados_produtos)


def salvar_produtos_csv(df: pd.DataFrame, caminho: str = 'dados/produtos.csv'):
    try:
        df.to_csv(caminho, index=False)
        print(f"Produtos salvos em {caminho} com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar CSV: {e}")


if __name__ == '__main__':
    df = realizar_web_scraping()
    if df is not None:
        salvar_produtos_csv(df)
