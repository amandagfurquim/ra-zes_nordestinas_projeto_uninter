from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from database import Base
from sqlalchemy.orm import relationship

Base = declarative_base()

#tabela do usuário
class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

#tabela do produto
class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, default=0)

#tabela do pedido
class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id")) 
    produto_id = Column(Integer, ForeignKey("produtos.id")) 
    quantidade = Column(Integer, default=1)
    total = Column(Float, nullable=False) # Calculado no POST
    status = Column(String, default="PENDENTE")
    forma_pagamento = Column(String, nullable=True)