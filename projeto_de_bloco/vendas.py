import pandas as pd
from crud_vendas import consultar_vendas, registrar_venda
from crud_produtos import atualizar_estoque
from tabulate import tabulate
from crud_produtos import pesquisar_produto
from commons.utils import entrar_inteiro, obter_data

def gerar_nota_fiscal(cliente, itens_comprados):
    """
    Registra a venda no banco de dados e exibe a nota fiscal.
    Retorna o objeto Venda registrado.
    """
    # Agrupa os itens para a baixa de estoque e registro.
    df_compras = pd.DataFrame(itens_comprados)

    df_agrupado = df_compras.groupby(['id_produto', 'nome', 'preco'], as_index=False).agg({
        'quantidade':'sum',
        'total_item':'sum'
    })

    # Registra a Venda no DB 
    itens_para_registro = []
    for _, row in df_agrupado.iterrows():
        itens_para_registro.append({
            'id_produto': int(row['id_produto']),
            'quantidade': int(row['quantidade']),
            'preco': float(row['preco'])
        })
        
    venda_registrada = registrar_venda(cliente, itens_para_registro)
    
    if not venda_registrada:
        print("ERRO: Falha ao registrar a venda no banco de dados.")
        return None

    # Faz a Baixa de Estoque Otimizada
    for _, row in df_agrupado.iterrows():
        id_produto = int(row['id_produto'])
        quantidade_vendida = int(row['quantidade'])
        atualizar_estoque(id_produto, -quantidade_vendida) 

    # Exibe a Nota Fiscal (usando o df_agrupado para display)
    total_compra = float(df_agrupado['total_item'].sum())

    tabela_nota = []
    for i, row in df_agrupado.iterrows():
        tabela_nota.append([
            i + 1,
            row['nome'],
            int(row['quantidade']),
            f"R$ {row['preco']:.2f}",
            f"R$ {row['total_item']:.2f}"
        ])

    print("\n" + "="*60)
    print(f"NOTA FISCAL — {cliente.nome} (Venda ID: {venda_registrada.id})")
    print(f"Data: {obter_data()}\n")
    print(tabulate(tabela_nota, headers=["Item", "Produto", "Qtd", "Preço Unit.", "Total"], tablefmt="grid"))
    print(f"\nTotal da compra: R$ {total_compra:.2f}")
    print("="*60)

    return venda_registrada
    


def atender_cliente(cliente):
    """
    Inicia o atendimento de um cliente, registra os itens comprados e gera a nota fiscal.
    Retorna (total, df_agrupado) onde df_agrupado será usado para baixar o estoque.
    """
    print(f"\n=== Iniciando atendimento do {cliente.nome} (ID: {cliente.id}) ===")

    itens_comprados = []

    while True:
        print("\n--- Novo Item ---")
        id_produto = entrar_inteiro("Digite o ID do produto (ou 0 para finalizar): ", min_val=0)

        if id_produto == 0:
            break

        produto = pesquisar_produto(id_produto)
        if not produto:
            print("Produto não encontrado.")
            continue

        print(f"Produto: {produto.nome} — Estoque: {produto.quantidade} — Preço: R$ {produto.preco:.2f}")

        if produto.quantidade == 0:
            print("Erro: Produto sem estoque.")
            continue

        quantidade = entrar_inteiro("Quantidade: ", min_val=1)

        if quantidade <= 0:
            print("Quantidade inválida.")
            continue

        if quantidade > produto.quantidade:
            print(f"Erro: Estoque insuficiente. Máximo disponível: {produto.quantidade}")
            continue

        # registra a compra sem fazer baixa de estoque)
        itens_comprados.append({
            'id_produto': produto.id,
            'nome': produto.nome,
            'quantidade': quantidade,
            'preco': produto.preco,
            'total_item': produto.preco * quantidade
        })

        print(f"{quantidade}x {produto.nome} adicionado(s) ao carrinho.")
        atualizar_estoque(produto.id,-quantidade) #atualizei aqui

    if itens_comprados:
        return gerar_nota_fiscal(cliente, itens_comprados)
    else:
        print("\nNenhum produto comprado.")
        
        return None

def listar_as_vendas():
    print("\n--- VENDAS REGISTRADAS ---")
    vendas = consultar_vendas()

    if not vendas:
        print("Nenhuma venda registrada.")
        return

    # TABELA PRINCIPAL
    tabela = []
    for v in vendas:
        total = sum(float(it.quantidade) * float(it.preco_unitario) for it in (v.itens or []))
        cliente_nome = v.cliente.nome if getattr(v, "cliente", None) else f"ID {v.id_cliente}"

        tabela.append([
            v.id,
            v.data_hora.strftime('%d/%m/%Y %H:%M'),
            cliente_nome,
            f"R$ {total:.2f}"
        ])

    print()
    print(tabulate(
        tabela,
        headers=["ID", "Data/Hora", "Cliente", "Total"],
        tablefmt="github"
    ))

    # ESCOLHA DA VENDA
    id_venda = entrar_inteiro("\nDigite o ID da venda para ver detalhes (0 para voltar): ", min_val=0)
    if id_venda == 0:
        return

    venda = next((x for x in vendas if x.id == id_venda), None)
    if not venda:
        print("Venda não encontrada.")
        return
    mostrar_detalhes_venda(venda)


    
def mostrar_detalhes_venda(venda):

    print("\n--- DETALHES DA VENDA ---")
    print(f"Venda: {venda.id}")
    print(f"Data: {venda.data_hora.strftime('%d/%m/%Y %H:%M')}")
    print(f"Cliente: {venda.cliente.nome if venda.cliente else venda.id_cliente}")
    print("-" * 25)

    # TABELA DE ITENS DA VENDA
    tabela_itens = []
    total = 0.0

    for it in venda.itens:
        subtotal = float(it.quantidade) * float(it.preco_unitario)
        total += subtotal

        nome_prod = it.produto.nome if getattr(it, "produto", None) else f"ID {it.id_produto}"

        tabela_itens.append([
            nome_prod,
            it.quantidade,
            f"R$ {it.preco_unitario:.2f}",
            f"R$ {subtotal:.2f}"
        ])

    print(tabulate(
        tabela_itens,
        headers=["Produto", "Qtd", "Preço Unit.", "Subtotal"],
        tablefmt="fancy_grid",
        colalign=("left", "center", "right", "right")
    ))

    print(f"\nTOTAL: R$ {total:.2f}")



