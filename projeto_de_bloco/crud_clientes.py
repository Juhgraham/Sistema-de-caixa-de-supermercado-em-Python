# crud_clientes.py
from __future__ import annotations

import pandas as pd
from sqlalchemy.exc import IntegrityError

from commons.db import get_session
from commons.models import Cliente


def carregar_clientes_iniciais(caminho_json: str = "dados/clientes.json") -> None: #atualizei aqui
    """Carrega clientes do JSON se a tabela estiver vazia."""
    try:
        df_clientes = pd.read_json(caminho_json)

        with get_session() as session:
            if session.query(Cliente).count() == 0:
                df_clientes.to_sql(
                    Cliente.__tablename__,
                    session.bind,
                    if_exists="append",
                    index=False
                )
                session.commit()
                print(f"{len(df_clientes)} clientes iniciais carregados com sucesso.")
            else:
                print("Clientes iniciais já carregados.")

    except FileNotFoundError:
        print(f"Aviso: Arquivo {caminho_json} não encontrado. Nenhum cliente inicial carregado.")
    except Exception as e:
        print(f"Erro ao carregar clientes iniciais: {e}")


def consultar_clientes() -> list[Cliente]:
    """Lista todos os clientes."""
    with get_session() as session:
        return session.query(Cliente).order_by(Cliente.id).all()


def buscar_cliente(cliente_id: int) -> Cliente | None:
    """Busca cliente por id."""
    with get_session() as session:
        return session.query(Cliente).filter(Cliente.id == cliente_id).first()


def cadastrar_cliente(nome: str) -> Cliente | None:
    """Cadastra um novo cliente. Se o nome tiverr vazio, cria 'Cliente X'."""
    nome = (nome or "").strip()

    with get_session() as session:
        try:
            if not nome:
                ultimo_id = session.query(Cliente.id).order_by(Cliente.id.desc()).first()
                proximo_id = (ultimo_id[0] + 1) if ultimo_id else 1
                nome = f"Cliente {proximo_id}"

            cliente = Cliente(nome=nome)
            session.add(cliente)
            session.commit()
            session.refresh(cliente)
            print(f"Cliente '{cliente.nome}' cadastrado com ID {cliente.id}.")
            return cliente

        except IntegrityError:
            session.rollback()
            print("Erro: Cliente com este nome já existe.")
            return None
        except Exception as e:
            session.rollback()
            print(f"Erro ao cadastrar cliente: {e}")
            return None


def atualizar_cliente(cliente_id: int, novo_nome: str) -> bool:
    """Atualiza o nome do cliente."""
    novo_nome = (novo_nome or "").strip()
    if not novo_nome:
        print("Nome inválido.")
        return False

    with get_session() as session:
        try:
            cliente = session.get(Cliente, cliente_id)
            if not cliente:
                return False

            cliente.nome = novo_nome
            session.commit()
            return True

        except IntegrityError:
            session.rollback()
            print("Erro: já existe um cliente com esse nome.")
            return False
        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar cliente: {e}")
            return False


def deletar_cliente(cliente_id: int) -> bool:
    """
    Remove um cliente.
    Observação: se houver vendas vinculadas, pode falhar por FK (depende do seu schema).
    """
    with get_session() as session:
        try:
            cliente = session.get(Cliente, cliente_id)
            if not cliente:
                return False

            session.delete(cliente)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erro ao deletar cliente: {e}")
            return False
