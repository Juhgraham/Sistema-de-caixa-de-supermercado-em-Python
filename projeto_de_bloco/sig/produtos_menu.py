# sig/produtos_menu.py
from sqlalchemy import func, asc, desc
from tabulate import tabulate
from commons.db import get_session
from commons.models import Produto, Fornecedor, ProdutoFornecedor
from commons.utils import entrar_inteiro, entrar_float


def _listar_fornecedores(session):
    fornecedores = session.query(Fornecedor).order_by(Fornecedor.id_fornecedor).all()
    if not fornecedores:
        print("Nenhum fornecedor cadastrado.")
        return []
    print("\nFornecedores:\n")
    for f in fornecedores:
        print(f"- {f.id_fornecedor} | {f.nome}")
    return fornecedores


def _selecionar_ids_fornecedores(session) -> list[int]:
    _listar_fornecedores(session)
    texto = input("\nInforme IDs de fornecedores (separados por vírgula) ou ENTER p/ nenhum: ").strip()
    if not texto:
        return []

    ids = []
    for parte in texto.split(","):
        parte = parte.strip()
        if not parte:
            continue
        if not parte.isdigit():
            print(f"ID inválido: {parte}")
            continue
        ids.append(int(parte))

    # valida existência
    validos = set(r[0] for r in session.query(Fornecedor.id_fornecedor).filter(Fornecedor.id_fornecedor.in_(ids)).all())
    ids_ok = [i for i in ids if i in validos]
    if len(ids_ok) != len(set(ids)):
        print("Alguns IDs não existem e foram ignorados.")
    return sorted(set(ids_ok))


def _mapa_fornecedores_por_produto(session) -> dict[int, list[str]]:
    forn_por_id = {f.id_fornecedor: f.nome for f in session.query(Fornecedor).all()}
    assoc = session.query(ProdutoFornecedor).all()

    m: dict[int, list[str]] = {}
    for a in assoc:
        m.setdefault(a.id_produto, []).append(forn_por_id.get(a.id_fornecedor, f"ID {a.id_fornecedor}"))

    for k in list(m.keys()):
        m[k] = sorted(set(m[k]))
    return m


def cadastrar_produto():
    nome = input("Nome do produto: ").strip()
    qtd = entrar_inteiro("Quantidade: ", min_val=0)
    preco = entrar_float("Preço: ", min_val=0.0)

    with get_session() as session:
        ids_forn = _selecionar_ids_fornecedores(session)

        produto = Produto(nome=nome, quantidade=qtd, preco=preco)
        session.add(produto)
        session.flush()  # pega produto.id

        # associa (se não escolher nenhum, deixa sem associação)
        for fid in ids_forn:
            session.add(ProdutoFornecedor(id_produto=produto.id, id_fornecedor=fid))

        session.commit()
        print(f"\nProduto cadastrado com ID {produto.id}.")


def listar_produtos():
    with get_session() as session:
        produtos = session.query(Produto).order_by(Produto.id).all()
        if not produtos:
            print("Nenhum produto cadastrado.")
            return

        mapa = _mapa_fornecedores_por_produto(session)

        tabela = []
        for p in produtos:
            fornecedores = ", ".join(mapa.get(p.id, [])) or "N/A"
            tabela.append([
                p.id,
                p.nome,
                p.quantidade,
                f"R$ {p.preco:.2f}",
                fornecedores
            ])

    print("\n--- Lista de Produtos ---")
    print(
        tabulate(
            tabela,
            headers=["ID", "Nome", "Qtd", "Preço", "Fornecedor(es)"],
            tablefmt="fancy_grid"
        )
    )


def atualizar_produto():
    pid = entrar_inteiro("ID do produto: ", min_val=1)
    with get_session() as session:
        produto = session.get(Produto, pid)
        if not produto:
            print("Produto não encontrado.")
            return

        print(f"Atual: nome={produto.nome}, qtd={produto.quantidade}, preco={produto.preco:.2f}")
        novo_nome = input("Novo nome (ENTER mantém): ").strip()
        if novo_nome:
            produto.nome = novo_nome

        qtd = input("Nova quantidade (ENTER mantém): ").strip()
        if qtd:
            if not qtd.isdigit():
                print("Quantidade inválida.")
                return
            produto.quantidade = max(0, int(qtd))

        pr = input("Novo preço (ENTER mantém): ").strip()
        if pr:
            try:
                produto.preco = max(0.0, float(pr))
            except ValueError:
                print("Preço inválido.")
                return

        print("\nAtualizar fornecedores do produto?")
        print("1 - Manter como está")
        print("2 - Substituir lista de fornecedores")
        op = input("Escolha: ").strip()

        if op == "2":
            ids_novos = _selecionar_ids_fornecedores(session)
            # apaga vínculos atuais
            session.query(ProdutoFornecedor).filter(ProdutoFornecedor.id_produto == pid).delete()
            # cria novos
            for fid in ids_novos:
                session.add(ProdutoFornecedor(id_produto=pid, id_fornecedor=fid))

        session.commit()
        print("Produto atualizado.")


