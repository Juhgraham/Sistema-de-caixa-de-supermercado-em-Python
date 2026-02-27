# sig/clientes_menu.py
from sqlalchemy import func, desc
from sqlalchemy.orm import joinedload
from tabulate import tabulate

from commons.db import get_session
from commons.models import Cliente, Venda, ItemVenda
from commons.utils import entrar_inteiro

from crud_clientes import (
    cadastrar_cliente,
    consultar_clientes,
    atualizar_cliente,
    deletar_cliente,
)

def _nota_fiscal(venda: Venda):
    print("\n" + "=" * 50)
    print("          SUPERMERCADO - NOTA FISCAL")
    print("=" * 50)
    print(f"Venda: {venda.id}")
    print(f"Data: {venda.data_hora.strftime('%d/%m/%Y %H:%M')}")
    print(f"Cliente: {venda.cliente.nome} (ID {venda.cliente.id})")
    print("-" * 50)

    tabela = []
    total = 0.0

    for it in venda.itens:
        subtotal = float(it.quantidade) * float(it.preco_unitario)
        total += subtotal

        nome_prod = (
            it.produto.nome if getattr(it, "produto", None)
            else f"ID {it.id_produto}"
        )

        tabela.append([
            nome_prod,
            it.quantidade,
            f"R$ {it.preco_unitario:.2f}",
            f"R$ {subtotal:.2f}"
        ])

    print(tabulate(
        tabela,
        headers=["Produto", "Qtd", "Preço Unit.", "Subtotal"],
        tablefmt="fancy_grid",
        colalign=("left", "center", "right", "right")
    ))

    print(f"\nTOTAL: R$ {total:.2f}")
    print("=" * 50)


# ---------- Relatórios do enunciado ----------

def listar_clientes_com_compras():
    with get_session() as session:
        rows = (
            session.query(
                Cliente.id,
                Cliente.nome,
                func.count(Venda.id).label("num_compras")
            )
            .join(Venda, Venda.id_cliente == Cliente.id)
            .group_by(Cliente.id, Cliente.nome)
            .order_by(Cliente.id)
            .all()
        )

    if not rows:
        print("Nenhum cliente possui compras registradas.")
        return

    print("\n--- Clientes com compras registradas ---")

    tabela = [
        [cid, nome, ncompras]
        for cid, nome, ncompras in rows
    ]

    print(tabulate(
        tabela,
        headers=["ID", "Cliente", "Nº de Compras"],
        tablefmt="fancy_grid",
        colalign=("center", "left", "center")
    ))


def clientes_com_compras_consultar_cliente():

    listar_clientes_com_compras()

    id_cliente = entrar_inteiro("ID do cliente: ", min_val=1)

    with get_session() as session:
        cliente = session.get(Cliente, id_cliente)
        if not cliente:
            print("Cliente não encontrado.")
            return

        vendas = (
            session.query(Venda)
            .options(
                joinedload(Venda.cliente),
                joinedload(Venda.itens).joinedload(ItemVenda.produto),
            )
            .filter(Venda.id_cliente == id_cliente)
            .order_by(Venda.data_hora.desc())
            .all()
        )

        if not vendas:
            print(f"O cliente {cliente.nome} não possui compras registradas.")
            return

        print(f"\nCompras de {cliente.nome} (mais recentes primeiro):")
        tabela = []
        for v in vendas:
            total_v = sum(float(it.quantidade) * float(it.preco_unitario) for it in v.itens)
            tabela.append([
                v.id,
                v.data_hora.strftime('%d/%m/%Y %H:%M'),
                f"R$ {total_v:.2f}"
            ])

        print(tabulate(
            tabela,
            headers=["ID da Venda", "Data/Hora", "Total"],
            tablefmt="fancy_grid",
            colalign=("center", "center", "right")
        ))

        id_venda = entrar_inteiro("\nDigite o ID da venda para ver a nota fiscal (0 pra voltar): ", min_val=0)
        if id_venda == 0:
            return

        venda = next((x for x in vendas if x.id == id_venda), None)
        if not venda:
            print("Venda não encontrada para este cliente.")
            return

        _nota_fiscal(venda)


def clientes_sem_compras():
    with get_session() as session:
        rows = (
            session.query(Cliente)
            .outerjoin(Venda, Venda.id_cliente == Cliente.id)
            .filter(Venda.id.is_(None))
            .order_by(Cliente.id)
            .all()
        )

    if not rows:
        print("Nenhum cliente sem compras.")
        return

    print("\n--- Clientes sem compras ---\n")
    tabela = [[c.id, c.nome] for c in rows]

    print(tabulate(
        tabela,
        headers=["ID", "Nome"],
        tablefmt="fancy_grid",
        colalign=("center", "left")
    ))


