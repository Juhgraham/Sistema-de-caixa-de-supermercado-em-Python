# crud_produtos.py
import pandas as pd
from sqlalchemy.orm import joinedload
from commons.db import get_session
from commons.models import Produto
from crud_fornecedores import carregar_fornecedores_iniciais

# --- Serviços ---

def consultar_produtos():
    with get_session() as session:
        return session.query(Produto).options(joinedload(Produto.fornecedores)).order_by(Produto.id).all() 

def pesquisar_produto(produto_id: int) -> Produto | None:
    with get_session() as session:
        return session.query(Produto).filter(Produto.id == produto_id).first()


def atualizar_estoque(produto_id: int, diferenca_qtd: int) -> bool:
    try:
        with get_session() as session:
            produto = session.query(Produto).filter(Produto.id == produto_id).first()
            if not produto:
                return False
            
            produto.quantidade += diferenca_qtd
            
            if produto.quantidade < 0:
                produto.quantidade = 0
                
            session.commit()
            session.refresh(produto)
            return True
    except Exception as e:
        session.rollback()
        print(f"Erro ao atualizar estoque: {e}")
        return False


def importar_produtos_csv(caminho_csv: str = 'dados/produtos.csv'):

    carregar_fornecedores_iniciais()

    try:
        df_produtos = pd.read_csv(caminho_csv)
        
        with get_session() as session:
            # Limpa as tabelas Produto e a de associação
            session.query(Produto).delete()
            session.commit()
            
            # Insere os dados do DataFrame no banco de dados 
            produtos_para_inserir = []
            for index, row in df_produtos.iterrows():
                produto = Produto(
                    nome=row['nome'],
                    quantidade=row['quantidade'],
                    preco=row['preco']
                )
                
                produtos_para_inserir.append(produto)
            
            session.add_all(produtos_para_inserir)
            session.commit()
            print(f"{len(df_produtos)} produtos importados com sucesso de {caminho_csv}.")
            
    except FileNotFoundError:
        print(f"Aviso: Arquivo {caminho_csv} não encontrado. Produtos não importados.")
    except Exception as e:
        session.rollback()
        print(f"Erro ao importar produtos: {e}")
