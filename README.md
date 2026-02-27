# Sistema de Gerenciamento de Supermercado

## Descrição do Projeto

Este projeto implementa um **Sistema de Gerenciamento de Supermercado** completo, desenvolvido em Python, utilizando o **SQLAlchemy ORM** para persistência de dados em um banco de dados SQLite. O sistema oferece funcionalidades robustas para o gerenciamento de clientes, produtos, fornecedores e vendas, além de um módulo de *web scraping* para importação inicial de produtos e relatórios gerenciais detalhados.

## Funcionalidades Principais

*   **Gerenciamento de Clientes (CRUD):** Cadastro, consulta, atualização e exclusão de clientes.
*   **Gerenciamento de Produtos (CRUD):** Cadastro, consulta, atualização e exclusão de produtos, com controle de estoque e associação a fornecedores.
*   **Gerenciamento de Fornecedores (CRUD):** Cadastro, consulta, atualização e exclusão de fornecedores.
*   **Registro de Vendas:** Processo de atendimento ao cliente, registro de itens comprados, baixa automática de estoque e emissão de nota fiscal.
*   **Sistema de Informações Gerenciais (SIG):** Relatórios sobre vendas por cliente, produtos mais/menos vendidos, produtos com baixo estoque e produtos por fornecedor.
*   **Web Scraping:** Importação inicial de dados de produtos de uma página web externa.
*   **Importação de Dados Iniciais:** Carregamento de clientes e fornecedores a partir de arquivos JSON e Excel, respectivamente.

## Tecnologias Utilizadas

*   **Python 3.x**
*   **SQLAlchemy:** ORM para interação com o banco de dados.
*   **SQLite:** Banco de dados leve e embarcado.
*   **Pandas:** Manipulação e análise de dados (para importação e relatórios).
*   **Requests:** Para requisições HTTP no web scraping.
*   **BeautifulSoup4:** Para parsing de HTML no web scraping.
*   **Tabulate:** Para formatação de tabelas na saída do console.
*   **Openpyxl:** Dependência para leitura de arquivos Excel com Pandas.

## Estrutura do Projeto
projeto_de_bloco/
├── commons/
│   ├── db.py             # Configuração do banco de dados e sessões
│   ├── models.py         # Definição dos modelos ORM (tabelas)
│   └── utils.py          # Funções utilitárias (entrada de dados, formatação)
├── crud_clientes.py      # Funções CRUD para clientes
├── crud_fornecedores.py  # Funções CRUD para fornecedores
├── crud_produtos.py      # Funções CRUD para produtos
├── crud_vendas.py        # Funções CRUD para vendas
├── dados/                # Arquivos de dados iniciais (clientes.json, fornecedores.xlsx, mercado_sqlalchemy.db)
├── sig/                  # Módulos do Sistema de Informações Gerenciais
│   ├── clientes_menu.py  # Menus e relatórios específicos de clientes
│   ├── produtos_menu.py  # Menus e relatórios específicos de produtos
│   └── sig_menu.py       # Menu principal do SIG
├── main.py               # Ponto de entrada da aplicação
├── relatorios.py         # Módulo de relatórios (fechamento de caixa)
├── requirements.txt      # Dependências do projeto
├── vendas.py             # Lógica de atendimento ao cliente e nota fiscal
└── web_scraping.py       # Módulo para web scraping de produtos

## Como Executar o Projeto

Siga os passos abaixo para configurar e rodar o projeto em sua máquina local:

### Pré-requisitos

Certifique-se de ter o Python 3.x instalado em seu sistema.

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

2. Criar e Ativar um Ambiente Virtual (Recomendado )
Bash
python3 -m venv venv
source venv/bin/activate  # No Windows: .\venv\Scripts\activate

3. Instalar as Dependências
Bash
pip install -r requirements.txt

4. Executar a Aplicação
Bash
python main.py
Ao iniciar, o sistema irá:
Inicializar o banco de dados SQLite (mercado_sqlalchemy.db).
Carregar clientes iniciais do dados/clientes.json (se o banco estiver vazio).
Carregar fornecedores e suas associações do dados/fornecedores.xlsx (se o banco estiver vazio).
Realizar um web scraping para importar produtos de https://pedrovncs.github.io/lindosprecos/produtos.html e salvá-los em dados/produtos.csv, para então importá-los para o banco de dados.
Você será apresentado a um menu interativo no console para interagir com o sistema.
Dados Iniciais
O projeto inclui os seguintes arquivos na pasta dados/ para inicialização:
clientes.json: Contém uma lista de clientes para serem carregados no sistema.
fornecedores.xlsx: Planilha Excel com duas abas (fornecedores e produto_fornecedor ) para carregar fornecedores e suas associações com produtos.


Autor
Juliana Costa