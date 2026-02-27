# relatorios.py
from tabulate import tabulate
from crud_produtos import consultar_produtos
from crud_vendas import consultar_vendas
from commons.utils import obter_data


def fechar_caixa(vendas_realizadas):
    
    # Exibe o relatório do caixa
    print("\n===========================")
    print("=== FECHAMENTO DO CAIXA ===")
    print("===========================\n")
    print(f"Data: {obter_data()}\n")

    vendas = consultar_vendas()
    
    if not vendas:
        print("Nenhuma venda registrada no banco de dados.")
        print("="*60)
        return

    # Agrupar vendas por cliente
    vendas_por_cliente = {}
    total_vendas = 0.0
    
    for venda in vendas:
        nome_cliente = venda.cliente.nome if venda.cliente else "Cliente Removido"
        total_venda = sum(item.quantidade * item.preco_unitario for item in venda.itens)
        total_vendas += total_venda
        
        if nome_cliente not in vendas_por_cliente:
            vendas_por_cliente[nome_cliente] = 0.0
        
        vendas_por_cliente[nome_cliente] += total_venda

    # Montar tabela
    tabela_clientes = [
        [nome, f"R$ {total:.2f}"]
        for nome, total in vendas_por_cliente.items()
    ]

    print(tabulate(tabela_clientes, headers=["Cliente", "Total Gasto"], tablefmt="fancy_grid"))
    print(f"\nTotal de vendas do caixa: R$ {total_vendas:.2f}\n")

    # Produtos sem estoque
    produtos = consultar_produtos()
    sem_estoque = [p for p in produtos if p.quantidade == 0]

    print("--- Produtos Sem Estoque ---")

    if sem_estoque:
        tabela_sem_estoque = [[p.id, p.nome, p.quantidade] for p in sem_estoque]
        print(tabulate(tabela_sem_estoque, headers=["ID", "Nome", "Qtd"], tablefmt="fancy_grid"))
    else:
        print(tabulate([["Nenhum produto esgotado"]], tablefmt="fancy_grid"))




