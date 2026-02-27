# utils.py
from datetime import datetime

def entrar_inteiro(mensagem: str, min_val: int = 0) -> int:
    '''tratamento para número int.'''
    while True:
        try:
            valor = int(input(mensagem))
            if valor >= min_val:
                return valor
            else:
                print(f"Erro: O valor deve ser maior ou igual a {min_val}.")
        except ValueError:
            print("Erro: Digite um número inteiro válido.")

def entrar_float(mensagem: str, min_val: float = 0.0) -> float:
    '''tratamento pra número float.'''
    while True:
        try:
            valor = input(mensagem).strip()
            valor = valor.replace(',', '.')
            f = float(valor)
            if f >= min_val:
                return f
            else:
                print(f"Erro: O valor deve ser maior ou igual a {min_val}.")
        except ValueError:
            print("Erro: Digite um número decimal válido.")

def obter_data() -> str:
    
    return datetime.now().strftime('%d/%m/%Y %H:%M')
