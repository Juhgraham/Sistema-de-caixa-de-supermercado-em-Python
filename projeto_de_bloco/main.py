# main.py
from commons.db import init_db
from crud_clientes import (
    carregar_clientes_iniciais, buscar_cliente, cadastrar_cliente
)
from vendas import atender_cliente, listar_as_vendas
from crud_fornecedores import carregar_fornecedores_iniciais
from relatorios import fechar_caixa
from sig.sig_menu import menu_sig
from web_scraping import realizar_web_scraping, salvar_produtos_csv
from crud_produtos import importar_produtos_csv
from commons.utils import entrar_inteiro


def inicializar_sistema():
    print("---- Iniciando Sistema ----\n")
    
    init_db()
    carregar_clientes_iniciais()
    carregar_fornecedores_iniciais()

    df_produtos = realizar_web_scraping()
    if df_produtos is not None:
        salvar_produtos_csv(df_produtos)
        importar_produtos_csv()
    else:
        print("\nAviso: Não foi possível realizar o web scraping.")
    
    principal()




def principal():

    vendas_realizadas = []

    while True:

        print("""
    ==== Bem-Vindos ao Supermercado ====\n
    ====================================
    """)
        print("\n1 - Caixa - Atendimento ao Cliente")
        print("2 - Acessar SIG (Sistema de Informações Gerenciais)")
        print("3 - Listar vendas")
        print("4 - Fechar caixa e sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\n--- Atendimento ao Cliente ---")
            id_cliente = entrar_inteiro("Digite o ID do Cliente (ou 0 para novo cadastro): ", min_val=0)

            cliente = None
            if id_cliente > 0:
                cliente = buscar_cliente(id_cliente)
                if not cliente:
                    print("Cliente não encontrado. Realizando novo cadastro.")
                    id_cliente = 0

            if id_cliente == 0:
                nome_cliente = input("Digite o nome do novo cliente: ")
                cliente = cadastrar_cliente(nome_cliente)
                if not cliente:
                    print("Falha ao cadastrar cliente. Retornando ao menu principal.")
                    continue

            venda_registrada = atender_cliente(cliente)
            if venda_registrada:
                vendas_realizadas.append(venda_registrada)

        elif opcao == "2":
            menu_sig()

        elif opcao == "3":
            listar_as_vendas()

        elif opcao == "4":
            fechar_caixa(vendas_realizadas)
            print("\nCaixa encerrado. Até logo!\n")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    inicializar_sistema()
