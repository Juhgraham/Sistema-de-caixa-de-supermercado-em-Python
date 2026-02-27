# crud_vendas.py
from commons.db import get_session
from commons.models import Venda, ItemVenda, Cliente, Produto
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

# Serviços da venda

def registrar_venda(cliente: Cliente, itens_comprados: list[dict]) -> Venda | None:
    """
    Registra uma nova venda e seus itens no banco de dados.
    itens_comprados é uma lista de dicionários com 'id_produto', 'quantidade', 'preco'.
    """
    if not itens_comprados:
        return None

    try:
        with get_session() as session:
            # Cria a Venda
            nova_venda = Venda(
                id_cliente=cliente.id,
                data_hora=datetime.now()
            )
            session.add(nova_venda)
            session.flush() # Pega o id da venda antes do commit

            # Cria os ItensVenda (detalhes)
            itens_venda_obj = []
            for item in itens_comprados:
                item_venda = ItemVenda(
                    id_venda=nova_venda.id,
                    id_produto=item['id_produto'],
                    quantidade=item['quantidade'],
                    preco_unitario=item['preco']
                )
                itens_venda_obj.append(item_venda)
            
            session.add_all(itens_venda_obj)
            session.commit()
            session.refresh(nova_venda)
            return nova_venda
            
    except IntegrityError as e:
        session.rollback()
        print(f"Erro de integridade ao registrar venda: {e}")
        return None
    except Exception as e:
        session.rollback()
        print(f"Erro ao registrar venda: {e}")
        return None

def consultar_vendas() -> list[Venda]:
    with get_session() as session:
        return (
            session.query(Venda)
            .options(
                joinedload(Venda.cliente),
                joinedload(Venda.itens).joinedload(ItemVenda.produto),
            )
            .order_by(Venda.data_hora.desc())
            .all()
        )