def excluir_produto():
    pid = entrar_inteiro("\nID do produto: ", min_val=1)

    with get_session() as session:
        produto = session.get(Produto, pid)
        if not produto:
            print("Produto não encontrado.")
            return

        # venda existe?
        from commons.models import ItemVenda  # importar aqui para evitar circular
        existe_venda = session.query(ItemVenda.id).filter(ItemVenda.id_produto == pid).first() is not None

        if existe_venda:
            print("Não é possível excluir: produto possui vendas registradas.")
            return

        # Se não tem venda eu posso excluir
        session.query(ProdutoFornecedor).filter(ProdutoFornecedor.id_produto == pid).delete()
        session.delete(produto)
        session.commit()

        print("\nProduto removido com sucesso.")



def consultar_mais_menos_vendidos():
    n = entrar_inteiro("Top N: ", min_val=1)
    with get_session() as session:
        # soma de quantidades vendidas por produto (inclui produtos 0 vendas)
        from commons.models import ItemVenda  # evita import circular

        qtd_expr = func.coalesce(func.sum(ItemVenda.quantidade), 0)

        base = (
            session.query(Produto.id, Produto.nome, qtd_expr.label("qtd_vendida"))
            .outerjoin(ItemVenda, ItemVenda.id_produto == Produto.id)
            .group_by(Produto.id, Produto.nome)
        )

        # mais vendidos
        mais = base.order_by(desc("qtd_vendida")).limit(n).all() #atualizei aqui
        tabela_mais = [
            [pid, nome, int(qtd)]
            for pid, nome, qtd in mais
        ]

        print(f"\n--- Top {n} Produtos MAIS Vendidos ---")
        print(tabulate(
            tabela_mais,
            headers=["ID", "Produto", "Quantidade Vendida"],
            tablefmt="fancy_grid"
        ))

        # menos vendidos
        menos = base.order_by(asc("qtd_vendida"), asc(Produto.id)).limit(n).all()
        tabela_menos = [
            [pid, nome, int(qtd)]
            for pid, nome, qtd in menos
        ]

        print(f"\n--- Top {n} Produtos MENOS Vendidos ---")
        print(tabulate(
            tabela_menos,
            headers=["ID", "Produto", "Quantidade Vendida"],
            tablefmt="fancy_grid"
        ))


def consultar_pouco_estoque():
    limite = entrar_inteiro("Considerar 'pouco estoque' abaixo de: ", min_val=0)
    with get_session() as session:
        produtos = (
            session.query(Produto)
            .filter(Produto.quantidade <= limite)
            .order_by(Produto.quantidade.asc(), Produto.id.asc())
            .all()
        )

    if not produtos:
        print("Nenhum produto com pouco estoque nesse limite.") #atualizei aqui
        return

    tabela = [
        [p.id, p.nome, p.quantidade]
        for p in produtos
    ]

    print("\n--- Produtos com pouco estoque ---")
    print(tabulate(
        tabela,
        headers=["ID", "Produto", "Estoque"],
        tablefmt="fancy_grid"
    ))


def fornecedores_de_um_produto():
    pid = entrar_inteiro("ID do produto: ", min_val=1)
    with get_session() as session:
        produto = session.get(Produto, pid)
        if not produto:
            print("Produto não encontrado.")
            return

        rows = (
            session.query(Fornecedor.id_fornecedor, Fornecedor.nome)
            .join(ProdutoFornecedor, ProdutoFornecedor.id_fornecedor == Fornecedor.id_fornecedor)
            .filter(ProdutoFornecedor.id_produto == pid)
            .order_by(Fornecedor.id_fornecedor)
            .all()
        )

    print(f"\nFornecedor(es) do produto {produto.nome} (ID {produto.id}):")
    if not rows:
        print("N/A (nenhum associado)")
        return
    tabela = [[fid, nome] for fid, nome in rows] #atualizei aqui

    print(
        tabulate(
            tabela,
            headers=["ID Fornecedor", "Nome"],
            tablefmt="fancy_grid"
        )
    )


def menu_produtos():
    while True:
        print("\n=== SIG > PRODUTOS ===")
        print("1 - Cadastrar produto")
        print("2 - Listar produtos")
        print("3 - Atualizar produto")
        print("4 - Excluir produto")
        print("5 - Consultas")
        print("6 - Voltar")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            atualizar_produto()
        elif opcao == "4":
            excluir_produto()
        elif opcao == "5":
            while True:
                print("\n--- PRODUTOS > CONSULTAS ---")
                print("1 - Produtos mais/menos vendidos")
                print("2 - Produtos com pouco estoque (limite)")
                print("3 - Fornecedores de um produto")
                print("4 - Voltar")
                op2 = input("Escolha: ").strip()

                if op2 == "1":
                    consultar_mais_menos_vendidos()
                elif op2 == "2":
                    consultar_pouco_estoque()
                elif op2 == "3":
                    fornecedores_de_um_produto()
                elif op2 == "4":
                    break
                else:
                    print("Opção inválida.")
        elif opcao == "6":
            break
        else:
            print("Opção inválida.")
