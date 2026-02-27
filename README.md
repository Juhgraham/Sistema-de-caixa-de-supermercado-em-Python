# 🛒 Sistema de Gerenciamento de Supermercado

## 📌 Descrição do Projeto

Este projeto implementa um **Sistema de Gerenciamento de Supermercado** desenvolvido em **Python**, utilizando **SQLAlchemy ORM** para persistência de dados em um banco **SQLite**.

O sistema permite o gerenciamento completo de clientes, produtos, fornecedores e vendas, além de contar com importação de dados iniciais e um módulo de **web scraping** para carregamento automático de produtos.

---

## 🚀 Funcionalidades Principais

- **Gerenciamento de Clientes (CRUD)**
  - Cadastro
  - Consulta
  - Atualização
  - Exclusão

- **Gerenciamento de Produtos (CRUD)**
  - Controle de estoque
  - Associação com fornecedores

- **Gerenciamento de Fornecedores (CRUD)**

- **Registro de Vendas**
  - Atendimento ao cliente
  - Registro de itens comprados
  - Baixa automática de estoque
  - Emissão de nota fiscal

- **Sistema de Informações Gerenciais (SIG)**
  - Vendas por cliente
  - Produtos mais/menos vendidos
  - Produtos com baixo estoque
  - Produtos por fornecedor

- **Web Scraping**
  - Importação automática de produtos via página web

- **Importação de Dados Iniciais**
  - Clientes via arquivo JSON
  - Fornecedores via planilha Excel

---

## 🛠 Tecnologias Utilizadas

- **Python 3.x**
- **SQLAlchemy** — ORM para interação com banco de dados
- **SQLite** — Banco de dados leve e embarcado
- **Pandas** — Manipulação e análise de dados
- **Requests** — Requisições HTTP
- **BeautifulSoup4** — Parsing de HTML
- **Tabulate** — Formatação de tabelas no console
- **Openpyxl** — Leitura de arquivos Excel

---

## 📂 Estrutura do Projeto

```bash
projeto_de_bloco/
│
├── commons/
│   ├── db.py              # Configuração do banco de dados
│   ├── models.py          # Modelos ORM (tabelas)
│   └── utils.py           # Funções utilitárias
│
├── crud_clientes.py       # CRUD de clientes
├── crud_fornecedores.py   # CRUD de fornecedores
├── crud_produtos.py       # CRUD de produtos
├── crud_vendas.py         # CRUD de vendas
│
├── dados/
│   ├── clientes.json
│   ├── fornecedores.xlsx
│   └── mercado_sqlalchemy.db
│
├── sig/
│   ├── clientes_menu.py
│   ├── produtos_menu.py
│   └── sig_menu.py
│
├── main.py                # Ponto de entrada da aplicação
├── relatorios.py          # Relatórios e fechamento de caixa
├── requirements.txt       # Dependências do projeto
├── vendas.py              # Lógica de vendas e nota fiscal
└── web_scraping.py        # Módulo de web scraping
```

---

## ▶️ Como Executar o Projeto

### ✅ Pré-requisitos

- Python 3.x instalado

---

### 1️⃣ Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

---

### 2️⃣ Criar e Ativar Ambiente Virtual (Recomendado)

**Linux / MacOS**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**
```bash
python -m venv venv
.\venv\Scripts\activate
```

---

### 3️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Executar a Aplicação

```bash
python main.py
```

---

## 🔄 Inicialização Automática

Ao iniciar, o sistema irá:

- Criar o banco de dados `mercado_sqlalchemy.db`
- Importar clientes do arquivo `dados/clientes.json` (caso o banco esteja vazio)
- Importar fornecedores do arquivo `dados/fornecedores.xlsx`
- Realizar web scraping da página:
  
  https://pedrovncs.github.io/lindosprecos/produtos.html

- Gerar o arquivo `dados/produtos.csv`
- Importar os produtos para o banco de dados

Após isso, será exibido um **menu interativo no console** para utilização do sistema.

---

## 📊 Dados Iniciais

O projeto inclui:

- `clientes.json` — Lista de clientes
- `fornecedores.xlsx` — Planilha com duas abas:
  - `fornecedores`
  - `produto_fornecedor`

---

## 💡 Possíveis Melhorias Futuras

- Interface gráfica (GUI ou Web)
- Autenticação de usuários
- Testes automatizados
- Deploy em ambiente cloud
- API REST com FastAPI

---

## 👩‍💻 Autora

**Juliana Pereira Costa**  
Estudante de Engenharia de Software com foco em Dados

---
