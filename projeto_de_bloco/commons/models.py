# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from commons.db import Base
from datetime import datetime

# Tabela Associativa
class ProdutoFornecedor(Base):
    __tablename__ = "produto_fornecedor"

    id_produto = Column(Integer, ForeignKey("produtos.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    id_fornecedor = Column(Integer, ForeignKey("fornecedores.id_fornecedor", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

    def __repr__(self):
        return f"<ProdutoFornecedor(produto={self.id_produto}, fornecedor={self.id_fornecedor})>"

#Fornecedor
class Fornecedor(Base):
    __tablename__ = "fornecedores"
    id_fornecedor = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False, unique=True)
    
    produtos = relationship("Produto", secondary="produto_fornecedor", back_populates="fornecedores")

    def __repr__(self):
        return f"<Fornecedor(id={self.id}, nome={self.nome!r})>"

# Produto 
class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco = Column(Float, nullable=False)
    
    fornecedores = relationship("Fornecedor", secondary="produto_fornecedor", back_populates="produtos")
    
    itens_venda = relationship("ItemVenda", back_populates="produto")

    def __repr__(self):
        fornecedores_nomes = ", ".join([f.nome for f in self.fornecedores])
        return f"<Produto(id={self.id}, nome={self.nome!r}, qtd={self.quantidade}, preco={self.preco:.2f}, fornecedores=[{fornecedores_nomes}])>"

#  Cliente 
class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    
    vendas = relationship("Venda", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente(id={self.id}, nome={self.nome!r})>"

# Venda 
class Venda(Base):
    __tablename__ = "vendas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_hora = Column(DateTime, default=datetime.now)
    
    id_cliente = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE", onupdate="CASCADE"))
    cliente = relationship("Cliente", back_populates="vendas")
    
    itens = relationship("ItemVenda", back_populates="venda", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Venda(id={self.id}, cliente={self.cliente.nome}, data={self.data_hora.strftime('%d/%m/%Y %H:%M')})>"

# ItemVenda
class ItemVenda(Base):
    __tablename__ = "itens_venda"
    id = Column(Integer, primary_key=True, autoincrement=True)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False) # Preço no momento da venda
    
    id_venda = Column(Integer, ForeignKey("vendas.id", ondelete="CASCADE", onupdate="CASCADE"))
    venda = relationship("Venda", back_populates="itens")
    
    id_produto = Column(Integer, ForeignKey("produtos.id", ondelete="CASCADE", onupdate="CASCADE"))
    produto = relationship("Produto", back_populates="itens_venda")

    def __repr__(self):
        return f"<ItemVenda(id={self.id}, produto={self.produto.nome}, qtd={self.quantidade}, preco={self.preco_unitario:.2f})>"