def top_clientes_por_numero_compras(top_n: int = 5):
    with get_session() as session:
        rows = (
            session.query(
                Cliente.id,
                Cliente.nome,
                func.count(func.distinct(Venda.id)).label("num_compras"),
            )
            .join(Venda, Venda.id_cliente == Cliente.id)
            .group_by(Cliente.id, Cliente.nome)
            .order_by(desc("num_compras"))
            .limit(top_n)
            .all()
        )

    if not rows:
        print("Ainda não há compras registradas.")
        return

    print(f"\n--- Top {top_n} clientes que mais compram ---")
    tabela = [[cid, nome, ncompras] for cid, nome, ncompras in rows]

    print(tabulate(
        tabela,
        headers=["ID", "Cliente", "Nº de Compras"],
        tablefmt="fancy_grid",
        colalign=("center", "left", "center")
    ))


def top_clientes_por_total_gasto(top_n: int = 5):
    with get_session() as session:
        total_expr = func.sum(ItemVenda.quantidade * ItemVenda.preco_unitario)

        rows = (
            session.query(
                Cliente.id,
                Cliente.nome,
                func.coalesce(total_expr, 0).label("total_gasto"),
            )
            .join(Venda, Venda.id_cliente == Cliente.id)
            .join(ItemVenda, ItemVenda.id_venda == Venda.id)
            .group_by(Cliente.id, Cliente.nome)
            .order_by(desc("total_gasto"))
            .limit(top_n)
            .all()
        )

    if not rows:
        print("Ainda não há compras registradas.")
        return

    print(f"\n--- Top {top_n} clientes que mais gastam ---")
    tabela = [
        [cid, nome, f"R$ {float(total):.2f}"]
        for cid, nome, total in rows
    ]

    print(tabulate(
        tabela,
        headers=["ID", "Cliente", "Total Gasto"],
        tablefmt="fancy_grid",
        colalign=("center", "left", "right")
    ))


# ---------- Crud ----------

def crud_listar_clientes():
    clientes = consultar_clientes()
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return
    print("\n--- Clientes ---")
    tabela = [[c.id, c.nome] for c in clientes]

    print(tabulate(
        tabela,
        headers=["ID", "Nome"],
        tablefmt="fancy_grid",
        colalign=("center", "left")
    ))


def crud_cadastrar_cliente():
    nome = input("Nome do cliente (ENTER para gerar automático): ").strip()
    cliente = cadastrar_cliente(nome)
    if not cliente:
        print("Falha ao cadastrar cliente.")


def crud_atualizar_cliente():
    cid = entrar_inteiro("\nID do cliente: ", min_val=1)
    novo_nome = input("\nNovo nome: ").strip()
    ok = atualizar_cliente(cid, novo_nome)
    print("\nCliente atualizado." if ok else "\nNão foi possível atualizar (ID inválido ou nome duplicado).")


def crud_excluir_cliente():
    cid = entrar_inteiro("ID do cliente: ", min_val=1)

    # trava simples: não permite deletar se tiver compras
    with get_session() as session:
        existe_venda = session.query(Venda.id).filter(Venda.id_cliente == cid).first() is not None
    if existe_venda:
        print("Não é possível excluir: cliente possui compras registradas.")
        return

    ok = deletar_cliente(cid)
    print("\nCliente removido." if ok else "\nCliente não encontrado.")


def menu_clientes():
    while True:
        print("\n=== SIG > CLIENTES ===")
        print("1 - Cadastrar cliente")
        print("2 - Listar clientes")
        print("3 - Atualizar cliente")
        print("4 - Excluir cliente")
        print("5 - Consultas")
        print("6 - Voltar")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            crud_cadastrar_cliente()

        elif opcao == "2":
            crud_listar_clientes()

        elif opcao == "3":
            crud_atualizar_cliente()

        elif opcao == "4":
            crud_excluir_cliente()

        elif opcao == "5":
            # ============================
            # SUBMENU DE CONSULTAS
            # ============================
            while True:
                print("\n--- CLIENTES > CONSULTAS ---")
                print("1 - Clientes com compras (consultar + nota fiscal)")
                print("2 - Clientes sem compras")
                print("3 - Top clientes (mais compram)")
                print("4 - Top clientes (mais gastam)")
                print("5 - Voltar")

                op2 = input("Escolha: ").strip()

                if op2 == "1":
                    clientes_com_compras_consultar_cliente()

                elif op2 == "2":
                    clientes_sem_compras()

                elif op2 == "3":
                    n = entrar_inteiro("Top N (ex: 5): ", min_val=1)
                    top_clientes_por_numero_compras(n)

                elif op2 == "4":
                    n = entrar_inteiro("Top N (ex: 5): ", min_val=1)
                    top_clientes_por_total_gasto(n)

                elif op2 == "5":
                    break

                else:
                    print("Opção inválida.")

        elif opcao == "6":
            break

        else:
            print("Opção inválida.")

