🛒 Sistema de Gerenciamento de Supermercado
📌 Descrição do Projeto

Este projeto implementa um Sistema de Gerenciamento de Supermercado completo, desenvolvido em Python, utilizando o SQLAlchemy ORM para persistência de dados em um banco de dados SQLite.

O sistema oferece funcionalidades para gerenciamento de clientes, produtos, fornecedores e vendas, além de um módulo de web scraping para importação inicial de produtos e geração de relatórios gerenciais detalhados.

🚀 Funcionalidades Principais

Gerenciamento de Clientes (CRUD)
Cadastro, consulta, atualização e exclusão de clientes.

Gerenciamento de Produtos (CRUD)
Cadastro, consulta, atualização e exclusão de produtos, com controle de estoque e associação a fornecedores.

Gerenciamento de Fornecedores (CRUD)
Cadastro, consulta, atualização e exclusão de fornecedores.

Registro de Vendas
Processo de atendimento ao cliente, registro de itens comprados, baixa automática de estoque e emissão de nota fiscal.

Sistema de Informações Gerenciais (SIG)
Relatórios sobre:

Vendas por cliente

Produtos mais/menos vendidos

Produtos com baixo estoque

Produtos por fornecedor

Web Scraping
Importação inicial de produtos a partir de uma página web externa.

Importação de Dados Iniciais

Clientes via arquivo JSON

Fornecedores via planilha Excel

🛠 Tecnologias Utilizadas

Python 3.x

SQLAlchemy — ORM para interação com o banco de dados

SQLite — Banco de dados leve e embarcado

Pandas — Manipulação e análise de dados

Requests — Requisições HTTP (web scraping)

BeautifulSoup4 — Parsing de HTML

Tabulate — Formatação de tabelas no console

Openpyxl — Leitura de arquivos Excel via Pandas

📂 Estrutura do Projeto
projeto_de_bloco/
│
├── commons/
│   ├── db.py              # Configuração do banco de dados e sessões
│   ├── models.py          # Definição dos modelos ORM (tabelas)
│   └── utils.py           # Funções utilitárias
│
├── crud_clientes.py       # CRUD de clientes
├── crud_fornecedores.py   # CRUD de fornecedores
├── crud_produtos.py       # CRUD de produtos
├── crud_vendas.py         # CRUD de vendas
│
├── dados/                 # Arquivos de dados iniciais
│   ├── clientes.json
│   ├── fornecedores.xlsx
│   └── mercado_sqlalchemy.db
│
├── sig/                   # Sistema de Informações Gerenciais
│   ├── clientes_menu.py
│   ├── produtos_menu.py
│   └── sig_menu.py
│
├── main.py                # Ponto de entrada da aplicação
├── relatorios.py          # Relatórios (fechamento de caixa)
├── requirements.txt       # Dependências do projeto
├── vendas.py              # Lógica de vendas e nota fiscal
└── web_scraping.py        # Web scraping de produtos
▶️ Como Executar o Projeto
✅ Pré-requisitos

Python 3.x instalado

1️⃣ Clonar o Repositório
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
2️⃣ Criar e Ativar um Ambiente Virtual (Recomendado)

Linux / MacOS

python3 -m venv venv
source venv/bin/activate

Windows

python -m venv venv
.\venv\Scripts\activate
3️⃣ Instalar as Dependências
pip install -r requirements.txt
4️⃣ Executar a Aplicação
python main.py
🔄 Ao iniciar o sistema

O sistema irá:

Inicializar o banco de dados SQLite (mercado_sqlalchemy.db)

Carregar clientes do arquivo dados/clientes.json (caso o banco esteja vazio)

Carregar fornecedores do arquivo dados/fornecedores.xlsx

Realizar web scraping da página:
https://pedrovncs.github.io/lindosprecos/produtos.html

Gerar o arquivo dados/produtos.csv

Importar os produtos para o banco de dados

Após isso, será exibido um menu interativo no console para utilização do sistema.

📊 Dados Iniciais

O projeto inclui arquivos para inicialização automática:

clientes.json — Lista de clientes

fornecedores.xlsx — Planilha com duas abas:

fornecedores

produto_fornecedor

👩‍💻 Autor

Juliana Pereira Costa
