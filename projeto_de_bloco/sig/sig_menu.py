# sig/sig_menu.py
from sig.clientes_menu import menu_clientes
from sig.produtos_menu import menu_produtos

def menu_sig():
    while True:
        print("\n=== SIG (Sistema de Informações Gerenciais) ===")
        print("1 - Clientes")
        print("2 - Produtos")
        print("3 - Voltar")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_clientes()
        elif opcao == "2":
            menu_produtos()
        elif opcao == "3":
            break
        else:
            print("Opção inválida.")
