# crud_fornecedores.py
from __future__ import annotations
from pathlib import Path
import pandas as pd
from sqlalchemy.orm import Session
from commons.db import get_session
from commons.models import Fornecedor, ProdutoFornecedor


# Importando da minha planilha do excel
def carregar_fornecedores_iniciais() -> None:
    """Abre session e chama o loader de Excel."""
    with get_session() as session:
        carregar_fornecedores_iniciais_db(session)
        print("fornecedores no db =", session.query(Fornecedor).count())
        print("associacoes no db =", session.query(ProdutoFornecedor).count())

def carregar_fornecedores_iniciais_db(session: Session) -> None:
    print("-> Carregando fornecedores e associações...")

    excel_path = Path(__file__).parent / "dados" / "fornecedores.xlsx"
    
    try:
        # Limpaa associação primeiro (evita FK/ordem ruim)
        session.query(ProdutoFornecedor).delete()
        session.query(Fornecedor).delete()
        session.commit()

        # Fornecedores
        df_fornecedores = pd.read_excel(excel_path, sheet_name="fornecedores")

        COL_ID_EXCEL = "id_fornecedor" if "id_fornecedor" in df_fornecedores.columns else "id"

        excel_to_db: dict[int, int] = {}

        for _, row in df_fornecedores.iterrows():
            excel_id = int(row[COL_ID_EXCEL])
            nome = str(row["nome"]).strip()

            if not nome:
                continue

            existente = session.query(Fornecedor).filter(Fornecedor.nome == nome).first()
            if existente:
                excel_to_db[excel_id] = existente.id
                continue

            fornecedor = Fornecedor(nome=nome)
            session.add(fornecedor)
            session.flush()  # Pega fornecedor.id_fornecedor
            excel_to_db[excel_id] = fornecedor.id_fornecedor 

        session.commit()
        print(f"Concluído, {len(excel_to_db)} fornecedores inseridos na tabela.")

        # Associações Produto-Fornecedor
        df_prod_forn = pd.read_excel(excel_path, sheet_name="produto_fornecedor")

        # Remove duplicados do excel
        if "id_produto" in df_prod_forn.columns and "id_fornecedor" in df_prod_forn.columns:
            df_prod_forn = df_prod_forn.drop_duplicates(subset=["id_produto", "id_fornecedor"])

        assoc_count = 0
        puladas = 0

        for _, row in df_prod_forn.iterrows():
            id_produto = int(row["id_produto"])
            excel_id_fornecedor = int(row["id_fornecedor"])

            id_fornecedor_db = excel_to_db.get(excel_id_fornecedor)
            if not id_fornecedor_db:
                puladas += 1
                continue

            session.add(ProdutoFornecedor(id_produto=id_produto, id_fornecedor=id_fornecedor_db))
            assoc_count += 1

        session.commit()
        print(f"Concluído, {assoc_count} associações inseridas em produto_fornecedor.")
        if puladas:
            print(f"ERRO, {puladas} associações puladas porque id_fornecedor do Excel não foi encontrado no mapa.")
            print("   (confira se o id_fornecedor da aba produto_fornecedor combina com o ID da aba fornecedores)")

    except FileNotFoundError:
        print(f"Erro: Arquivo {excel_path} não encontrado.")
    except Exception as e:
        session.rollback()
        print(f"Erro ao carregar fornecedores/associações: {e}")


        # Pretendo mais pra frente poder inserir, atualizar e deletar fornecedores, por isso fiz crud_fornecedores